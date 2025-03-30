import logging
from typing import Optional

import click
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from zmp_openapi_models.alerts import (
    AlertSortField,
    AlertStatus,
    Priority,
    RepeatedCountOperator,
    Sender,
    Severity,
)

from zmp_alert_mcp_server.api_wrapper import AuthenticationType, ZmpAPIWrapper
from zmp_alert_mcp_server.input_schema import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    GetAlertsInput,
    SortDirection,
)
from zmp_alert_mcp_server.operations import operations

# for stdio
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logging.getLogger("zmp_openapi_toolkit.openapi.zmpapi_models").setLevel(logging.INFO)
logging.getLogger("zmp_openapi_toolkit.toolkits.toolkit").setLevel(logging.INFO)
logging.getLogger("httpcore.http11").setLevel(logging.INFO)
logging.getLogger("httpcore.http11").setLevel(logging.INFO)
logging.getLogger("mcp.server.lowlevel.server").setLevel(logging.DEBUG)
logging.getLogger("mcp.server.fastmcp.tools.tool_manager").setLevel(logging.DEBUG)
logging.getLogger("mcp.server.fastmcp.server").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


class GatewaySettings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="ZMP_GW_", env_file=".env"
    )
    endpoint: str
    access_key: str


def init_mcp(mcp: FastMCP, api_wrapper: ZmpAPIWrapper):
    @mcp.tool(description="Alert search using multiple filters")
    def get_alerts(
        statuses: list[AlertStatus] | None = Field(
            default_factory=list,
            description="Search query string for status. Values are Open, Closed, Acked, Snoozed",
        ),
        senders: list[Sender] | None = Field(
            default_factory=list,
            description="Search query string for sender.",
        ),
        priorities: list[Priority] | None = Field(
            default_factory=list,
            description="Search query string for alert priority. Values: P1, P2, P3, P4, P5",
        ),
        severities: list[Severity] | None = Field(
            default_factory=list,
            description="Search query string for alert severity. Values: critical, warning",
        ),
        fingerprint: Optional[str] = Field(
            default=None,
            max_length=36,
            description="Search query string for fingerprint. The max length is 36",
        ),
        alert_id: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Search query string for fingerprint. The max length is 100",
        ),
        repeated_count: Optional[int] = Field(
            default=None,
            le=10000,
            description="Search query string for repeated count, Should be less than 10000",
        ),
        repeated_count_operator: Optional[RepeatedCountOperator] = Field(
            default=RepeatedCountOperator.GTE,
            description="Search query string for repeated count operator. Values: GTE, LTE, EQ, NEQ",
        ),
        alertname: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Search query string for alert name. The max length is 100",
        ),
        description: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Search query string for alert description. The max length is 100",
        ),
        summary: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Search query string for alert summary. The max length is 100",
        ),
        project: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Search query string for alert project. The max length is 100",
        ),
        clusters: list[str] | None = Field(
            default_factory=list,
            description="Search query string for alert clusters",
        ),
        namespaces: list[str] | None = Field(
            default_factory=list,
            description="Search query string for alert namespaces",
        ),
        start_date: Optional[str] = Field(
            default=None,
            description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        ),
        end_date: Optional[str] = Field(
            default=None,
            description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        ),
        start_date_created_at: Optional[str] = Field(
            default=None,
            description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        ),
        end_date_created_at: Optional[str] = Field(
            default=None,
            description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        ),
        start_date_closed_at: Optional[str] = Field(
            default=None,
            description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        ),
        end_date_closed_at: Optional[str] = Field(
            default=None,
            description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        ),
        labels: list[str] | None = Field(
            default_factory=list,
            description="Search query string for labels e.g. severity:critical,priority:P1",
        ),
        sort_field: Optional[AlertSortField] = Field(
            default=AlertSortField.UPDATED_AT,
            description="Sort field name. Values: UPDATED_AT, CREATED_AT, CLOSED_AT",
        ),
        sort_direction: Optional[SortDirection] = Field(
            default=SortDirection.DESC,
            description="Sort direction. Values: ASC, DESC",
        ),
        page_number: Optional[int] = Field(
            default=DEFAULT_PAGE_NUMBER,
            ge=DEFAULT_PAGE_NUMBER,
            description=f"Page number. Default is {DEFAULT_PAGE_NUMBER} and it should be greater than 0",
        ),
        page_size: Optional[int] = Field(
            default=DEFAULT_PAGE_SIZE,
            ge=DEFAULT_PAGE_SIZE,
            le=MAX_PAGE_SIZE,
            description=f"Page size. Default is {DEFAULT_PAGE_SIZE} and it should be greater than 10 and less than {MAX_PAGE_SIZE}",
        ),
    ) -> CallToolResult:
        kwargs = {
            "statuses": statuses,
            "senders": senders,
            "priorities": priorities,
            "severities": severities,
            "fingerprint": fingerprint,
            "alert_id": alert_id,
            "repeated_count": repeated_count,
            "repeated_count_operator": repeated_count_operator,
            "alertname": alertname,
            "description": description,
            "summary": summary,
            "project": project,
            "clusters": clusters,
            "namespaces": namespaces,
            "start_date": start_date,
            "end_date": end_date,
            "start_date_created_at": start_date_created_at,
            "end_date_created_at": end_date_created_at,
            "start_date_closed_at": start_date_closed_at,
            "end_date_closed_at": end_date_closed_at,
            "labels": labels,
            "sort_field": sort_field,
            "sort_direction": sort_direction,
            "page_number": page_number,
            "page_size": page_size,
        }

        query_params = GetAlertsInput(**kwargs)
        operation = operations["get_alerts"]
        try:
            data = api_wrapper.run(
                operation["method"], operation["path"], query_params=query_params
            )

            logger.info(f"Response Data: {data}")

            return CallToolResult(
                content=[TextContent(type="text", text=f"Operation successful: {data}")]
            )
        except Exception as error:
            logger.error(f"Error: {error}")
            return CallToolResult(
                isError=True,
                content=[TextContent(type="text", text=f"Error: {str(error)}")],
            )


@click.command()
# @click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
# @click.option("--endpoint", "-e", type=str, required=True, help="ZMP OpenAPI endpoint")
@click.option(
    "--access-key", "-s", type=str, required=True, help="ZMP OpenAPI access key"
)
def main(transport: str, access_key: str):
    mcp = FastMCP(
        name="ZMP Alert Server",
        instructions="You are a server that receives alerts from the ZMP API and sends them to the user.",
        dependencies=["zmp_openapi_models"],
        host="0.0.0.0",
        port=8888,
    )
    gw_settings = GatewaySettings()
    api_wrapper = ZmpAPIWrapper(
        gw_settings.endpoint,
        access_key=access_key
    )
    init_mcp(mcp, api_wrapper)
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
