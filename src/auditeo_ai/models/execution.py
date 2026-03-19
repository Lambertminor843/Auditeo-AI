from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ExecutionStatus(StrEnum):
    """
    Execution status
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionContext(BaseModel):
    """
    Execution context model
    """

    id: str | None = Field(default=None, description="The ID of the execution")
    total_token_usage: int = Field(
        default=0, ge=0, description="The total token usage of the execution"
    )
    start_time: datetime = Field(
        default=None, description="The start time of the execution"
    )
    end_time: datetime = Field(
        default=None, description="The end time of the execution"
    )
    status: ExecutionStatus = Field(
        default=ExecutionStatus.PENDING, description="The status of the execution"
    )
