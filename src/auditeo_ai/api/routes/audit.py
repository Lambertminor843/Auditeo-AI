import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from auditeo_ai.flows.audit_flow import AuditFlow
from auditeo_ai.models import (
    APIResponse,
    AuditRunRequest,
    AuditRunResponse,
    ExecutionContext,
    ExecutionStatus,
)
from auditeo_ai.utils import flow_loop_executor, get_logger

router = APIRouter(tags=["audit"])
logger = get_logger("auditeo-ai:api")


def _execute_audit_flow(
    inputs: dict[str, Any],
) -> APIResponse:
    """
    Execute the audit flow synchronously.

    Args:
        inputs: The inputs for the audit flow

    Returns:
        APIResponse
    """

    try:
        flow = AuditFlow()
        inputs["execution_context"] = ExecutionContext(
            id=str(uuid.uuid4()),
            status=ExecutionStatus.PENDING,
            start_time=datetime.now(),
        )
        flow.kickoff(inputs=inputs)
        data = AuditRunResponse(
            website_url=flow.state.website_url,
            factual_metrics=flow.state.factual_metrics,
            kpis=flow.state.insights_crew_output.kpis,
            insights_report=flow.state.insights_crew_output.structured_report,
            recommendations=(
                flow.state.recommendations_crew_output.recommendations
                if flow.state.recommendations_crew_output
                else None
            ),
        )
        flow.state.execution_context.status = ExecutionStatus.COMPLETED
        flow.state.execution_context.end_time = datetime.now()
        trace_id = logger.info("Audit flow executed successfully")
        return APIResponse(
            success=True,
            trace_id=trace_id,
            message="Audit flow executed successfully",
            data=data,
            execution_context=flow.state.execution_context,
        )

    except Exception as e:
        trace_id = logger.error(f"Audit flow failed: \n{e}", exc_info=True)
        flow.state.execution_context.status = ExecutionStatus.FAILED
        flow.state.execution_context.end_time = datetime.now()
        return APIResponse(
            success=False,
            trace_id=trace_id,
            message="Audit flow execution failed",
            data=None,
        )


@router.post("/audit", response_model=APIResponse)
async def run_audit(payload: AuditRunRequest) -> APIResponse:

    inputs = {"website_url": payload.website_url}

    response = await flow_loop_executor(_execute_audit_flow, inputs)

    if not response.success:
        raise HTTPException(status_code=500, detail=response.model_dump())

    return response
