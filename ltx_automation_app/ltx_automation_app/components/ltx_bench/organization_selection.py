# ltx_automation_app/components/ltx_bench/organization_selection.py
"""
Updated organization selection using new state structure.
Cleaned and simplified.
"""

import reflex as rx
from ltx_automation_app.states.ltx_bench_state import (
    LTXBenchNavigationState,
    ProjectManagementState
)


def organization_selection_view() -> rx.Component:
    """Organization selection page - cleaned version"""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Select Organization",
                class_name="text-2xl font-semibold text-gray-700 mb-6",
            ),
            
            # Create new organization
            rx.el.div(
                rx.el.h3(
                    "Create New Organization",
                    class_name="text-lg font-semibold text-gray-700 mb-3",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Enter organization name...",
                        value=ProjectManagementState.new_org_input,
                        on_change=ProjectManagementState.set_new_org_input,
                        class_name="w-full px-3 py-2.5 rounded-lg border border-gray-300 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 mb-3 text-sm",
                    ),
                    rx.el.button(
                        rx.icon(
                            "building",
                            class_name="w-4 h-4 mr-2",
                        ),
                        "Create Organization",
                        on_click=lambda: ProjectManagementState.create_organization(
                            ProjectManagementState.new_org_input
                        ),
                        class_name="w-full flex items-center justify-center bg-indigo-600 text-white py-2.5 px-4 rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium",
                    ),
                    class_name="p-4 bg-white rounded-xl shadow border border-gray-200",
                ),
            ),
            
            # Select existing organization
            rx.el.div(
                rx.el.h3(
                    "Select Existing Organization",
                    class_name="text-lg font-semibold text-gray-700 mt-6 mb-3",
                ),
                rx.el.div(
                    rx.cond(
                        LTXBenchNavigationState.organizations.length() == 0,
                        rx.el.p(
                            "No organizations yet. Create one above to begin!",
                            class_name="text-sm text-gray-500 italic p-3 text-center",
                        ),
                        rx.foreach(
                            LTXBenchNavigationState.organizations,
                            lambda org: organization_button(org),
                        ),
                    ),
                    class_name="space-y-2 p-4 bg-white rounded-xl shadow border border-gray-200 max-h-[calc(100vh-420px)] overflow-y-auto",
                ),
            ),
        ),
        class_name="max-w-md mx-auto space-y-6",
    )


def organization_button(org_name: str) -> rx.Component:
    """Individual organization selection button"""
    return rx.el.button(
        rx.el.div(
            rx.icon(
                "building",
                class_name="w-5 h-5 text-gray-600",
            ),
            rx.el.span(
                org_name,
                class_name="font-medium",
            ),
            class_name="flex items-center space-x-3",
        ),
        on_click=lambda: select_organization_handler(org_name),
        class_name="w-full text-left py-3 px-4 rounded-lg bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 hover:border-gray-400 transition-all",
    )


async def select_organization_handler(org_name: str):
    """Handler for organization selection"""
    # Update navigation state
    nav_state = await rx.get_state(LTXBenchNavigationState)
    nav_state.selected_organization = org_name
    nav_state.current_view = "projects"
    
    # Clear project management input
    mgmt_state = await rx.get_state(ProjectManagementState)
    mgmt_state.new_org_input = ""


# ============ CLEANUP NOTES ============
"""
CLEANED UP:
1. Removed old LTXBenchState references
2. Uses ProjectManagementState for inputs
3. Uses LTXBenchNavigationState for navigation
4. Simplified handler functions
5. Cleaner async state updates

REMOVED:
- Complex state management from single state
- Unnecessary navigation flags
- Redundant methods
"""