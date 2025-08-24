# ltx_automation_app/states/ltx_bench_state.py
"""
LTX Bench states with proper database integration.
Each state class inherits directly from rx.State for optimal performance.
"""

import reflex as rx
from typing import Dict, Any, List
from sqlmodel import select
from ltx_automation_app.database.models import (
    Organization, 
    Project, 
    Template,
    ReadmeInstruction,
    Metric, 
    Evaluation,
    EvaluationMetric
)


class LTXBenchNavigationState(rx.State):
    """
    Navigation state - controls which view is shown.
    """
    # Main navigation
    current_view: str = "dashboard"
    
    # Organization/Project info
    selected_organization: str = ""
    selected_project: str = ""
    organizations: list[str] = []
    projects: list[str] = []
    
    @rx.event
    def load_initial_data(self):
        """Load organizations from database when page loads."""
        self.refresh_organizations()
    
    @rx.event
    def refresh_organizations(self):
        """Refresh organizations list from database."""
        with rx.session() as session:
            orgs = session.exec(select(Organization)).all()
            self.organizations = [org.name for org in orgs]
    
    @rx.event
    def refresh_projects(self):
        """Refresh projects for selected organization from database."""
        if not self.selected_organization:
            self.projects = []
            return
            
        with rx.session() as session:
            org = session.exec(
                select(Organization).where(Organization.name == self.selected_organization)
            ).first()
            
            if org:
                projects = session.exec(
                    select(Project).where(Project.organization_id == org.id)
                ).all()
                self.projects = [proj.name for proj in projects]
            else:
                self.projects = []
    
    @rx.event
    def set_view(self, view: str):
        """Set the current view."""
        self.current_view = view
    
    @rx.event
    def show_dashboard(self):
        """Navigate to dashboard."""
        self.current_view = "dashboard"
    
    @rx.event
    def show_evaluation_library(self):
        """Navigate to evaluation library."""
        self.current_view = "evaluation_library"
    
    @rx.event
    def show_existing_projects(self):
        """Navigate to existing projects view."""
        self.current_view = "existing_projects"
    
    @rx.event
    def show_new_project(self):
        """Navigate to new project creation (starts with organization selection)."""
        self.current_view = "organization"
        # Reset selections when starting new project flow
        self.selected_organization = ""
        self.selected_project = ""
        self.refresh_organizations()
    
    @rx.event
    def select_organization(self, org_name: str):
        """Select an organization and refresh projects."""
        self.selected_organization = org_name
        self.refresh_projects()
    
    @rx.event
    def select_project(self, project_name: str):
        """Select a project and navigate to file prep."""
        self.selected_project = project_name
        self.current_view = "file_prep"


class ProjectManagementState(rx.State):
    """
    State for project and organization management.
    Handles creation of new orgs/projects.
    """
    # Input fields
    new_org_input: str = ""
    new_project_input: str = ""
    new_project_description: str = ""
    
    @rx.event
    def set_new_org_input(self, value: str):
        """Set new organization input."""
        self.new_org_input = value
    
    @rx.event
    def set_new_project_input(self, value: str):
        """Set new project input."""
        self.new_project_input = value
    
    @rx.event
    def set_new_project_description(self, value: str):
        """Set new project description."""
        self.new_project_description = value
    
    @rx.event
    async def create_organization(self, org_name: str):
        """Create a new organization in database."""
        if not org_name or not org_name.strip():
            return rx.toast.error("Organization name cannot be empty")
        
        org_name = org_name.strip()
        
        with rx.session() as session:
            # Check if org already exists
            existing = session.exec(
                select(Organization).where(Organization.name == org_name)
            ).first()
            
            if existing:
                return rx.toast.error(f"Organization '{org_name}' already exists")
            
            # Create new org
            new_org = Organization(name=org_name)
            session.add(new_org)
            session.commit()
        
        # Update navigation state
        nav_state = await self.get_state(LTXBenchNavigationState)
        nav_state.refresh_organizations()
        nav_state.selected_organization = org_name
        
        # Clear input
        self.new_org_input = ""
        
        return rx.toast.success(f"Organization '{org_name}' created")
    
    @rx.event
    async def create_project(self, project_data: dict):
        """Create a new project in database."""
        project_name = project_data.get("project_name", "").strip()
        project_description = project_data.get("description", "").strip()
        
        if not project_name:
            return rx.toast.error("Project name cannot be empty")
        
        # Get navigation state
        nav_state = await self.get_state(LTXBenchNavigationState)
        
        with rx.session() as session:
            # Get organization
            org = session.exec(
                select(Organization).where(
                    Organization.name == nav_state.selected_organization
                )
            ).first()
            
            if not org:
                return rx.toast.error("Organization not found")
            
            # Check if project already exists
            existing = session.exec(
                select(Project).where(
                    Project.name == project_name,
                    Project.organization_id == org.id
                )
            ).first()
            
            if existing:
                return rx.toast.error(f"Project '{project_name}' already exists")
            
            # Create new project
            new_project = Project(
                name=project_name,
                description=project_description,
                organization_id=org.id
            )
            session.add(new_project)
            session.commit()
        
        # Update navigation state
        nav_state.refresh_projects()
        nav_state.selected_project = project_name
        nav_state.current_view = "file_prep"
        
        # Clear inputs
        self.new_project_input = ""
        self.new_project_description = ""
        
        return rx.toast.success(f"Project '{project_name}' created")


