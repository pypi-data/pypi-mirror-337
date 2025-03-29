from cloe_metadata import base


def merge_repository_content(
    new_content: base.Databases,
    old_content: base.Databases,
) -> base.Databases:
    old_tables = {
        f"{database.name}.{schema.name}.{table.name}": table
        for database in old_content.databases
        for schema in database.schemas
        for table in schema.tables
    }
    for database in new_content.databases:
        for schema in database.schemas:
            for table in schema.tables:
                if old_table := old_tables.get(
                    f"{database.name}.{schema.name}.{table.name}",
                ):
                    table.id = old_table.id
                    table.level = old_table.level
    return new_content
