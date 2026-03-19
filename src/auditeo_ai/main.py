"""
Auditeo AI Main Entry Point.

This module provides the main entry point for running the Auditeo AI API server.
"""

import sys

import uvicorn

from auditeo_ai.api.app import app

__all__ = ["app", "main"]


def main() -> int:
    """Run the Auditeo AI API server."""
    uvicorn.run(
        "auditeo_ai.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
