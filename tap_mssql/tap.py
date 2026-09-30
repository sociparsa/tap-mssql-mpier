"""mssql tap class."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON schema typing helpers
from singer_sdk.contrib.msgspec import MsgSpecWriter
from singer_sdk.sql import SQLTap

from .client import MSSQLStream


class Tapmssql(SQLTap):
    """mssql tap class."""

    name = "tap-mssql"
    default_stream_class = MSSQLStream
    message_writer_class = MsgSpecWriter

    config_jsonschema = th.PropertiesList(
        th.Property(
            "dialect",
            th.StringType,
            description="The Dialect of SQLAlchamey",
            required=True,
            allowed_values=["mssql"],
            default="mssql"
        ),
        th.Property(
            "driver_type",
            th.StringType,
            description="The Python Driver you will be using to connect to the SQL server",
            required=True,
            allowed_values=["pyodbc", "pymssql"],
            default="pymssql"
        ),
        th.Property(
            "host",
            th.StringType,
            description="The FQDN of the Host serving out the SQL Instance",
            required=True
        ),
        th.Property(
            "port",
            th.IntegerType,
            description="The port on which SQL awaiting connection"
        ),
        th.Property(
            "user",
            th.StringType,
            description="The User Account who has been granted access to the SQL Server",
        ),
        th.Property(
            "password",
            th.StringType,
            description="The Password for the User account",
            secret=True
        ),
        th.Property(
            "database",
            th.StringType,
            description="The Default database for this connection",
            required=True
        ),
        th.Property(
            "azure_access_tokens",
            th.StringType,
            description="Obtain Azure Access Tokens when connecting: \'True\', \'False\'",
            default="False"
        ),
        th.Property(
            "sqlalchemy_eng_params",
            th.ObjectType(
                th.Property(
                    "fast_executemany",
                    th.StringType,
                    description="Fast Executemany Mode: True, False"
                ),
                th.Property(
                    "future",
                    th.StringType,
                    description="Run the engine in 2.0 mode: True, False"
                )
            ),
            description="SQLAlchemy Engine Paramaters: fast_executemany, future"
        ),
        th.Property(
            "sqlalchemy_url_query",
            th.ObjectType(
                th.Property(
                    "driver",
                    th.StringType,
                    description="The Driver to use when connection should match the Driver Type"
                ),
                th.Property(
                    "MultiSubnetFailover",
                    th.StringType,
                    description="This is a Yes No option"
                ),
                th.Property(
                    "TrustServerCertificate",
                    th.StringType,
                    description="This is a Yes No option"
                )
            ),
            description="SQLAlchemy URL Query options: driver, MultiSubnetFailover, TrustServerCertificate"  # noqa: E501
        ),
        th.Property(
            "batch_config",
            th.ObjectType(
                th.Property(
                    "encoding",
                    th.ObjectType(
                        th.Property(
                            "format",
                            th.StringType,
                            description="Currently the only format is jsonl",
                        ),
                        th.Property(
                            "compression",
                            th.StringType,
                            description="Currently the only compression options is gzip",
                        )
                    )
                ),
                th.Property(
                    "storage",
                    th.ObjectType(
                        th.Property(
                            "root",
                            th.StringType,
                            description=("the directory you want batch messages to be placed in\n"
                                        "example: file://test/batches"
                            )
                        ),
                        th.Property(
                            "prefix",
                            th.StringType,
                            description=("What prefix you want your messages to have\n"
                                        "example: test-batch-"
                            )
                        )
                    )
                )
            ),
            description="Optional Batch Message configuration",
        ),
        th.Property(
            "stream_filters",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "stream",
                        th.StringType,
                        required=True,
                        description=("Name of the stream to filter, "
                                     "example: dbo-my_table")
                    ),
                    th.Property(
                        "filters",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "column_label",
                                    th.StringType,
                                    required=True,
                                    description=("Label of the column to filter on.")
                                ),
                                th.Property(
                                    "operation",
                                    th.StringType,
                                    required=True,
                                    description=("Type of filter operation: "
                                                 "['==','<=','>=','<', '>', '!=']"),
                                    allowed_values=["==", "<=", ">=", "<", ">", "!="]
                                ),
                                th.Property(
                                    "value",
                                    th.StringType,
                                    required=True,
                                    description=("Filter value.")
                                ),
                                th.Property(
                                    "type",
                                    th.StringType,
                                    required=True,
                                    description=("Type of the filter value. "
                                                 "Can be one of the following: "
                                                 "['String','Float','Integer','Date','DateTime','Boolean']"),
                                    allowed_values=["String", "Float", "Integer",
                                                    "Date", "DateTime", "Boolean"]
                                )
                            )
                        ),
                        required=True,
                    )
                ),
            ),
            description=("Filters added to the WHERE clause of a stream's SQL "
                         "query, applied with or without batch_config. "
                         "All filters of a stream are combined with AND."),
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
        th.Property(
            "hd_jsonschema_types",
            th.BooleanType,
            default=False,
            description="Turn on Higher Defined(HD) JSON Schema types to assist Targets"
        ),
    ).to_dict()


if __name__ == "__main__":
    Tapmssql.cli()
