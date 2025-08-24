# evaluation_library_view.py
"""
Updated Evaluation Library view with proper alignment, icons, and database integration.
"""

import reflex as rx
from ltx_automation_app.states.ltx_bench_state import EvaluationLibraryState


def evaluation_library_view() -> rx.Component:
    """
    Main evaluation library view with properly aligned sidebar and content.
    """
    return rx.el.div(
        # Header
        rx.el.div(
            rx.icon("home", class_name="w-5 h-5 text-gray-600 mr-2"),
            rx.el.h1("Evaluation Library", class_name="text-2xl font-bold text-gray-800"),
            class_name="flex items-center px-6 py-4 border-b border-gray-200 bg-white"
        ),
        
        # Main content area - sidebar and content aligned
        rx.el.div(
            # Sidebar with proper alignment
            evaluation_library_sidebar(),
            
            # Content area that aligns with sidebar
            rx.el.div(
                library_content_area(),
                class_name="flex-1 bg-white rounded-lg mx-6 my-4 p-6 shadow-sm border border-gray-200"
            ),
            
            class_name="flex flex-1 min-h-0"
        ),
        
        # Back to Dashboard at bottom
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                "Back to Dashboard",
                href="/ltx-bench",
                class_name="flex items-center text-gray-600 hover:text-gray-800 text-sm"
            ),
            class_name="px-6 py-3 border-t border-gray-200 bg-white"
        ),
        
        # Info icon with instructions (bottom left of sidebar)
        rx.popover.root(
            rx.popover.trigger(
                rx.el.button(
                    rx.icon("circle-help", class_name="w-4 h-4"),
                    rx.el.span("Using Library", class_name="ml-2 text-xs"),
                    class_name="fixed bottom-20 left-4 flex items-center text-gray-500 hover:text-gray-700 hover:bg-gray-50 px-3 py-1.5 rounded transition-colors"
                )
            ),
            rx.popover.content(
                rx.el.div(
                    rx.el.h3("Instructions for Use:", class_name="font-semibold text-gray-900 mb-2"),
                    rx.el.p(
                        "Use the Template Builder if you're ready to build a template to be used for future projects which are then stored in the Template Library. If you need to edit a component within the evaluations, you can do that before creating a template.",
                        class_name="text-sm text-gray-600"
                    ),
                    class_name="max-w-xs"
                ),
                side="right",
                align="end",
                class_name="bg-white border border-gray-200 rounded-lg shadow-lg p-4"
            )
        ),
        
        class_name="flex flex-col h-screen bg-gray-50",
        on_mount=EvaluationLibraryState.initialize_readme_library
    )


def evaluation_library_sidebar() -> rx.Component:
    """
    Sidebar with icons and proper alignment.
    """
    return rx.el.div(
        # Evaluation Library section
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.cond(
                        EvaluationLibraryState.eval_library_expanded,
                        rx.icon("chevron-down", class_name="w-4 h-4"),
                        rx.icon("chevron-right", class_name="w-4 h-4")
                    ),
                    rx.el.span("Evaluation Library", class_name="font-medium text-sm"),
                    class_name="flex items-center gap-2"
                ),
                on_click=EvaluationLibraryState.toggle_eval_library,
                class_name="w-full text-left px-4 py-2 hover:bg-gray-50 rounded"
            ),
            
            # Collapsible content with icons
            rx.cond(
                EvaluationLibraryState.eval_library_expanded,
                rx.el.div(
                    sidebar_item_with_icon("Read Me", "readme", "book-open-check"),
                    sidebar_item_with_icon("Metrics", "metrics", "layout-list"),
                    sidebar_item_with_icon("Calculations", "calculations", "calculator"),
                    sidebar_item_with_icon("Questions", "questions", "message-square"),
                    sidebar_item_with_icon("Charts and Tables", "charts", "chart-bar"),
                    class_name="ml-2"
                ),
                rx.el.div()
            ),
            class_name="mb-3"
        ),
        
        # Template Library section
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.cond(
                        EvaluationLibraryState.template_library_expanded,
                        rx.icon("chevron-down", class_name="w-4 h-4"),
                        rx.icon("chevron-right", class_name="w-4 h-4")
                    ),
                    rx.el.span("Template Library", class_name="font-medium text-sm"),
                    class_name="flex items-center gap-2"
                ),
                on_click=EvaluationLibraryState.toggle_template_library,
                class_name="w-full text-left px-4 py-2 hover:bg-gray-50 rounded"
            ),
            
            # Collapsible content with icons
            rx.cond(
                EvaluationLibraryState.template_library_expanded,
                rx.el.div(
                    sidebar_item_with_icon("Existing Templates", "existing_templates", "folder"),
                    sidebar_item_with_icon("Template Builder", "template_builder", "file-plus"),
                    class_name="ml-2"
                ),
                rx.el.div()
            ),
            class_name="mb-3"
        ),
        
        # Using Eval Library item (if selected)
        rx.cond(
            EvaluationLibraryState.selected_section == "using_eval",
            sidebar_item_with_icon("Using Eval Library", "using_eval", "circle-check"),
            rx.el.div()
        ),
        
        class_name="w-64 p-4 bg-white border-r border-gray-200"
    )


