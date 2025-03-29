import logging
import re
import uuid

import cloe_metadata.base.repository.database.column as base_column
import jinja2 as j2
from cloe_metadata import base
from cloe_util_snowflake_connector import snowflake_interface
from pydantic import BaseModel, ConfigDict

from ..utils.template_env import env_sql

logger = logging.getLogger(__name__)


class SnowflakeCrawler(BaseModel):
    """
    Class to construct a crawler to retrieve snowflake metadata
    and transform to a CLOE compatible format.
    """

    snf_interface: snowflake_interface.SnowflakeInterface
    ignore_columns: bool
    ignore_tables: bool
    databases: base.Databases = base.Databases(databases=[])
    schemas: dict[str, list[base.Schema]] = {}
    databases_cache: dict[str, base.Database] = {}
    templates_env: j2.Environment = env_sql
    database_filter: str | None = None
    database_name_replace: str | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get_databases(self) -> None:
        """Retrieves databases in snowflake and adds them to the repository."""
        query = "SHOW DATABASES"
        all_databases = self.snf_interface.run_one_with_return(query)
        result_w_names = []
        if self.database_filter is not None:
            pattern = re.compile(self.database_filter)
            for raw_database in all_databases:
                if pattern.match(raw_database["name"]) is not None:
                    result_w_names.append(raw_database)
        else:
            result_w_names = all_databases
        for row in result_w_names:
            db_name = row["name"]
            if db_name.lower() in ("snowflake", "snowflake_sample_data"):
                continue
            database = base.Database(name=db_name, schemas=[])
            self.databases_cache[database.name] = database
            self.databases.databases.append(database)

    def _transform_table_columns(
        self,
        table_columns: list[dict[str, str]],
    ) -> dict[str, list[base_column.Column]]:
        """
        Transforms a query result from a snowflake information schema
        columns view into a CLOE columns object and gathering all columns
        of all table in a dict.
        """
        tables: dict[str, list[base_column.Column]] = {}
        for row in table_columns:
            if f"{row['TABLE_SCHEMA']}{row['TABLE_NAME']}" not in tables:
                tables[f"{row['TABLE_SCHEMA']}{row['TABLE_NAME']}"] = []
            column = base_column.Column(
                name=row["COLUMN_NAME"],
                ordinal_position=int(row["ORDINAL_POSITION"])
                if row["ORDINAL_POSITION"] is not None
                else None,
                is_key=bool(row["IS_IDENTITY"])
                if row["IS_IDENTITY"] is not None
                else None,
                is_nullable=bool(row["IS_NULLABLE"])
                if row["IS_NULLABLE"] is not None
                else None,
                data_type=row["DATA_TYPE"],
                constraints=row["COLUMN_DEFAULT"],
                data_type_length=int(row["CHARACTER_MAXIMUM_LENGTH"])
                if row["CHARACTER_MAXIMUM_LENGTH"] is not None
                else None,
                data_type_numeric_scale=int(row["NUMERIC_SCALE"])
                if row["NUMERIC_SCALE"] is not None
                else None,
                data_type_precision=int(row["NUMERIC_PRECISION"])
                if row["NUMERIC_PRECISION"] is not None
                else None,
            )
            tables[f"{row['TABLE_SCHEMA']}{row['TABLE_NAME']}"].append(column)
        return tables

    def _get_schemas(self) -> None:
        """
        Retrieves schemas in snowflake and saves them in the
        corrspeonding database
        """
        queries = {}
        for database in self.databases.databases:
            queries[database.name] = self.templates_env.get_template(
                "schema_retrieve.sql.j2",
            ).render(database_name=database.name)
        logger.debug("Queries for schema crawl created.")
        result_w_names = self.snf_interface.run_many_with_return(queries)
        logger.debug("Schema crawl results retrieved.")
        for database_name, result in result_w_names.items():
            if not result:
                continue
            for row in result:
                schema = base.Schema(name=row["SCHEMA_NAME"])
                self.databases_cache[database_name].schemas.append(schema)
                if database_name not in self.schemas:
                    self.schemas[database_name] = []
                self.schemas[database_name].append(schema)

    def _get_tables(self) -> None:
        """
        Retrieves tables in snowflake and saves them in the corrspeonding schema
        """
        queries = {}
        for database in self.databases.databases:
            if not self.ignore_columns:
                queries[database.name] = self.templates_env.get_template(
                    "column_retrieve.sql.j2",
                ).render(database_name=database.name)
            else:
                queries[database.name] = self.templates_env.get_template(
                    "table_retrieve.sql.j2",
                ).render(database_name=database.name)
        logger.debug("Queries for tables crawl created.")
        result_w_names = self.snf_interface.run_many_with_return(queries)
        logger.debug("Tables crawl results retrieved.")
        for database_name, result in result_w_names.items():
            if result is None:
                continue
            schemas: dict[str, list[base.Table]] = {
                schema_name: []
                for schema_name in sorted({row["TABLE_SCHEMA"] for row in result})
            }
            table_columns = {}
            if not self.ignore_columns:
                table_columns = self._transform_table_columns(result)
            for table_info in sorted(
                {(row["TABLE_SCHEMA"], row["TABLE_NAME"]) for row in result},
                key=lambda x: "".join(x),
            ):
                new_table = base.Table(
                    id=uuid.uuid4(),
                    name=table_info[1],
                    columns=table_columns.get(f"{table_info[0]}{table_info[1]}", []),
                )
                schemas[table_info[0]].append(new_table)
            for schema_name, schema_tables in schemas.items():
                schema = base.Schema(name=schema_name, tables=schema_tables)
                self.databases_cache[database_name].schemas.append(schema)

    def _transform(self) -> None:
        """Transform databases in a CLOE json format."""
        for database in self.databases.databases:
            if self.database_name_replace is not None:
                database.name = re.sub(
                    self.database_name_replace,
                    r"{{ CLOE_BUILD_CRAWLER_DB_REPLACEMENT }}",
                    database.name,
                )

    def to_json(self) -> str:
        return self.databases.model_dump_json(
            indent=4,
            by_alias=True,
            exclude_none=True,
        )

    def crawl(self) -> None:
        """
        Crawls a snowflake instance and saves metadata
        in a CLOE compatible format
        """
        self._get_databases()
        if self.ignore_tables:
            self._get_schemas()
        else:
            self._get_tables()
        self._transform()
        self.snf_interface.close()
