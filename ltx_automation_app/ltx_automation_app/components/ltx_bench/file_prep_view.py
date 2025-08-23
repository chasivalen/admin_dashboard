# ltx_automation_app/components/ltx_bench/file_prep_view.py
"""
Updated File Prep view using FilePrepState.
NO STATIC FILE IMPORTS - All data from database.
"""

import reflex as rx
from ltx_automation_app.states.ltx_bench_state import (
    FilePrepState,
    LTXBenchNavigationState,
    EvaluationLibraryState  # To load README and metrics from database
)

# NO MORE STATIC FILE IMPORTS!
# All data comes from database through the state


def file_prep_view() -> rx.Component:
    """
    Main File Prep view with step-by-step workflow.
    Now uses FilePrepState and database data.
    """
    return rx.el.div(
        # Project info header
        project_info_header(),
        
        # Step Progress Indicator
        progress_indicator(),
        
        # Custom metrics datalist for suggestions (now from database)
        custom_metrics_datalist(),
        
        # Main content area - shows current step
        rx.cond(
            FilePrepState.current_file_prep_step == 1,
            step_1_readme_config(),
            rx.cond(
                FilePrepState.current_file_prep_step == 2,
                step_2_metrics_selection(),
                rx.cond(
                    FilePrepState.current_file_prep_step == 3,
                    step_3_file_upload(),
                    rx.cond(
                        FilePrepState.current_file_prep_step == 4,
                        step_4_export_settings(),
                        step_5_review_export()
                    )
                )
            )
        ),
        
        class_name="max-w-6xl mx-auto space-y-6",
        # CRITICAL FIX: Load database data when component mounts
        # These event handlers populate the state vars from the database
        on_mount=[
            EvaluationLibraryState.load_readme_instructions,
            EvaluationLibraryState.load_all_metrics  # This was being called but the method didn't exist!
        ]
    )


def step_2_metrics_selection() -> rx.Component:
    """Step 2: Metrics Selection from database."""
    return rx.el.div(
        rx.el.h2("Step 2: Select Metrics", class_name="text-2xl font-bold mb-6"),
        
        # Metric search
        rx.el.div(
            rx.input(
                placeholder="Search metrics...",
                value=FilePrepState.metric_search,
                on_change=FilePrepState.set_metric_search,
                class_name="w-full p-2 border rounded"
            ),
            class_name="mb-4"
        ),
        
        # Metrics from database - Now this will work!
        rx.el.div(
            rx.el.h3("Available Metrics", class_name="text-lg font-semibold mb-3"),
            rx.el.div(
                # This foreach now references a properly defined state var
                rx.foreach(
                    EvaluationLibraryState.all_metrics,  # This now exists!
                    lambda metric: rx.el.div(
                        rx.checkbox(
                            rx.el.div(
                                rx.el.span(metric["name"], class_name="font-medium"),
                                rx.el.span(f" ({metric['type']})", class_name="text-sm text-gray-500"),
                                class_name="flex items-center"
                            ),
                            checked=FilePrepState.selected_metric_ids.contains(metric["id"]),
                            on_change=lambda checked: FilePrepState.toggle_metric(metric["id"], checked)
                        ),
                        class_name="p-2 border-b"
                    )
                ),
                class_name="max-h-96 overflow-y-auto border rounded"
            )
        ),
        
        # Custom metric input
        rx.el.div(
            rx.el.h3("Add Custom Metric", class_name="text-lg font-semibold mb-3 mt-6"),
            rx.el.div(
                rx.input(
                    placeholder="Enter custom metric name...",
                    value=FilePrepState.custom_metric_input,
                    on_change=FilePrepState.set_custom_metric_input,
                    class_name="flex-1 p-2 border rounded"
                ),
                rx.button(
                    "Add",
                    on_click=FilePrepState.add_custom_metric,
                    class_name="ml-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                ),
                class_name="flex"
            )
        ),
        
        # Display selected metrics count
        rx.el.div(
            rx.el.span(
                f"Selected Metrics: {len(FilePrepState.selected_metric_ids)}",
                class_name="text-sm text-gray-600"
            ),
            class_name="mt-4"
        ),
        
        # Navigation buttons
        navigation_buttons(show_previous=True),
        
        class_name="bg-white p-6 rounded-lg shadow"
    )
def project_info_header() -> rx.Component:
    """Display current project and organization info."""
    return rx.el.div(
        rx.el.div(
            rx.el.span("Project: ", class_name="text-sm text-gray-600"),
            rx.el.span(
                LTXBenchNavigationState.selected_project,
                class_name="font-semibold text-gray-800"
            ),
            rx.el.span(" | ", class_name="text-gray-400 mx-2"),
            rx.el.span("Organization: ", class_name="text-sm text-gray-600"),
            rx.el.span(
                LTXBenchNavigationState.selected_organization,
                class_name="font-semibold text-gray-800"
            ),
            class_name="flex items-center"
        ),
        class_name="mb-6 p-4 bg-white rounded-lg shadow border border-gray-200"
    )


def progress_indicator() -> rx.Component:
    """Step progress indicator showing workflow progress."""
    steps = ["README", "Metrics", "Files", "Export", "Review"]
    
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                steps,
                lambda step, idx: rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            idx + 1,
                            class_name=rx.cond(
                                FilePrepState.current_file_prep_step > idx,
                                "text-white",
                                rx.cond(
                                    FilePrepState.current_file_prep_step == idx + 1,
                                    "text-purple-600",
                                    "text-gray-400"
                                )
                            )
                        ),
                        class_name=rx.cond(
                            FilePrepState.current_file_prep_step > idx,
                            "w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center",
                            rx.cond(
                                FilePrepState.current_file_prep_step == idx + 1,
                                "w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center border-2 border-purple-600",
                                "w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center"
                            )
                        )
                    ),
                    rx.el.span(
                        step,
                        class_name=rx.cond(
                            FilePrepState.current_file_prep_step == idx + 1,
                            "text-xs mt-1 font-semibold text-purple-600",
                            "text-xs mt-1 text-gray-500"
                        )
                    ),
                    class_name="flex flex-col items-center"
                )
            ),
            class_name="flex justify-between items-center"
        ),
        class_name="mb-8 p-6 bg-white rounded-lg shadow"
    )


