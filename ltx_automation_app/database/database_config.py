# File: ltx_automation_app/database/database_config.py
"""
Database helper functions for LTX Automation
Uses rx.session() for all database operations per Reflex patterns
NO STATIC FILE IMPORTS - All data comes from database
"""

import reflex as rx
from sqlmodel import select
from pathlib import Path
import json

# Import models
from .models import (
    Organization, Project, Template, ReadmeInstruction, 
    Metric, Evaluation, EvaluationMetric
)

# NO MORE STATIC FILE IMPORTS! 


def seed_database():
    """
    Create default organization if it doesn't exist.
    No longer seeds from static files - data comes from Excel migration.
    """
    with rx.session() as session:
        # Just ensure a default organization exists
        existing_org = session.exec(
            select(Organization).where(Organization.name == "Default Organization")
        ).first()
        
        if not existing_org:
            default_org = Organization(name="Default Organization")
            session.add(default_org)
            session.commit()
            print("Created Default Organization")
        
        # Check if we have data from the Excel migration
        readme_count = session.exec(select(ReadmeInstruction)).first()
        metric_count = session.exec(select(Metric)).first()
        
        if readme_count:
            print(f"Database has README instructions from Excel migration")
        if metric_count:
            print(f"Database has Metrics from Excel migration")
        
        if not readme_count and not metric_count:
            print("WARNING: No data found in database. Run your Excel migration script.")


# Helper functions using rx.session() - these should be called from State event handlers
def get_all_organizations():
    """
    Get all organizations from database.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(select(Organization)).all()


def get_organization_projects(org_id: int):
    """
    Get all projects for a specific organization.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(
            select(Project).where(Project.organization_id == org_id)
        ).all()


def get_all_metrics(metric_type: str = None, metric_focus: str = None):
    """
    Get metrics from database with optional filtering.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        query = select(Metric)
        
        if metric_type:
            query = query.where(Metric.METRIC_TYPE == metric_type)
        
        if metric_focus:
            query = query.where(Metric.METRIC_FOCUS == metric_focus)
        
        return session.exec(query).all()


def get_evergreen_metrics():
    """
    Get only evergreen (default) metrics.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(
            select(Metric).where(Metric.DEFAULT_IND == "Y")
        ).all()


def get_custom_metrics():
    """
    Get only custom metrics.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(
            select(Metric).where(Metric.CUSTOM_IND == "Y")
        ).all()


def get_all_templates():
    """
    Get all templates.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(select(Template)).all()


def get_all_readme_instructions(active_only: bool = True):
    """
    Get all README instructions from database.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        query = select(ReadmeInstruction)
        
        if active_only:
            query = query.where(ReadmeInstruction.STATUS_IND == "Active")
        
        # Order by id or any order field you have
        return session.exec(query).all()


def get_readme_by_title(title: str):
    """
    Get a specific README instruction by title.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(
            select(ReadmeInstruction).where(ReadmeInstruction.README_TITLE == title)
        ).first()


def get_metric_by_name(name: str):
    """
    Get a specific metric by name.
    Should be called from within a State event handler.
    """
    with rx.session() as session:
        return session.exec(
            select(Metric).where(Metric.METRIC_NAME == name)
        ).first()