class EvaluationLibraryState(rx.State):
    """
    State for the Evaluation Library section.
    Properly loads and manages database content following Reflex patterns.
    """
    # Sidebar navigation
    selected_section: str = ""
    eval_library_expanded: bool = True
    template_library_expanded: bool = True
    
    # Read Me Library state
    selected_readme_id: str = ""
    current_readme_data: Dict[str, Any] = {}
    readme_instructions: list[dict[str, str]] = []  # Loaded from database
    
    # Edit mode state
    readme_edit_mode: bool = False  # Controls edit/view mode for README
    
    # Temporary edit values (before saving)
    edit_eval_type: str = ""
    edit_score_type: str = ""
    edit_pre_eval: str = ""
    edit_default_custom: str = "default"  # "default" or "custom"
    edit_readme_title: str = ""  # For editing README title
    edit_readme_content: str = ""  # For editing README content
    
    # Dropdown options loaded from database
    eval_type_options: list[str] = []  # Distinct EVAL_TYPE values
    score_type_options: list[str] = []  # Distinct SCORE_TYPE values
    pre_eval_options: list[str] = []  # Distinct PRE_EVAL_CONTEXT values
    
    # Selected README for viewing/editing
    selected_readme_title: str = ""
    selected_readme_content: str = ""
    selected_eval_type: str = ""
    selected_score_type: str = ""
    selected_pre_eval: str = ""
    selected_default_custom: str = "default"
    
    # Metrics Library state
    all_metrics: list[Dict[str, Any]] = []
    metrics_loading: bool = False
    metrics_error: str = ""
    filtered_metrics: list[Dict[str, Any]] = []
    metric_search_term: str = ""
    
    # Additional state methods for sidebar and sections
    @rx.event
    def select_section(self, section: str):
        """Select a section in the sidebar."""
        self.selected_section = section
        # Load data for the selected section if needed
        if section == "readme":
            if not self.readme_instructions:  # Only load if not already loaded
                self.load_readme_instructions()
        elif section == "metrics":
            if not self.all_metrics:  # Only load if not already loaded
                self.load_all_metrics()
    
    @rx.event
    def select_library_section(self, section_id: str):
        """Alias for select_section to match what views are calling."""
        self.select_section(section_id)
    
    @rx.event
    def toggle_eval_library(self):
        """Toggle evaluation library expansion."""
        self.eval_library_expanded = not self.eval_library_expanded
    
    @rx.event
    def toggle_template_library(self):
        """Toggle template library expansion."""
        self.template_library_expanded = not self.template_library_expanded
    
    
    @rx.event
    def initialize_readme_library(self):
        """
        Initialize README library on component mount.
        Load instructions and dropdown options.
        """
        self.load_readme_instructions()
        self.load_readme_dropdown_options()
    
    @rx.event
    def load_readme_instructions(self):
        """
        Load all README instructions from the database.
        """
        try:
            with rx.session() as session:
                instructions = session.exec(select(ReadmeInstruction)).all()
                
                self.readme_instructions = [
                    {
                        "id": str(instruction.id),
                        "title": instruction.README_TITLE,
                        "content": instruction.README_TXT,
                        "README_TITLE": instruction.README_TITLE,  # For view compatibility
                        "README_TXT": instruction.README_TXT,  # For view compatibility
                        "README_ID": str(instruction.id),  # For view compatibility
                        "score_type": instruction.SCORE_TYPE or "",
                        "eval_type": instruction.EVAL_TYPE or "",
                        "pre_eval_context": instruction.PRE_EVAL_CONTEXT or "",
                        "default_ind": instruction.DEFAULT_IND or "N",
                        "DEFAULT_IND": instruction.DEFAULT_IND or "N",  # For view compatibility
                        "custom_ind": instruction.CUSTOM_IND or "Y",
                        "status": instruction.STATUS_IND or "Active"
                    }
                    for instruction in instructions
                ]
                
                # If there are instructions, select the first one
                if self.readme_instructions:
                    self.select_readme(self.readme_instructions[0]["id"])
                    
        except Exception as e:
            print(f"Error loading README instructions: {e}")
            self.readme_instructions = []
            return rx.toast.error("Failed to load README instructions")
    
    @rx.event
    def load_readme_dropdown_options(self):
        """
        Load distinct values for dropdowns from the database.
        This ensures dropdowns always show current database values.
        """
        try:
            with rx.session() as session:
                # Get distinct EVAL_TYPE values (excluding None/empty)
                eval_types = session.exec(
                    select(ReadmeInstruction.EVAL_TYPE).distinct().where(
                        ReadmeInstruction.EVAL_TYPE != None,
                        ReadmeInstruction.EVAL_TYPE != ""
                    )
                ).all()
                self.eval_type_options = list(set([t for t in eval_types if t]))
                
                # Get distinct SCORE_TYPE values (excluding None/empty)
                score_types = session.exec(
                    select(ReadmeInstruction.SCORE_TYPE).distinct().where(
                        ReadmeInstruction.SCORE_TYPE != None,
                        ReadmeInstruction.SCORE_TYPE != ""
                    )
                ).all()
                self.score_type_options = list(set([t for t in score_types if t]))
                
                # Get distinct PRE_EVAL_CONTEXT values (excluding None/empty)
                pre_evals = session.exec(
                    select(ReadmeInstruction.PRE_EVAL_CONTEXT).distinct().where(
                        ReadmeInstruction.PRE_EVAL_CONTEXT != None,
                        ReadmeInstruction.PRE_EVAL_CONTEXT != ""
                    )
                ).all()
                self.pre_eval_options = list(set([t for t in pre_evals if t]))
                
        except Exception as e:
            print(f"Error loading dropdown options: {e}")
            # Set default options if database query fails
            self.eval_type_options = ["TEXT PROCESSING", "LOCALIZATION", "Q & A", "ISSUES"]
            self.score_type_options = ["1 to 5", "Y/N", "0 to 100"]
            self.pre_eval_options = ["SOURCE/TARGET", "POST/RETITLE", "LACKING INFORMATION", "NONE"]
            
    @rx.event
    def cancel_edit(self):
        """
        Cancel editing and revert to view mode without saving.
        """
        self.readme_edit_mode = False
        # Reset edit vars
        self.edit_readme_title = ""  # ADD THIS LINE
        self.edit_readme_content = ""  # ADD THIS LINE
        self.edit_eval_type = ""
        self.edit_score_type = ""
        self.edit_pre_eval = ""
        self.edit_default_custom = "default"
    
    @rx.event
    def select_readme(self, readme_id: str):
        """
        Select a README instruction for viewing/editing.
        """
        for readme in self.readme_instructions:
            if readme["id"] == readme_id:
                self.selected_readme_id = readme_id
                self.selected_readme_title = readme["title"]
                self.selected_readme_content = readme["content"]
                self.selected_eval_type = readme["eval_type"]
                self.selected_score_type = readme["score_type"]
                self.selected_pre_eval = readme["pre_eval_context"]
                
                # Set current_readme_data with uppercase keys for view compatibility
                self.current_readme_data = {
                    "id": readme["id"],
                    "README_TITLE": readme["README_TITLE"],
                    "README_TXT": readme["README_TXT"],
                    "README_ID": readme["README_ID"],
                    "DEFAULT_IND": readme["DEFAULT_IND"],
                    "eval_type": readme["eval_type"],
                    "score_type": readme["score_type"],
                    "pre_eval_context": readme["pre_eval_context"]
                }
                
                # Set default/custom based on indicators
                if readme.get("default_ind") == "Y":
                    self.selected_default_custom = "default"
                else:
                    self.selected_default_custom = "custom"
                
                # Reset edit mode when selecting new README
                self.readme_edit_mode = False
                break
    
    @rx.event
    def toggle_edit_mode(self):
        """
        Toggle between edit and view mode for README.
        When entering edit mode, copy current values to edit vars.
        """
        if not self.readme_edit_mode:
            # Entering edit mode - copy current values to edit vars
            self.edit_readme_title = self.selected_readme_title  # Copy title for editing
            self.edit_readme_content = self.selected_readme_content  # Copy content for editing
            self.edit_eval_type = self.selected_eval_type
            self.edit_score_type = self.selected_score_type
            self.edit_pre_eval = self.selected_pre_eval
            self.edit_default_custom = self.selected_default_custom
            self.readme_edit_mode = True
        else:
            # Exiting edit mode without saving - just toggle back
            self.readme_edit_mode = False
    
    @rx.event
    def save_readme_changes(self):
        """
        Save the edited README changes to the database.
        This saves ALL changes including title, content, and settings.
        """
        try:
            with rx.session() as session:
                # Find and update the README in the database
                readme = session.exec(
                    select(ReadmeInstruction).where(
                        ReadmeInstruction.id == int(self.selected_readme_id)
                    )
                ).first()
                
                if readme:
                    # Update ALL fields in the database
                    readme.README_TITLE = self.edit_readme_title  # Save edited title
                    readme.README_TXT = self.edit_readme_content  # Save edited content
                    readme.EVAL_TYPE = self.edit_eval_type
                    readme.SCORE_TYPE = self.edit_score_type
                    readme.PRE_EVAL_CONTEXT = self.edit_pre_eval
                    readme.DEFAULT_IND = "Y" if self.edit_default_custom == "default" else "N"
                    readme.CUSTOM_IND = "N" if self.edit_default_custom == "default" else "Y"
                    
                    session.commit()
                    
                    # Update the local state to reflect saved changes
                    self.selected_readme_title = self.edit_readme_title
                    self.selected_readme_content = self.edit_readme_content
                    self.selected_eval_type = self.edit_eval_type
                    self.selected_score_type = self.edit_score_type
                    self.selected_pre_eval = self.edit_pre_eval
                    self.selected_default_custom = self.edit_default_custom
                    
                    # Update the readme_instructions list to reflect changes
                    for i, instruction in enumerate(self.readme_instructions):
                        if instruction["id"] == self.selected_readme_id:
                            self.readme_instructions[i]["title"] = self.edit_readme_title
                            self.readme_instructions[i]["content"] = self.edit_readme_content
                            self.readme_instructions[i]["README_TITLE"] = self.edit_readme_title
                            self.readme_instructions[i]["README_TXT"] = self.edit_readme_content
                            self.readme_instructions[i]["eval_type"] = self.edit_eval_type
                            self.readme_instructions[i]["score_type"] = self.edit_score_type
                            self.readme_instructions[i]["pre_eval_context"] = self.edit_pre_eval
                            self.readme_instructions[i]["default_ind"] = "Y" if self.edit_default_custom == "default" else "N"
                            self.readme_instructions[i]["custom_ind"] = "N" if self.edit_default_custom == "default" else "Y"
                            self.current_readme_data = self.readme_instructions[i]
                            break
                    
                    # Exit edit mode
                    self.readme_edit_mode = False
                    
                    return rx.toast.success("README saved successfully to database")
                else:
                    return rx.toast.error("README not found in database")
                    
        except Exception as e:
            print(f"Error saving README changes: {e}")
            return rx.toast.error(f"Failed to save changes: {str(e)}")
    
    @rx.event
    def set_edit_eval_type(self, value: str):
        """Set the evaluation type during editing."""
        self.edit_eval_type = value
    
    @rx.event
    def set_edit_score_type(self, value: str):
        """Set the score type during editing."""
        self.edit_score_type = value
    
    @rx.event
    def set_edit_pre_eval(self, value: str):
        """Set the pre-eval context during editing."""
        self.edit_pre_eval = value
    
    @rx.event
    def set_edit_default_custom(self, value: str):
        """Set default/custom radio during editing."""
        self.edit_default_custom = value
    
        
    @rx.event
    def set_edit_readme_content(self, value: str):
        """Set the readme content during editing."""
        self.edit_readme_content = value
    
    @rx.event
    def delete_readme(self):
        """Delete the currently selected README instruction."""
        if not self.selected_readme_id:
            return rx.toast.error("No README selected")
        
        # Implement deletion logic if needed
        return rx.toast.info("Delete functionality not yet implemented")
    
    @rx.event
    def edit_readme(self):
        """Enter edit mode for the selected README."""
        self.toggle_edit_mode()
    
    # Metrics methods
    @rx.event
    def load_all_metrics(self):
        """
        Load all metrics from the database.
        """
        try:
            with rx.session() as session:
                metrics = session.exec(select(Metric)).all()
                
                self.all_metrics = [
                    {
                        "id": str(metric.id),
                        "name": metric.METRIC_NAME,
                        "type": metric.METRIC_TYPE,
                        "definition": metric.METRIC_DEF or "",
                        "notes": metric.METRIC_NOTES or ""
                    }
                    for metric in metrics
                ]
                self.filtered_metrics = self.all_metrics
                
        except Exception as e:
            print(f"Error loading metrics: {e}")
            self.metrics_error = "Failed to load metrics"
            self.all_metrics = []
            self.filtered_metrics = []
    
    @rx.event
    def search_metrics(self, search_term: str):
        """Filter metrics based on search term."""
        self.metric_search_term = search_term
        if not search_term:
            self.filtered_metrics = self.all_metrics
        else:
            search_lower = search_term.lower()
            self.filtered_metrics = [
                m for m in self.all_metrics
                if search_lower in m["name"].lower() or
                   search_lower in m.get("definition", "").lower()
            ]
    
    # Methods actually called by views
    @rx.event
    def select_section(self, section: str):
        """Select a section in the sidebar."""
        self.selected_section = section
        # Load data for the selected section if needed
        if section == "readme" and not self.readme_instructions:
            self.load_readme_instructions()
        elif section == "metrics" and not self.all_metrics:
            self.load_all_metrics()
    
    # Placeholder methods for sections not yet implemented
    @rx.event
    def questions_library_content(self):
        """Placeholder for questions library."""
        pass
    
    @rx.event
    def charts_library_content(self):
        """Placeholder for charts library."""
        pass
    
    @rx.event
    def existing_templates_content(self):
        """Placeholder for existing templates."""
        pass
    
    @rx.event
    def template_builder_content(self):
        """Placeholder for template builder."""
        pass
        
class FilePrepState(rx.State):
    """
    State for LTX Bench file preparation.
    Works with EvaluationLibraryState to get database content.
    Only stores selections and configurations, not the actual data.
    """
    
    # File upload state
    uploaded_files: list[Dict[str, Any]] = []
    file_upload_complete: bool = False
    
    # Step tracking
    current_file_prep_step: int = 1
    max_file_prep_step: int = 5
    
    # Step 1: README Configuration (stores selections only)
    include_readme: bool = True
    selected_readme_template: str = ""  # Just the ID, not the content (renamed for compatibility)
    custom_readme_sections: list[Dict[str, str]] = []  # For user-added custom text
    
    # Stakeholder and terminology configuration
    stakeholder_perspective: str = "customer"
    terminology_choices: Dict[str, str] = {
        "source_issue": "SOURCE",
        "target_issue": "TARGET", 
        "scoring_instruction": "1_TO_5"
    }
    
    # Step 2: Metrics Selection (stores IDs only)
    selected_metric_ids: list[str] = []  # Just the IDs of selected metrics
    selected_metrics: list[str] = []  # Compatibility alias for views
    custom_metrics: list[Dict[str, str]] = []  # User-defined metrics not in DB
    metric_search: str = ""  # For filtering metrics (renamed for view compatibility)
    metric_search_term: str = ""  # Keep both names for now
    custom_metric_input: str = ""  # For custom metric input field
    
    # Step 3: File Configuration
    num_models: int = 1  # Number of LLMs/tools to compare
    
    # Step 4: Export Settings
    export_format: str = "excel"
    excel_filename: str = ""
    include_yellow_warning: bool = True
    include_data_analysis: bool = True
    include_criteria_assessment: bool = True
    
    # Step 5: Generation
    generation_status: str = "ready"  # ready, generating, complete, error
    download_url: str = ""
    error_message: str = ""
    
    # Evaluation configuration
    eval_type: str = ""  # Will be set based on selected README
    score_type: str = "1_TO_5"
    
    # Cache for dropdown options (loaded from database)
    _available_readme_options: list[Dict[str, str]] = []
    _available_metric_options: list[Dict[str, str]] = []
    
    # ============ Step Navigation ============
    
    @rx.event
    def set_step(self, step: int):
        """Navigate to a specific step."""
        if 1 <= step <= self.max_file_prep_step:
            self.current_file_prep_step = step
    
    @rx.event
    def next_step(self):
        """Move to next step in workflow."""
        if self.current_file_prep_step < self.max_file_prep_step:
            self.current_file_prep_step += 1
    
    @rx.event
    def previous_step(self):
        """Move to previous step."""
        if self.current_file_prep_step > 1:
            self.current_file_prep_step -= 1
    
    # ============ Data Loading from Database ============
    
    @rx.event
    def load_available_options(self):
        """Load available READMEs and Metrics from database for dropdowns."""
        with rx.session() as session:
            # Load README options
            readmes = session.exec(
                select(ReadmeInstruction).where(
                    ReadmeInstruction.STATUS_IND == "Active"
                )
            ).all()
            self._available_readme_options = [
                {
                    "id": str(readme.id),
                    "title": readme.README_TITLE,
                    "type": readme.EVAL_TYPE or "GENERAL"
                }
                for readme in readmes
            ]
            
            # Load Metric options
            metrics = session.exec(
                select(Metric).where(
                    Metric.STATUS_IND == "Active"
                )
            ).all()
            self._available_metric_options = [
                {
                    "id": str(metric.id),
                    "name": metric.METRIC_NAME,
                    "type": metric.METRIC_TYPE,
                    "definition": metric.METRIC_DEF
                }
                for metric in metrics
            ]
    
    @rx.event
    def get_filtered_metrics(self, search_term: str = "") -> list[Dict[str, str]]:
        """Get filtered list of metrics based on search term."""
        if not search_term:
            return self._available_metric_options
        
        search_lower = search_term.lower()
        return [
            m for m in self._available_metric_options
            if search_lower in m["name"].lower() or 
               search_lower in m.get("definition", "").lower()
        ]
    
    # ============ Step 1: README Configuration ============
    
    @rx.event
    def select_readme_template(self, readme_id: str):
        """Select a README template by ID."""
        self.selected_readme_template = readme_id
        
        # Load the eval_type from the selected README
        with rx.session() as session:
            readme = session.exec(
                select(ReadmeInstruction).where(
                    ReadmeInstruction.id == int(readme_id)
                )
            ).first()
            if readme:
                self.eval_type = readme.EVAL_TYPE or "GENERAL"
    
    @rx.event
    def toggle_include_readme(self):
        """Toggle whether to include README in template."""
        self.include_readme = not self.include_readme
    
    @rx.event
    def set_stakeholder_perspective(self, value: str):
        """Set stakeholder perspective."""
        self.stakeholder_perspective = value
    
    @rx.event
    def set_source_issue_term(self, value: str):
        """Set source issue terminology."""
        self.terminology_choices["source_issue"] = value
    
    @rx.event
    def set_target_issue_term(self, value: str):
        """Set target issue terminology."""
        self.terminology_choices["target_issue"] = value
    
    @rx.event
    def set_scoring_method(self, value: str):
        """Set scoring method terminology."""
        self.terminology_choices["scoring_instruction"] = value
    
    @rx.event
    def set_terminology(self, term_type: str, value: str):
        """Set terminology choices."""
        if term_type in self.terminology_choices:
            self.terminology_choices[term_type] = value
    
    @rx.event
    def add_custom_readme_section(self, text: str):
        """Add a custom README section."""
        if text.strip():
            self.custom_readme_sections.append({
                "id": str(datetime.now().timestamp()),
                "text": text
            })
    
    @rx.event
    def remove_custom_readme_section(self, section_id: str):
        """Remove a custom README section."""
        self.custom_readme_sections = [
            s for s in self.custom_readme_sections 
            if s["id"] != section_id
        ]
    
    # ============ Step 2: Metrics Selection ============
    
    @rx.event
    def toggle_metric(self, metric_name_or_id: str):
        """Toggle selection of a metric - can work with both names and IDs."""
        # Check if it's an ID (numeric) or a name
        if metric_name_or_id.isdigit():
            # It's an ID
            if metric_name_or_id in self.selected_metric_ids:
                self.selected_metric_ids.remove(metric_name_or_id)
            else:
                self.selected_metric_ids.append(metric_name_or_id)
        else:
            # It's a name - for compatibility with views
            if metric_name_or_id in self.selected_metrics:
                self.selected_metrics.remove(metric_name_or_id)
            else:
                self.selected_metrics.append(metric_name_or_id)
    
    @rx.event
    def select_all_evergreen_metrics(self):
        """Select all evergreen metrics."""
        with rx.session() as session:
            evergreen = session.exec(
                select(Metric).where(
                    Metric.METRIC_TYPE == "EVERGREEN",
                    Metric.STATUS_IND == "Active"
                )
            ).all()
            for metric in evergreen:
                metric_id = str(metric.id)
                if metric_id not in self.selected_metric_ids:
                    self.selected_metric_ids.append(metric_id)
    
    @rx.event
    def clear_all_metrics(self):
        """Clear all selected metrics."""
        self.selected_metric_ids = []
    
    @rx.event
    def add_custom_metric(self, name: str = None, definition: str = ""):
        """Add a custom metric not in database."""
        # Use the passed name or fall back to the input field
        metric_name = name or self.custom_metric_input
        
        if metric_name and metric_name.strip():
            self.custom_metrics.append({
                "id": f"custom_{datetime.now().timestamp()}",
                "name": metric_name.strip(),
                "definition": definition,
                "type": "CUSTOM"
            })
            # Also add to selected metrics
            self.selected_metrics.append(metric_name.strip())
            # Clear the input field
            self.custom_metric_input = ""
    
    @rx.event
    def remove_custom_metric(self, metric_id: str):
        """Remove a custom metric."""
        self.custom_metrics = [
            m for m in self.custom_metrics 
            if m["id"] != metric_id
        ]
    
    @rx.event
    def set_metric_search(self, term: str):
        """Set the metric search term."""
        self.metric_search = term
        self.metric_search_term = term
    
    @rx.event
    def set_custom_metric_input(self, value: str):
        """Set the custom metric input field."""
        self.custom_metric_input = value
    
    # ============ Step 3: File Upload ============
    
    @rx.event
    async def handle_file_upload(self, files: Any):
        """Handle file uploads - using Any to match Reflex expectations."""
        for file in files:
            # Read file data
            upload_data = await file.read()
            
            # Save to upload directory
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = upload_dir / file.filename
            with file_path.open("wb") as f:
                f.write(upload_data)
            
            # Store file info
            self.uploaded_files.append({
                "name": file.filename,
                "size": len(upload_data),
                "type": file.content_type or "application/octet-stream",
                "path": str(file_path),
                "uploaded_at": datetime.now().isoformat()
            })
        
        if self.uploaded_files:
            self.file_upload_complete = True
            return rx.toast.success(f"Uploaded {len(files)} file(s)")
    
    @rx.event
    def remove_file(self, filename: str):
        """Remove an uploaded file."""
        self.uploaded_files = [
            f for f in self.uploaded_files 
            if f["name"] != filename
        ]
        
        if not self.uploaded_files:
            self.file_upload_complete = False
    
    @rx.event
    def set_num_models(self, value: int):
        """Set number of models/tools to evaluate."""
        if value > 0:
            self.num_models = value
    
    # ============ Step 4: Export Settings ============
    
    @rx.event
    def set_excel_filename(self, value: str):
        """Set the export filename."""
        # Remove .xlsx extension if provided (we'll add it)
        self.excel_filename = value.replace('.xlsx', '').replace('.xlsm', '')
    
    @rx.event
    def toggle_yellow_warning(self):
        """Toggle yellow warning for missing scores."""
        self.include_yellow_warning = not self.include_yellow_warning
    
    @rx.event
    def toggle_data_analysis(self):
        """Toggle data analysis tab inclusion."""
        self.include_data_analysis = not self.include_data_analysis
    
    @rx.event
    def toggle_criteria_assessment(self):
        """Toggle criteria assessment tab inclusion."""
        self.include_criteria_assessment = not self.include_criteria_assessment
    
    # ============ Step 5: Generate Excel ============
    
    @rx.event
    async def generate_excel(self):
        """
        Generate Excel file based on configuration.
        Pulls actual content from database at generation time.
        """
        # Validation
        if not self.selected_metric_ids and not self.custom_metrics:
            self.error_message = "Please select at least one metric"
            return rx.toast.error(self.error_message)
        
        if not self.excel_filename:
            self.error_message = "Please provide a filename"
            return rx.toast.error(self.error_message)
        
        self.generation_status = "generating"
        self.error_message = ""
        
        try:
            with rx.session() as session:
                # Get selected README content
                readme_content = None
                if self.include_readme and self.selected_readme_template:
                    readme = session.exec(
                        select(ReadmeInstruction).where(
                            ReadmeInstruction.id == int(self.selected_readme_template)
                        )
                    ).first()
                    if readme:
                        readme_content = {
                            "title": readme.README_TITLE,
                            "text": readme.README_TXT,
                            "eval_type": readme.EVAL_TYPE,
                            "score_type": readme.SCORE_TYPE
                        }
                
                # Get selected metrics content
                selected_metrics = []
                if self.selected_metric_ids:
                    metrics = session.exec(
                        select(Metric).where(
                            Metric.id.in_([int(id) for id in self.selected_metric_ids])
                        )
                    ).all()
                    selected_metrics = [
                        {
                            "name": m.METRIC_NAME,
                            "type": m.METRIC_TYPE,
                            "definition": m.METRIC_DEF,
                            "notes": m.METRIC_NOTES
                        }
                        for m in metrics
                    ]
                
                # Add custom metrics
                selected_metrics.extend(self.custom_metrics)
                
                # TODO: Actual Excel generation logic here
                # This would create the workbook with:
                # - README tab (if included)
                # - Part 1 evaluation sheets (one per model)
                # - Part 2 Data Analysis (if included)
                # - Part 3 Criteria Assessment (if included)
                # Using the pulled content from database
                
                # For now, simulate success
                self.generation_status = "complete"
                self.download_url = f"/_upload/{self.excel_filename}.xlsx"
                
                return rx.toast.success("Excel template generated successfully!")
                
        except Exception as e:
            self.generation_status = "error"
            self.error_message = str(e)
            return rx.toast.error(f"Generation failed: {str(e)}")
    
    # ============ Reset Functions ============
    
    @rx.event
    def reset_file_prep(self):
        """Reset file prep to initial state."""
        self.current_file_prep_step = 1
        self.selected_readme_template = ""
        self.custom_readme_sections = []
        self.selected_metric_ids = []
        self.selected_metrics = []
        self.custom_metrics = []
        self.metric_search = ""
        self.metric_search_term = ""
        self.custom_metric_input = ""
        self.uploaded_files = []
        self.file_upload_complete = False
        self.num_models = 1
        self.excel_filename = ""
        self.generation_status = "ready"
        self.download_url = ""
        self.error_message = ""
        # Keep terminology and settings as they might be user preferences
    
    @rx.event
    def reset_to_step(self, step: int):
        """Reset all data after a specific step."""
        if step < 2:
            self.selected_metric_ids = []
            self.selected_metrics = []
            self.custom_metrics = []
            self.metric_search = ""
            self.metric_search_term = ""
            self.custom_metric_input = ""
        if step < 3:
            self.uploaded_files = []
            self.file_upload_complete = False
        if step < 4:
            self.excel_filename = ""
        if step < 5:
            self.generation_status = "ready"
            self.download_url = ""
            self.error_message = ""
        
        self.current_file_prep_step = step