def custom_metrics_datalist() -> rx.Component:
    """
    Create datalist for custom metrics suggestions from database.
    Uses metrics loaded from database instead of static files.
    """
    return rx.el.datalist(
        rx.foreach(
            EvaluationLibraryState.all_metrics,
            lambda metric: rx.el.option(metric["name"])
        ),
        id="custom_metrics_list"
    )


def step_1_readme_config() -> rx.Component:
    """Step 1: README Configuration."""
    return rx.el.div(
        rx.el.h2("Step 1: README Configuration", class_name="text-2xl font-bold mb-6"),
        
        # README Template Selection from database
        rx.el.div(
            rx.el.label("Select README Template", class_name="block text-sm font-medium mb-2"),
            rx.el.select(
                rx.el.option("Choose a README template...", value=""),
                rx.foreach(
                    EvaluationLibraryState.readme_instructions,
                    lambda readme: rx.el.option(
                        readme["README_TITLE"],
                        value=str(readme["README_ID"])
                    )
                ),
                value=FilePrepState.selected_readme_template,
                on_change=FilePrepState.select_readme_template,
                class_name="w-full p-2 border rounded"
            ),
            class_name="mb-4"
        ),
        
        # Stakeholder Perspective
        rx.el.div(
            rx.el.label("Stakeholder Perspective (Optional)", class_name="block text-sm font-medium mb-2"),
            rx.text_area(
                placeholder="Enter any stakeholder-specific context...",
                value=FilePrepState.stakeholder_perspective,
                on_change=FilePrepState.set_stakeholder_perspective,
                class_name="w-full p-2 border rounded",
                rows="4"
            ),
            class_name="mb-4"
        ),
        
        # Terminology Choices
        rx.el.div(
            rx.el.h3("Terminology Preferences", class_name="text-lg font-semibold mb-3"),
            
            rx.el.div(
                rx.el.label("Source Issue Term", class_name="block text-sm font-medium mb-1"),
                rx.input(
                    value=FilePrepState.terminology_choices["source_issue"],
                    on_change=FilePrepState.set_source_issue_term,
                    class_name="w-full p-2 border rounded"
                ),
                class_name="mb-3"
            ),
            
            rx.el.div(
                rx.el.label("Target Issue Term", class_name="block text-sm font-medium mb-1"),
                rx.input(
                    value=FilePrepState.terminology_choices["target_issue"],
                    on_change=FilePrepState.set_target_issue_term,
                    class_name="w-full p-2 border rounded"
                ),
                class_name="mb-3"
            ),
            
            rx.el.div(
                rx.el.label("Scoring Method", class_name="block text-sm font-medium mb-1"),
                rx.input(
                    value=FilePrepState.terminology_choices["scoring_instruction"],
                    on_change=FilePrepState.set_scoring_method,
                    class_name="w-full p-2 border rounded"
                ),
                class_name="mb-3"
            ),
            
            class_name="mb-6 p-4 bg-gray-50 rounded"
        ),
        
        # Navigation buttons
        navigation_buttons(show_previous=False),
        
        class_name="bg-white p-6 rounded-lg shadow"
    )


