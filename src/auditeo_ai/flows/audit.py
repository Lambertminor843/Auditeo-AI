"""
Audit Flow
"""

from pydantic import BaseModel

class AuditFlowState(BaseModel):
    """
    Audit Flow State
    """
    url: str
    website_content: str
    website_structure: str
    website_performance: str
    website_security: str
    website_seo: str
    website_accessibility: str
    website_usability: str
    website_engagement: str
    website_conversion: str
    website_monetization: str
    website_analytics: str