def sidebar_item_with_icon(label: str, section_id: str, icon_name: str) -> rx.Component:
    """
    Sidebar item with icon.
    """
    return rx.el.button(
        rx.icon(
            icon_name, 
            class_name=rx.cond(
                EvaluationLibraryState.selected_section == section_id,
                "w-4 h-4 text-indigo-600",  # Indigo when selected
                "w-4 h-4 text-indigo-500"   # Lighter indigo when not selected
            )
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                EvaluationLibraryState.selected_section == section_id,
                "text-indigo-600 font-medium",
                "text-gray-700"
            )
        ),
        on_click=lambda: EvaluationLibraryState.select_library_section(section_id),
        class_name=rx.cond(
            EvaluationLibraryState.selected_section == section_id,
            "w-full flex items-center gap-3 px-3 py-2 bg-indigo-50 border-l-2 border-indigo-600",
            "w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-50"
        )
    )


def library_content_area() -> rx.Component:
    """
    Main content area based on selected section.
    """
    return rx.cond(
        EvaluationLibraryState.selected_section == "readme",
        readme_library_view(),
        rx.cond(
            EvaluationLibraryState.selected_section == "metrics",
            metrics_library_content(),
            rx.cond(
                EvaluationLibraryState.selected_section == "calculations",
                calculations_library_content(),
                rx.cond(
                    EvaluationLibraryState.selected_section == "questions",
                    questions_library_content(),
                    rx.cond(
                        EvaluationLibraryState.selected_section == "charts",
                        charts_library_content(),
                        rx.cond(
                            EvaluationLibraryState.selected_section == "existing_templates",
                            existing_templates_content(),
                            rx.cond(
                                EvaluationLibraryState.selected_section == "template_builder",
                                template_builder_content(),
                                default_content()
                            )
                        )
                    )
                )
            )
        )
    )


