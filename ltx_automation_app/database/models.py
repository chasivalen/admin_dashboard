# ltx_automation_app/database/models.py
"""
Database models for LTX Automation - Updated with optional fields for migration
"""

import reflex as rx
import sqlmodel
import sqlalchemy
from typing import Optional
from datetime import datetime


class ReadmeInstruction(rx.Model, table=True):
    """
    README Instruction model - matches Excel columns exactly
    """
    # Make required fields optional with defaults for migration
    README_TITLE: Optional[str] = sqlmodel.Field(default="", index=True)
    README_TXT: Optional[str] = sqlmodel.Field(default="", sa_column=sqlalchemy.Column(sqlalchemy.Text))
    
    # Optional fields that will be populated later via dropdowns
    SCORE_TYPE: Optional[str] = None
    EVAL_TYPE: Optional[str] = None
    PRE_EVAL_CONTEXT: Optional[str] = None
    CONTENT_TYPE: Optional[str] = None
    
    # Status and indicator fields
    STATUS_IND: Optional[str] = sqlmodel.Field(default="Active")
    DEFAULT_IND: Optional[str] = sqlmodel.Field(default="N")  # Y for default, N for custom
    CUSTOM_IND: Optional[str] = sqlmodel.Field(default="Y")   # Y for custom, N for default
    
    # Timestamps
    CREATE_DT: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "CREATE_DT",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    MODIFIED_DT: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "MODIFIED_DT",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )
    
    # Property to access id as README_ID for consistency
    @property
    def README_ID(self):
        return self.id


class Metric(rx.Model, table=True):
    """
    Metric model - matches Excel columns exactly
    """
    # Make required fields optional with defaults for migration
    METRIC_TYPE: Optional[str] = sqlmodel.Field(default="", index=True)
    METRIC_NAME: Optional[str] = sqlmodel.Field(default="", index=True)
    METRIC_DEF: Optional[str] = sqlmodel.Field(default="", sa_column=sqlalchemy.Column(sqlalchemy.Text))
    METRIC_NOTES: Optional[str] = sqlmodel.Field(default=None, sa_column=sqlalchemy.Column(sqlalchemy.Text))
    
    # Indicator fields for metric applicability
    GENAI_IND: Optional[str] = sqlmodel.Field(default="N")  # Y/N for GenAI applicability
    MT_LLM_IND: Optional[str] = sqlmodel.Field(default="N")  # Y/N for MT/LLM applicability
    
    # Type fields (to be populated via dropdowns later)
    SCORE_TYPE: Optional[str] = None
    EVAL_TYPE: Optional[str] = None
    EVAL_TYPE_DETAIL: Optional[str] = None
    CONTENT_TYPE: Optional[str] = None
    
    # Status field
    STATUS_IND: Optional[str] = sqlmodel.Field(default="Active")
    
    # Timestamps
    CREATE_DT: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "CREATE_DT",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    MODIFIED_DT: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "MODIFIED_DT",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )


# Keep existing models for app functionality
class Organization(rx.Model, table=True):
    """
    Organization model - stores organizations using the tool
    """
    name: Optional[str] = sqlmodel.Field(default="", index=True, unique=True)
    created_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "created_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )


class Project(rx.Model, table=True):
    """
    Project model - stores projects within organizations
    """
    name: Optional[str] = sqlmodel.Field(default="")
    description: Optional[str] = None
    organization_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="organization.id")
    created_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "created_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    updated_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "updated_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )


class Template(rx.Model, table=True):
    """
    Template model - stores evaluation templates
    """
    name: Optional[str] = sqlmodel.Field(default="")
    description: Optional[str] = None
    content: Optional[str] = None  # JSON string of template structure
    variables: Optional[str] = None  # JSON string of variables used
    created_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "created_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    updated_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "updated_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )


class Evaluation(rx.Model, table=True):
    """
    Evaluation model - stores evaluation configurations
    """
    name: Optional[str] = sqlmodel.Field(default="")
    project_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="project.id")
    evaluation_type: Optional[str] = sqlmodel.Field(default="Metrics")  # e.g., "Metrics", "README", "Both"
    status: Optional[str] = sqlmodel.Field(default="Draft")  # Draft, Active, Completed
    configuration: Optional[str] = None  # JSON string of evaluation config
    results: Optional[str] = None  # JSON string of evaluation results
    created_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "created_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    updated_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "updated_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )


class EvaluationMetric(rx.Model, table=True):
    """
    EvaluationMetric model - junction table linking evaluations to metrics
    """
    evaluation_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="evaluation.id")
    metric_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="metric.id")
    value: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "created_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )