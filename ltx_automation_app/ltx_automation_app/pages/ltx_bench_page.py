# ltx_automation_app/pages/ltx_bench_page.py
"""
Updated LTX Bench page with new dashboard navigation.
Uses refactored states for better performance.
"""

import reflex as rx
from ltx_automation_app.states.ltx_bench_state import (
    LTXBenchNavigationState, 
    FilePrepState,
    ProjectManagementState
)
from ltx_automation_app.components.ltx_bench.dashboard.ltx_bench_dashboard import ltx_bench_dashboard
from ltx_automation_app.components.ltx_bench.evaluation_library.evaluation_library_view import evaluation_library_view
from ltx_automation_app.components.ltx_bench.organization_selection import organization_selection_view
from ltx_automation_app.components.ltx_bench.project_management import project_creation_and_selection_view
from ltx_automation_app.components.ltx_bench.file_prep_view import file_prep_view


def ltx_bench_page() -> rx.Component:
    """
    Main LTX Bench page with dashboard as entry point.
    Uses state-based navigation for clean single-page experience.
    """
    return rx.el.div(
        # Main navigation based on current_view
        rx.cond(
            LTXBenchNavigationState.current_view == "dashboard",
            ltx_bench_dashboard(),
            
            rx.cond(
                LTXBenchNavigationState.current_view == "evaluation_library",
                evaluation_library_view(),
                
                rx.cond(
                    LTXBenchNavigationState.current_view == "existing_projects",
                    existing_projects_view(),  # Placeholder for now
                    
                    rx.cond(
                        LTXBenchNavigationState.current_view == "organization",
                        organization_flow_container(),
                        
                        rx.cond(
                            LTXBenchNavigationState.current_view == "file_prep",
                            file_prep_container(),
                            
                            # Default fallback
                            ltx_bench_dashboard()
                        )
                    )
                )
            )
        ),
        
        class_name="min-h-screen bg-gray-50 font-sans"
    )


def organization_flow_container() -> rx.Component:
    """
    Container for organization/project creation flow.
    Handles the New Project path from dashboard.
    """
    return rx.el.div(
        # Show org selection if no org selected
        rx.cond(
            LTXBenchNavigationState.selected_organization == "",
            organization_selection_view_updated(),
            
            # Otherwise show project creation/selection
            project_creation_and_selection_view_updated()
        ),
        
        class_name="container mx-auto p-8"
    )


def file_prep_container() -> rx.Component:
    """
    Container for file prep workflow.
    Uses FilePrepState which loads on demand.
    """
    return rx.el.div(
        # Back to dashboard link
        rx.el.button(
            rx.icon("home", class_name="w-5 h-5 mr-2"),
            "Dashboard",
            on_click=LTXBenchNavigationState.show_dashboard,
            class_name="mb-4 flex items-center text-indigo-600 hover:text-indigo-700"
        ),
        
        # File prep component
        file_prep_view(),
        
        class_name="container mx-auto p-8"
    )


def existing_projects_view() -> rx.Component:
    """
    Placeholder for existing projects view.
    Will show list of projects to continue working on.
    """
    return rx.el.div(
        # Back button
        rx.el.button(
            rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
            "Back to Dashboard",
            on_click=LTXBenchNavigationState.show_dashboard,
            class_name="mb-6 flex items-center text-indigo-600 hover:text-indigo-700"
        ),
        
        rx.el.h1(
            "Existing Projects",
            class_name="text-3xl font-bold text-gray-800 mb-8 text-center"
        ),
        
        rx.el.div(
            rx.el.p(
                "Coming soon…",
                class_name="text-gray-500 text-xl italic text-center py-16"
            ),
            class_name="bg-white rounded-lg shadow border border-gray-200 max-w-4xl mx-auto"
        ),
        
        class_name="container mx-auto p-8"
    )


# Updated organization selection to work with new state
def organization_selection_view_updated() -> rx.Component:
    """
    Updated org selection to use ProjectManagementState.
    """
    return rx.el.div(
        # Back to dashboard
        rx.el.button(
            rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
            "Back to Dashboard",
            on_click=LTXBenchNavigationState.show_dashboard,
            class_name="mb-6 flex items-center text-indigo-600 hover:text-indigo-700"
        ),
        
        rx.el.h2(
            "Select Organization",
            class_name="text-2xl font-semibold text-gray-700 mb-6 text-center",
        ),
        
        # Rest of the organization selection UI...
        # (Using existing organization_selection_view code but with new state references)
        rx.el.div(
            # Create new organization section
            rx.el.div(
                rx.el.h3("Create New Organization", class_name="text-lg font-semibold mb-3"),
                rx.el.input(
                    placeholder="Enter organization name...",
                    value=ProjectManagementState.new_org_input,
                    on_change=ProjectManagementState.set_new_org_input,
                    class_name="w-full px-3 py-2 border rounded-lg mb-3"
                ),
                rx.el.button(
                    "Create Organization",
                    on_click=lambda: ProjectManagementState.create_organization(
                        ProjectManagementState.new_org_input
                    ),
                    class_name="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700"
                ),
                class_name="bg-white p-4 rounded-lg shadow mb-6"
            ),
            class_name="max-w-md mx-auto"
        )
    )


def project_creation_and_selection_view_updated() -> rx.Component:
    """
    Updated project view to navigate to file prep after creation.
    """
    # Similar updates for project creation...
    return rx.el.div(
        rx.el.h2("Create or Select Project", class_name="text-2xl font-bold text-center mb-6"),
        # Implementation continues...
        class_name="max-w-2xl mx-auto"
    )


# ============ MIGRATION NOTES ============
"""
MIGRATION SUMMARY:
1. Dashboard is now the entry point
2. Navigation uses LTXBenchNavigationState.current_view
3. Each major section loads its own state on demand
4. File prep uses FilePrepState (loaded only when needed)
5. Organization/Project uses ProjectManagementState

BENEFITS:
- Dashboard loads instantly (minimal state)
- File prep state doesn't slow down navigation
- Evaluation library loads separately
- Better performance and UX

TODO:
1. Update existing components to use new states
2. Implement state communication where needed
3. Add proper back navigation throughout
"""