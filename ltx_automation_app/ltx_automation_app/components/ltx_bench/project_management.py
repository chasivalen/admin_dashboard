# ltx_automation_app/components/ltx_bench/project_management.py
"""
Updated project creation and selection using new state structure.
Simplified and cleaned.
"""

import reflex as rx
from ltx_automation_app.states.ltx_bench_state import (
    LTXBenchNavigationState,
    ProjectManagementState
)


def project_creation_and_selection_view() -> rx.Component:
    """Main view for creating new projects and selecting existing ones"""
    return rx.el.div(
        # Organization badge showing current org
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Organization:",
                    class_name="text-sm text-gray-600 mr-2",
                ),
                rx.el.span(
                    LTXBenchNavigationState.selected_organization,
                    class_name="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium text-gray-700",
                ),
                rx.el.button(
                    rx.icon(
                        "arrow-left-right",
                        class_name="w-4 h-4",
                    ),
                    "Switch Organization",
                    on_click=switch_organization_handler,
                    class_name="ml-4 text-sm text-indigo-600 hover:text-indigo-700 font-medium",
                ),
                class_name="flex items-center",
            ),
            class_name="mb-6 p-4 bg-white rounded-lg shadow border border-gray-200",
        ),
        
        # Create new project section
        rx.el.div(
            rx.el.h2(
                "Create New Project",
                class_name="text-lg font-semibold text-gray-700 mb-3",
            ),
            rx.el.form(
                rx.el.input(
                    placeholder="Project name...",
                    name="project_name",
                    class_name="w-full px-3 py-2.5 rounded-lg border border-gray-300 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 mb-3 text-sm",
                ),
                rx.el.textarea(
                    placeholder="Project description...",
                    name="description",
                    rows=3,
                    class_name="w-full px-3 py-2.5 rounded-lg border border-gray-300 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 mb-3 text-sm",
                ),
                rx.el.button(
                    rx.icon(
                        "circle-plus",
                        class_name="w-4 h-4 mr-2",
                    ),
                    "Create Project",
                    type="submit",
                    class_name="w-full flex items-center justify-center bg-indigo-600 text-white py-2.5 px-4 rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium",
                ),
                on_submit=ProjectManagementState.create_project,
                reset_on_submit=True,
                class_name="p-4 bg-white rounded-xl shadow border border-gray-200",
            ),
        ),
        
        # Select existing project section
        rx.el.div(
            rx.el.h2(
                "Select Existing Project",
                class_name="text-lg font-semibold text-gray-700 mt-6 mb-3",
            ),
            rx.el.div(
                rx.cond(
                    LTXBenchNavigationState.projects.length() == 0,
                    rx.el.p(
                        "No projects yet. Create one above to begin!",
                        class_name="text-sm text-gray-500 italic p-3 text-center",
                    ),
                    rx.foreach(
                        LTXBenchNavigationState.projects,
                        project_selector_button,
                    ),
                ),
                class_name="space-y-2 p-4 bg-white rounded-xl shadow border border-gray-200 max-h-[calc(100vh-520px)] overflow-y-auto",
            ),
        ),
        
        class_name="max-w-2xl mx-auto space-y-6",
    )


def project_selector_button(project_name: str) -> rx.Component:
    """Individual project button with description"""
    return rx.el.button(
        rx.el.div(
            # Organization badge
            rx.el.div(
                rx.el.span(
                    "Org: " + LTXBenchNavigationState.selected_organization,
                    class_name="px-2 py-1 bg-gray-100 rounded text-xs font-medium text-gray-600",
                ),
                class_name="mb-2",
            ),
            # Project name
            rx.el.div(
                project_name,
                class_name="text-lg font-semibold text-gray-800",
            ),
            # Project description
            rx.cond(
                ProjectManagementState.project_descriptions.get(project_name, ""),
                rx.el.p(
                    ProjectManagementState.project_descriptions.get(project_name, ""),
                    class_name="text-sm text-gray-600 mt-1",
                ),
            ),
            class_name="text-left",
        ),
        on_click=lambda: select_project_handler(project_name),
        class_name=rx.cond(
            LTXBenchNavigationState.selected_project == project_name,
            "w-full text-left py-4 px-4 rounded-lg bg-indigo-100 text-indigo-700 border border-indigo-300 font-semibold shadow-sm transition-all",
            "w-full text-left py-4 px-4 rounded-lg bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 hover:border-gray-400 transition-all",
        ),
    )


async def select_project_handler(project_name: str):
    """Handle project selection"""
    nav_state = await rx.get_state(LTXBenchNavigationState)
    nav_state.selected_project = project_name
    nav_state.current_view = "file_prep"
    
    return rx.toast.info(f"Selected project: {project_name}", duration=2000)


async def switch_organization_handler():
    """Switch back to organization selection"""
    nav_state = await rx.get_state(LTXBenchNavigationState)
    nav_state.current_view = "organization"
    nav_state.selected_project = ""


# ============ CLEANUP NOTES ============
"""
CLEANED UP:
1. Uses new split state structure
2. Simplified event handlers
3. Cleaner async state communication
4. Removed redundant navigation flags

REMOVED:
- Old combined state references
- Complex navigation logic
- Unnecessary state variables
"""