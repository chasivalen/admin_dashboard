import reflex as rx
from typing import Dict
from ltx_automation_app.states.ltx_bench_state import LTXBenchState


def project_list_view() -> rx.Component:
    """
    Project list view showing all projects for the selected organization.
    Currently a placeholder - full implementation coming soon.
    """
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h1(
                "Project List",
                class_name="text-3xl font-bold text-gray-800 mb-4 text-center",
            ),
            
            # Add new project button - navigate back to project creation
            rx.el.div(
                rx.el.button(
                    rx.icon("plus", size=20),
                    on_click=LTXBenchState.reset_to_project_creation,
                    class_name="w-12 h-12 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center justify-center transition-colors",
                ),
                class_name="flex justify-center mb-8",
            ),
        ),
        
        # Project cards
        rx.el.div(
            rx.cond(
                LTXBenchState.projects.length() > 0,
                rx.el.div(
                    rx.foreach(
                        LTXBenchState.projects,
                        lambda project_name: project_card({
                            "name": project_name,
                            "description": LTXBenchState.project_descriptions.get(project_name, "")
                        }),
                    ),
                    class_name="space-y-4",
                ),
                rx.el.p(
                    "No projects yet. Click + to create your first project!",
                    class_name="text-gray-500 text-center italic",
                ),
            ),
            class_name="max-w-4xl mx-auto",
        ),
    )


def project_card(project: Dict[str, str]) -> rx.Component:
    """
    Individual project card component.
    
    Args:
        project: Dict with 'name' and 'description' keys
    """
    return rx.el.div(
        rx.el.div(
            # Organization badge
            rx.el.span(
                "Org: " + LTXBenchState.selected_organization,
                class_name="px-3 py-1 bg-gray-200 rounded text-xs font-medium text-gray-600 inline-block mb-3",
            ),
            
            # Project name
            rx.el.h3(
                project["name"],
                class_name="text-xl font-semibold text-gray-800 mb-2",
            ),
            
            # Project description
            rx.cond(
                project["description"] != "",
                rx.el.p(
                    project["description"],
                    class_name="text-gray-600 text-sm",
                ),
                rx.el.p(
                    "No description provided",
                    class_name="text-gray-400 text-sm italic",
                ),
            ),
            
            class_name="block",
        ),
        on_click=lambda: LTXBenchState.select_project(project["name"]),
        class_name="p-6 bg-white rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-lg transition-all cursor-pointer",
    )