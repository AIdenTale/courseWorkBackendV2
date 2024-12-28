from pydantic import BaseModel


class ReportAggregatedStatuses(BaseModel):
    state: str
    count: int


class ReportAggregatedStatusesData(BaseModel):
    data: list[ReportAggregatedStatuses]