def readme_library_view() -> rx.Component:
    """
    Read Me Library view with proper database integration and edit mode.
    """
    return rx.el.div(
        # Header (Add New Instructions button will be added here later)
        rx.el.div(
            rx.el.h2("Read Me Library", class_name="text-xl font-semibold"),
            # TODO: Add New Instructions button will be implemented with new design
            class_name="flex items-center justify-between mb-6"
        ),
        
        # README Selection Dropdown
        rx.el.div(
            rx.el.label("Select Read Me", class_name="text-sm font-medium text-gray-700 mr-3"),
            rx.el.select(
                rx.el.option("Select a README template...", value=""),
                rx.foreach(
                    EvaluationLibraryState.readme_instructions,
                    lambda readme: rx.el.option(
                        readme["title"],
                        value=readme["id"]
                    )
                ),
                value=EvaluationLibraryState.selected_readme_id,
                on_change=EvaluationLibraryState.select_readme,
                class_name="w-96 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            ),
            class_name="flex items-center mb-6"
        ),
        
        # Selected README Display/Edit
        rx.cond(
            EvaluationLibraryState.selected_readme_id != "",
            readme_content_section(),
            rx.el.div(
                rx.el.p(
                    "Select a README template from the dropdown to view its contents.",
                    class_name="text-gray-500 text-center py-12"
                ),
                class_name="border border-gray-200 rounded-lg bg-gray-50 min-h-[400px] flex items-center justify-center"
            )
        )
    )


def readme_content_section() -> rx.Component:
    """
    README content section with edit mode including title editing.
    """
    return rx.el.div(
        # Title bar with edit controls
        rx.el.div(
            # Title (editable in edit mode)
            rx.el.input(
                value=rx.cond(
                    EvaluationLibraryState.readme_edit_mode,
                    EvaluationLibraryState.edit_readme_title,
                    EvaluationLibraryState.selected_readme_title
                ),
                on_change=EvaluationLibraryState.set_edit_readme_title,
                disabled=~EvaluationLibraryState.readme_edit_mode,
                class_name="text-xl font-semibold px-2 py-1 border border-gray-300 rounded disabled:bg-gray-50 disabled:cursor-not-allowed"
            ),
            
            # Edit/Save/Cancel buttons
            rx.el.div(
                rx.cond(
                    EvaluationLibraryState.readme_edit_mode,
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=EvaluationLibraryState.cancel_edit,
                            class_name="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 mr-2"
                        ),
                        rx.el.button(
                            "Save",
                            on_click=EvaluationLibraryState.save_readme_changes,
                            class_name="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                        ),
                        class_name="flex items-center"
                    ),
                    rx.el.button(
                        rx.icon("pencil", class_name="w-4 h-4 mr-2"),
                        "Edit",
                        on_click=EvaluationLibraryState.toggle_edit_mode,
                        class_name="flex items-center px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                    )
                ),
                class_name="flex items-center"
            ),
            class_name="flex items-center justify-between mb-6 pb-4 border-b"
        ),
        
        # Dropdowns and Radio buttons - all visible, just disabled in view mode
        rx.el.div(
            # Eval Type dropdown
            rx.el.div(
                rx.el.label("Eval Type:", class_name="text-sm font-medium text-gray-700 mb-1"),
                rx.el.select(
                    rx.foreach(
                        EvaluationLibraryState.eval_type_options,
                        lambda option: rx.el.option(option, value=option)
                    ),
                    value=rx.cond(
                        EvaluationLibraryState.readme_edit_mode,
                        EvaluationLibraryState.edit_eval_type,
                        EvaluationLibraryState.selected_eval_type
                    ),
                    on_change=EvaluationLibraryState.set_edit_eval_type,
                    disabled=~EvaluationLibraryState.readme_edit_mode,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded disabled:bg-gray-50 disabled:cursor-not-allowed"
                ),
                class_name="flex-1"
            ),
            
            # Score Type dropdown
            rx.el.div(
                rx.el.label("Score Type:", class_name="text-sm font-medium text-gray-700 mb-1"),
                rx.el.select(
                    rx.foreach(
                        EvaluationLibraryState.score_type_options,
                        lambda option: rx.el.option(option, value=option)
                    ),
                    value=rx.cond(
                        EvaluationLibraryState.readme_edit_mode,
                        EvaluationLibraryState.edit_score_type,
                        EvaluationLibraryState.selected_score_type
                    ),
                    on_change=EvaluationLibraryState.set_edit_score_type,
                    disabled=~EvaluationLibraryState.readme_edit_mode,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded disabled:bg-gray-50 disabled:cursor-not-allowed"
                ),
                class_name="flex-1"
            ),
            
            # Pre-Eval dropdown
            rx.el.div(
                rx.el.label("Pre-Eval:", class_name="text-sm font-medium text-gray-700 mb-1"),
                rx.el.select(
                    rx.foreach(
                        EvaluationLibraryState.pre_eval_options,
                        lambda option: rx.el.option(option, value=option)
                    ),
                    value=rx.cond(
                        EvaluationLibraryState.readme_edit_mode,
                        EvaluationLibraryState.edit_pre_eval,
                        EvaluationLibraryState.selected_pre_eval
                    ),
                    on_change=EvaluationLibraryState.set_edit_pre_eval,
                    disabled=~EvaluationLibraryState.readme_edit_mode,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded disabled:bg-gray-50 disabled:cursor-not-allowed"
                ),
                class_name="flex-1"
            ),
            
            # Type radio buttons
            rx.el.div(
                rx.el.label("Type:", class_name="text-sm font-medium text-gray-700 mb-1"),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="default_custom",
                            value="default",
                            checked=rx.cond(
                                EvaluationLibraryState.readme_edit_mode,
                                EvaluationLibraryState.edit_default_custom == "default",
                                EvaluationLibraryState.selected_default_custom == "default"
                            ),
                            on_change=lambda: EvaluationLibraryState.set_edit_default_custom("default"),
                            disabled=~EvaluationLibraryState.readme_edit_mode,
                            class_name="mr-2 disabled:cursor-not-allowed"
                        ),
                        "DEFAULT",
                        class_name="flex items-center mr-4"
                    ),
                    rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="default_custom",
                            value="custom",
                            checked=rx.cond(
                                EvaluationLibraryState.readme_edit_mode,
                                EvaluationLibraryState.edit_default_custom == "custom",
                                EvaluationLibraryState.selected_default_custom == "custom"
                            ),
                            on_change=lambda: EvaluationLibraryState.set_edit_default_custom("custom"),
                            disabled=~EvaluationLibraryState.readme_edit_mode,
                            class_name="mr-2 disabled:cursor-not-allowed"
                        ),
                        "CUSTOM",
                        class_name="flex items-center"
                    ),
                    class_name="flex items-center"
                ),
                class_name="flex-1"
            ),
            
            class_name="grid grid-cols-4 gap-4 mb-4"
        ),
        
        # README Content Text with proper scroll
        rx.el.div(
            rx.el.textarea(
                value=rx.cond(
                    EvaluationLibraryState.readme_edit_mode,
                    EvaluationLibraryState.edit_readme_content,
                    EvaluationLibraryState.selected_readme_content
                ),
                on_change=EvaluationLibraryState.set_edit_readme_content,
                disabled=~EvaluationLibraryState.readme_edit_mode,
                rows=12,
                class_name="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none disabled:bg-gray-50 disabled:cursor-not-allowed"
            ),
            class_name="mt-4"
        )
    )


# Placeholder functions for other sections
def default_content() -> rx.Component:
    return rx.el.div(
        rx.el.p("Select an item from the sidebar to view content.", class_name="text-gray-500 text-center py-12")
    )


def metrics_library_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Metrics Library", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Metrics management interface coming soon...", class_name="text-gray-500")
    )


def calculations_library_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Calculations Library", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Calculations interface coming soon...", class_name="text-gray-500")
    )


def questions_library_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Questions Library", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Questions interface coming soon...", class_name="text-gray-500")
    )


def charts_library_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Charts and Tables Library", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Charts and tables interface coming soon...", class_name="text-gray-500")
    )


def existing_templates_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Existing Templates", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Templates list coming soon...", class_name="text-gray-500")
    )


def template_builder_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Template Builder", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Template builder interface coming soon...", class_name="text-gray-500")
    )