def step_2_metrics_selection() -> rx.Component:
    """Step 2: Metrics Selection from database."""
    return rx.el.div(
        rx.el.h2("Step 2: Select Metrics", class_name="text-2xl font-bold mb-6"),
        
        # Metric search
        rx.el.div(
            rx.input(
                placeholder="Search metrics...",
                value=FilePrepState.metric_search,
                on_change=FilePrepState.set_metric_search,
                class_name="w-full p-2 border rounded"
            ),
            class_name="mb-4"
        ),
        
        # Metrics from database
        rx.el.div(
            rx.el.h3("Available Metrics", class_name="text-lg font-semibold mb-3"),
            rx.el.div(
                rx.foreach(
                    EvaluationLibraryState.all_metrics,
                    lambda metric: rx.el.div(
                        rx.checkbox(
                            rx.el.div(
                                rx.el.span(metric["name"], class_name="font-medium"),
                                rx.el.span(f" ({metric['type']})", class_name="text-sm text-gray-500"),
                                class_name="flex items-center"
                            ),
                            checked=FilePrepState.selected_metrics.contains(metric["name"]),
                            on_change=lambda: FilePrepState.toggle_metric(metric["name"])
                        ),
                        rx.el.p(
                            metric["definition"],
                            class_name="ml-6 text-sm text-gray-600 mt-1"
                        ),
                        class_name="mb-3 p-3 border rounded hover:bg-gray-50"
                    )
                ),
                class_name="max-h-96 overflow-y-auto space-y-2"
            ),
            class_name="mb-6"
        ),
        
        # Custom metric input
        rx.el.div(
            rx.el.h3("Add Custom Metric", class_name="text-lg font-semibold mb-3"),
            rx.el.div(
                rx.input(
                    placeholder="Enter custom metric name...",
                    value=FilePrepState.custom_metric_input,
                    on_change=FilePrepState.set_custom_metric_input,
                    list="custom_metrics_list",
                    class_name="flex-1 p-2 border rounded"
                ),
                rx.button(
                    "Add Metric",
                    on_click=lambda: FilePrepState.add_custom_metric(FilePrepState.custom_metric_input),
                    class_name="ml-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
                ),
                class_name="flex"
            ),
            class_name="mb-6"
        ),
        
        # Selected metrics summary
        rx.el.div(
            rx.el.h3("Selected Metrics", class_name="text-lg font-semibold mb-2"),
            rx.el.p(
                rx.cond(
                    FilePrepState.selected_metrics.length() > 0,
                    f"{FilePrepState.selected_metrics.length()} metrics selected",
                    "No metrics selected"
                ),
                class_name="text-gray-600"
            ),
            class_name="mb-4 p-3 bg-blue-50 rounded"
        ),
        
        # Navigation buttons
        navigation_buttons(),
        
        class_name="bg-white p-6 rounded-lg shadow"
    )


def step_3_file_upload() -> rx.Component:
    """Step 3: File Upload and Configuration."""
    return rx.el.div(
        rx.el.h2("Step 3: Upload Files", class_name="text-2xl font-bold mb-6"),
        
        # File upload area
        rx.el.div(
            rx.upload(
                rx.el.div(
                    rx.icon("upload", size=48, class_name="text-gray-400 mb-4"),
                    rx.el.p("Drag and drop files here or click to browse", 
                           class_name="text-gray-600"),
                    rx.el.p("Supported formats: XLSX, XLS, CSV, TXT", 
                           class_name="text-sm text-gray-500 mt-2"),
                    class_name="flex flex-col items-center justify-center p-8"
                ),
                accept=".xlsx,.xls,.csv,.txt",
                multiple=True,
                on_drop=FilePrepState.handle_file_upload,
                class_name="border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-400 transition-colors"
            ),
            class_name="mb-6"
        ),
        
        # Uploaded files list
        rx.cond(
            FilePrepState.uploaded_files.length() > 0,
            rx.el.div(
                rx.el.h3("Uploaded Files", class_name="text-lg font-semibold mb-3"),
                rx.foreach(
                    FilePrepState.uploaded_files,
                    lambda file: rx.el.div(
                        rx.el.span(file["name"], class_name="flex-1"),
                        rx.el.span(f"{file['size']} bytes", class_name="text-sm text-gray-500 mr-4"),
                        rx.button(
                            "Remove",
                            on_click=lambda: FilePrepState.remove_file(file["name"]),
                            class_name="text-red-600 hover:text-red-800"
                        ),
                        class_name="flex items-center p-2 border rounded mb-2"
                    )
                ),
                class_name="mb-6"
            ),
            rx.el.div()
        ),
        
        # Additional options
        rx.el.div(
            rx.el.h3("Evaluation Options", class_name="text-lg font-semibold mb-3"),
            
            rx.el.div(
                rx.el.label("Number of Models", class_name="block text-sm font-medium mb-2"),
                rx.input(
                    type="number",
                    value=FilePrepState.num_models,
                    on_change=lambda v: FilePrepState.set_num_models(v),
                    min=1,
                    max=10,
                    class_name="w-24 p-2 border rounded"
                ),
                class_name="mb-4"
            ),
            
            rx.checkbox(
                "Include yellow warning for missing scores",
                checked=FilePrepState.include_yellow_warning,
                on_change=FilePrepState.toggle_yellow_warning,
                class_name="mb-4"
            ),
            
            class_name="p-4 bg-gray-50 rounded"
        ),
        
        # Navigation buttons
        navigation_buttons(),
        
        class_name="bg-white p-6 rounded-lg shadow"
    )


