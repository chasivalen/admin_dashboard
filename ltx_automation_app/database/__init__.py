# File: ltx_automation_app/database/__init__.py
"""
Database package initialization for LTX Automation
Exports all models and database utilities
"""

from .models import (
    Organization,
    Project,
    Template,
    ReadmeInstruction,
    Metric,
    Evaluation,
    EvaluationMetric
)

from .database_config import (
    seed_database,
    get_all_organizations,
    get_organization_projects,
    get_all_metrics,
    get_evergreen_metrics,
    get_custom_metrics,  # Added this since it's in the updated database_config
    get_all_templates,
    get_all_readme_instructions,  # Changed from get_all_instructions
    get_readme_by_title,  # Added these new functions too
    get_metric_by_name    # Added these new functions too
)

# Initialize database on import
# This ensures tables are created and seeded when the app starts
# Removed since we don't have db_config instance anymore

__all__ = [
    # Models
    "Organization",
    "Project", 
    "Template",
    "ReadmeInstruction",
    "Metric",
    "Evaluation",
    "EvaluationMetric",
    
    # Database utilities
    "seed_database",
    "get_all_organizations",
    "get_organization_projects",
    "get_all_metrics",
    "get_evergreen_metrics",
    "get_custom_metrics",
    "get_all_templates",
    "get_all_readme_instructions",
    "get_readme_by_title",
    "get_metric_by_name"
]