from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from zmp_openapi_models.alerts import (
    AlertSortField,
    AlertStatus,
    Priority,
    RepeatedCountOperator,
    Sender,
    Severity,
)

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 500


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class GetAlertsInput(BaseModel):
    statuses: list[AlertStatus] = Field(
        default_factory=list,
        title="alert status",
        description="Search Field string for status"
    )
    senders: list[Sender] = Field(
        default_factory=list,
        title="alert sender",
        description="Search Field string for sender"
    )
    priorities: list[Priority] = Field(
        default_factory=list,
        title="alert priority",
        description="Search Field string for alert priority"
    )
    severities: list[Severity] = Field(
        default_factory=list,
        title="alert severity",
        description="Search Field string for alert severity"
    )
    fingerprint: Optional[str] = Field(
        default=None,
        max_length=36,
        title="alert fingerprint",
        description="Search Field string for fingerprint. The max length is 36"
    )
    alert_id: Optional[str] = Field(
        default=None,
        max_length=100,
        title="alert id",
        description="Search Field string for fingerprint. The max length is 100"
    )
    repeated_count: Optional[int] = Field(
        default=None,
        le=10000,
        title="alert repeated count",
        description="Search Field string for repeated count, Should be less than 10000"
    )
    repeated_count_operator: RepeatedCountOperator = Field(
        default=RepeatedCountOperator.GTE,
        title="alert repeated count operator",
        description="Search Field string for repeated count operator"
    )
    alertname: Optional[str] = Field(
        default=None,
        max_length=100,
        title="alert name",
        description="Search Field string for alert name. The max length is 100"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=100,
        title="alert description",
        description="Search Field string for alert description. The max length is 100"
    )
    summary: Optional[str] = Field(
        default=None,
        max_length=100,
        title="alert summary",
        description="Search Field string for alert summary. The max length is 100"
    )
    project: Optional[str] = Field(
        default=None,
        max_length=100,
        title="alert project",
        description="Search Field string for alert project. The max length is 100"
    )
    clusters: list[str] = Field(
        default_factory=list,
        title="alert clusters",
        description="Search Field string for alert clusters"
    )
    namespaces: list[str] = Field(
        default_factory=list,
        title="alert namespaces",
        description="Search Field string for alert namespaces"
    )
    start_date: Optional[str] = Field(
        default=None,
        title="search start date",
        description="Search Field string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    end_date: Optional[str] = Field(
        default=None,
        title="search end date",
        description="Search Field string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    start_date_created_at: Optional[str] = Field(
        default=None,
        title="search start date",
        description="Search Field string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    end_date_created_at: Optional[str] = Field(
        default=None,
        title="search end date",
        description="Search Field string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    start_date_closed_at: Optional[str] = Field(
        default=None,
        title="search start date",
        description="Search Field string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    end_date_closed_at: Optional[str] = Field(
        default=None,
        title="search end date",
        description="Search Field string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    labels: list[str] = Field(
        default_factory=list,
        title="search labels",
        description="Search Field string for labels e.g. severity:critical,priority:P1"
    )
    sort_field: AlertSortField = Field(
        default=AlertSortField.UPDATED_AT,
        title="sort field",
        description="Sort field name"
    )
    sort_direction: SortDirection = Field(
        default=SortDirection.DESC,
        title="sort direction",
        description="Sort direction"
    )
    page_number: Optional[int] = Field(
        default=DEFAULT_PAGE_NUMBER,
        ge=DEFAULT_PAGE_NUMBER,
        title="page number",
        description=f"Page number. Default is {DEFAULT_PAGE_NUMBER} and it should be greater than 0"
    )
    page_size: Optional[int] = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=DEFAULT_PAGE_SIZE,
        le=MAX_PAGE_SIZE,
        title="page size",
        description=f"Page size. Default is {DEFAULT_PAGE_SIZE} and it should be greater than 10 and less than {MAX_PAGE_SIZE}"
    )
