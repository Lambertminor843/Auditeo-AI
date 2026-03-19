"""
Audit Flow
"""

from crewai import Flow
from crewai.flow.flow import listen, router, start
from pydantic import BaseModel

from auditeo_ai.models import FactualMetrics


class AuditFlowState(BaseModel):
    """
    Audit Flow State
    """
    url: str
    factual_metrics: FactualMetrics | None = None


class AuditFlow(Flow[AuditFlowState]):
    """
    Audit Flow
    """
    
    @start()
    def scraping(self) -> str:
        """
        Scrape the page
        """
        return self.state.url