def step_4_export_settings() -> rx.Component:
    """Step 4: Export Settings."""
    return rx.el.div(
        rx.el.h2("Step 4: Export Settings", class_name="text-2xl font-bold mb-6"),
        
        rx.el.div(
            rx.el.label("Export Format", class_name="block text-sm font-medium mb-2"),
            rx.radio_group(
                ["Excel (.xlsx)", "CSV", "JSON"],
                value=FilePrepState.export_format,
                on_change=lambda v: FilePrepState.set_export_format(v),
                class_name="space-y-2"
            ),
            class_name="mb-6"
        ),
        
        rx.el.div(
            rx.el.label("Filename", class_name="block text-sm font-medium mb-2"),
            rx.input(
                placeholder="Enter filename (without extension)...",
                value=FilePrepState.excel_filename,
                on_change=FilePrepState.set_excel_filename,
                class_name="w-full p-2 border rounded"
            ),
            class_name="mb-6"
        ),
        
        # Navigation buttons
        navigation_buttons(),
        
        class_name="bg-white p-6 rounded-lg shadow"
    )


def step_5_review_export() -> rx.Component:
    """Step 5: Review and Export."""
    return rx.el.div(
        rx.el.h2("Step 5: Review and Generate", class_name="text-2xl font-bold mb-6"),
        
        # Summary of selections
        rx.el.div(
            rx.el.h3("Configuration Summary", class_name="text-lg font-semibold mb-4"),
            
            rx.el.div(
                rx.el.p(f"README Template: {FilePrepState.selected_readme_template}", 
                       class_name="mb-2"),
                rx.el.p(f"Selected Metrics: {FilePrepState.selected_metrics.length()}", 
                       class_name="mb-2"),
                rx.el.p(f"Uploaded Files: {FilePrepState.uploaded_files.length()}", 
                       class_name="mb-2"),
                rx.el.p(f"Number of Models: {FilePrepState.num_models}", 
                       class_name="mb-2"),
                rx.el.p(f"Export Format: {FilePrepState.export_format}", 
                       class_name="mb-2"),
                class_name="p-4 bg-gray-50 rounded"
            ),
            class_name="mb-6"
        ),
        
        # Generate button
        rx.el.div(
            rx.button(
                rx.cond(
                    FilePrepState.generation_status == "generating",
                    "Generating...",
                    "Generate Excel Template"
                ),
                on_click=FilePrepState.generate_excel,
                disabled=FilePrepState.generation_status == "generating",
                class_name="w-full py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400"
            ),
            class_name="mb-6"
        ),
        
        # Download link when ready
        rx.cond(
            FilePrepState.generation_status == "complete",
            rx.el.div(
                rx.link(
                    "Download Generated File",
                    href=FilePrepState.download_url,
                    class_name="text-blue-600 hover:text-blue-800 underline"
                ),
                class_name="text-center"
            ),
            rx.el.div()
        ),
        
        # Navigation buttons
        navigation_buttons(show_next=False),
        
        class_name="bg-white p-6 rounded-lg shadow"
    )


def navigation_buttons(show_previous: bool = True, show_next: bool = True) -> rx.Component:
    """Navigation buttons for moving between steps."""
    return rx.el.div(
        rx.cond(
            show_previous,
            rx.button(
                "Previous",
                on_click=FilePrepState.previous_step,
                class_name="px-6 py-2 border border-gray-300 rounded hover:bg-gray-50"
            ),
            rx.el.div()
        ),
        rx.cond(
            show_next,
            rx.button(
                "Next",
                on_click=FilePrepState.next_step,
                class_name="px-6 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
            ),
            rx.el.div()
        ),
        class_name="flex justify-between mt-6"
    )