# ltx_automation_app/components/ltx_bench/dashboard/ltx_bench_dashboard.py
"""
Main dashboard for LTX Bench feature with sidebar navigation.
Features minimal sidebar and dismissible instructions dialog.
"""

import reflex as rx
from ltx_automation_app.states.ltx_bench_state import LTXBenchNavigationState


def ltx_bench_dashboard() -> rx.Component:
    """
    Dashboard with sidebar navigation and instructions dialog.
    Clean, minimal design with clear navigation options.
    """
    return rx.el.div(
        # Back arrow to main app
        rx.el.a(
            rx.icon("arrow-left", class_name="w-6 h-6 text-indigo-600"),
            href="/",
            class_name="absolute top-8 left-8 p-2 rounded-full hover:bg-gray-100 transition-colors z-10",
        ),
        
        # Main container with sidebar and content
        rx.el.div(
            # Left sidebar with navigation
            sidebar_navigation(),
            
            # Main content area
            rx.el.div(
                # Title
                rx.el.h1(
                    "LTX Bench Dashboard",
                    class_name="text-3xl font-bold text-gray-800 mb-8"
                ),
                
                # Show Instructions button/dialog
                instructions_dialog(),
                
                class_name="flex-1 p-8"
            ),
            
            class_name="flex min-h-screen"
        ),
        
        class_name="bg-gray-50"
    )


def sidebar_navigation() -> rx.Component:
    """
    Minimal sidebar with just the navigation buttons.
    Matches the mockup design.
    """
    return rx.el.div(
        rx.el.div(
            # Evaluation Library button
            sidebar_button(
                icon_name="library",
                title="Evaluation Library",
                on_click=LTXBenchNavigationState.show_evaluation_library,
            ),
            
            # Existing Projects button
            sidebar_button(
                icon_name="folder-open",
                title="Existing Projects",
                on_click=LTXBenchNavigationState.show_existing_projects,
            ),
            
            # New Project button
            sidebar_button(
                icon_name="folder-plus",
                title="New Project",
                on_click=LTXBenchNavigationState.show_new_project,
            ),
            
            class_name="space-y-4"
        ),
        
        class_name="w-48 p-6 bg-white border-r border-gray-200"
    )


def sidebar_button(icon_name: str, title: str, on_click) -> rx.Component:
    """
    Individual sidebar button with icon and text.
    Minimal design with hover effect.
    """
    return rx.el.button(
        rx.el.div(
            # Icon
            rx.icon(
                icon_name,
                class_name="w-6 h-6 text-indigo-600 mb-2"
            ),
            
            # Title
            rx.el.span(
                title,
                class_name="text-sm font-medium text-gray-700"
            ),
            
            class_name="flex flex-col items-center"
        ),
        
        on_click=on_click,
        class_name="w-full p-4 rounded-lg hover:bg-gray-50 transition-colors"
    )


def instructions_dialog() -> rx.Component:
    """
    Dialog component for instructions.
    Shows "Show Instructions" button that opens a dialog with full instructions.
    """
    return rx.dialog.root(
        # Trigger button
        rx.dialog.trigger(
            rx.el.button(
                "Show Instructions",
                class_name="px-4 py-2 text-indigo-600 hover:text-indigo-700 font-medium"
            ),
        ),
        
        # Dialog content
        rx.dialog.content(
            # Header
            rx.dialog.title(
                "Instructions for Use:",
                class_name="text-lg font-semibold text-gray-800"
            ),
            
            # Instructions content
            rx.el.div(
                rx.el.p(
                    "Select from the sidebar, to get started.",
                    class_name="text-gray-700 mb-3"
                ),
                rx.el.p(
                    "The Evaluation Library allows users to review and modify evaluation components such as metrics, read me instructions, etc.",
                    class_name="text-gray-600 mb-3"
                ),
                rx.el.p(
                    "If you select an existing project, you can pick up where you left off on a prior project or move from file prep to final report, etc.",
                    class_name="text-gray-600 mb-3"
                ),
                rx.el.p(
                    "Creating a new project will allow you to use a previously saved project template or build a new project using stored components from the Evaluation Library to file prep for a new project.",
                    class_name="text-gray-600"
                ),
                class_name="py-4"
            ),
            
            # Close button
            rx.dialog.close(
                rx.el.button(
                    "Close",
                    class_name="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                ),
            ),
            
            max_width="600px",
        ),
    )


# ============ IMPLEMENTATION NOTES ============
"""
DASHBOARD UPDATE:
1. Changed from cards to minimal sidebar navigation
2. Added dialog for instructions (not overlay by default)
3. "Show Instructions" button that user can click when needed
4. Kept existing lucide icons (library, folder-open, folder-plus)
5. Clean, minimal design matching the mockup

STYLING NOTES:
- Minimal sidebar with just buttons
- No heavy backgrounds or borders
- Instructions in a dialog instead of always visible
- Maintains clean look when instructions are closed
"""