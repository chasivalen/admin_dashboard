# ltx_automation_app/components/ltx_bench/evaluation_library/add_readme_views.py


import reflex as rx
from ltx_automation_app.states.ltx_bench_state import EvaluationLibraryState


def add_readme_step_one() -> rx.Component:
    """
    Step 1: Form with title and dropdown selections.
    """
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h2(
                "Add New Read Me Instructions",
                class_name="text-2xl font-semibold text-gray-900 mb-6"
            ),
            class_name="border-b pb-4"
        ),
        
        # Form fields
        rx.el.div(
            # Title input
            rx.el.div(
                rx.el.label(
                    "Read Me Title",
                    class_name="block text-sm font-medium text-gray-700 mb-2"
                ),
                rx.el.input(
                    placeholder="Field Text",
                    value=EvaluationLibraryState.new_readme_title,
                    on_change=EvaluationLibraryState.set_new_readme_title,
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                ),
                class_name="mb-5"
            ),
            
            # Eval Type dropdown with tooltip
            rx.el.div(
                rx.el.div(
                    rx.el.label("Eval Type:", class_name="text-sm font-medium text-gray-700"),
                    rx.tooltip(
                        rx.icon("circle-help", class_name="w-4 h-4 text-gray-400 ml-2"),
                        content="The type of evaluations for which you would use this type of evaluation. Select from the dropdown and create new if the category does not exist."
                    ),
                    class_name="flex items-center mb-2"
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Select...", value=""),
                        rx.foreach(
                            EvaluationLibraryState.eval_type_options,
                            lambda option: rx.el.option(option, value=option)
                        ),
                        value=EvaluationLibraryState.new_eval_type,
                        on_change=EvaluationLibraryState.set_new_eval_type,
                        class_name="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-5 h-5"),
                        on_click=lambda: EvaluationLibraryState.show_add_option_input("eval_type"),
                        class_name="ml-2 p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                    ),
                    class_name="flex items-center"
                ),
                # Inline input for adding new option (shown conditionally)
                rx.cond(
                    EvaluationLibraryState.show_eval_type_input,
                    rx.el.div(
                        rx.el.input(
                            placeholder="Enter new eval type...",
                            value=EvaluationLibraryState.new_option_input,
                            on_change=EvaluationLibraryState.set_new_option_input,
                            on_key_down=lambda key: rx.cond(
                                key == "Enter",
                                EvaluationLibraryState.add_new_eval_type(),
                            ),
                            class_name="flex-1 px-3 py-2 border border-green-300 rounded-lg mt-2"
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Add",
                                on_click=EvaluationLibraryState.add_new_eval_type,
                                class_name="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                            ),
                            rx.el.button(
                                "Cancel",
                                on_click=lambda: EvaluationLibraryState.cancel_add_option(),
                                class_name="px-3 py-1 ml-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                            ),
                            class_name="mt-2"
                        ),
                        class_name="mt-2"
                    ),
                ),
                class_name="mb-4"
            ),
            
            # Score Type dropdown with tooltip
            rx.el.div(
                rx.el.div(
                    rx.el.label("Score Type:", class_name="text-sm font-medium text-gray-700"),
                    rx.tooltip(
                        rx.icon("circle-help", class_name="w-4 h-4 text-gray-400 ml-2"),
                        content="The way the users will score the type of evaluation for which this read me is used. The scoring type should match the text in the instructions."
                    ),
                    class_name="flex items-center mb-2"
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Select...", value=""),
                        rx.foreach(
                            EvaluationLibraryState.score_type_options,
                            lambda option: rx.el.option(option, value=option)
                        ),
                        value=EvaluationLibraryState.new_score_type,
                        on_change=EvaluationLibraryState.set_new_score_type,
                        class_name="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-5 h-5"),
                        on_click=lambda: EvaluationLibraryState.show_add_option_input("score_type"),
                        class_name="ml-2 p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                    ),
                    class_name="flex items-center"
                ),
                # Inline input for adding new option
                rx.cond(
                    EvaluationLibraryState.show_score_type_input,
                    rx.el.div(
                        rx.el.input(
                            placeholder="Enter new score type...",
                            value=EvaluationLibraryState.new_option_input,
                            on_change=EvaluationLibraryState.set_new_option_input,
                            on_key_down=lambda key: rx.cond(
                                key == "Enter",
                                EvaluationLibraryState.add_new_score_type(),
                            ),
                            class_name="flex-1 px-3 py-2 border border-green-300 rounded-lg mt-2"
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Add",
                                on_click=EvaluationLibraryState.add_new_score_type,
                                class_name="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                            ),
                            rx.el.button(
                                "Cancel",
                                on_click=lambda: EvaluationLibraryState.cancel_add_option(),
                                class_name="px-3 py-1 ml-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                            ),
                            class_name="mt-2"
                        ),
                        class_name="mt-2"
                    ),
                ),
                class_name="mb-4"
            ),
            
            # Pre-Eval dropdown with tooltip
            rx.el.div(
                rx.el.div(
                    rx.el.label("Pre-Eval:", class_name="text-sm font-medium text-gray-700"),
                    rx.tooltip(
                        rx.icon("circle-help", class_name="w-4 h-4 text-gray-400 ml-2"),
                        content="If there is a Pre-Eval field used, what are the options the user will be able to select from in this type of evaluation? Select from the dropdown and create new score type if one does not exist."
                    ),
                    class_name="flex items-center mb-2"
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Select...", value=""),
                        rx.foreach(
                            EvaluationLibraryState.pre_eval_options,
                            lambda option: rx.el.option(option, value=option)
                        ),
                        value=EvaluationLibraryState.new_pre_eval,
                        on_change=EvaluationLibraryState.set_new_pre_eval,
                        class_name="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-5 h-5"),
                        on_click=lambda: EvaluationLibraryState.show_add_option_input("pre_eval"),
                        class_name="ml-2 p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                    ),
                    class_name="flex items-center"
                ),
                # Inline input for adding new option
                rx.cond(
                    EvaluationLibraryState.show_pre_eval_input,
                    rx.el.div(
                        rx.el.input(
                            placeholder="Enter new pre-eval option...",
                            value=EvaluationLibraryState.new_option_input,
                            on_change=EvaluationLibraryState.set_new_option_input,
                            on_key_down=lambda key: rx.cond(
                                key == "Enter",
                                EvaluationLibraryState.add_new_pre_eval(),
                            ),
                            class_name="flex-1 px-3 py-2 border border-green-300 rounded-lg mt-2"
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Add",
                                on_click=EvaluationLibraryState.add_new_pre_eval,
                                class_name="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                            ),
                            rx.el.button(
                                "Cancel",
                                on_click=lambda: EvaluationLibraryState.cancel_add_option(),
                                class_name="px-3 py-1 ml-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                            ),
                            class_name="mt-2"
                        ),
                        class_name="mt-2"
                    ),
                ),
                class_name="mb-4"
            ),
            
            # Read Me Type radio buttons with tooltip
            rx.el.div(
                rx.el.div(
                    rx.el.label("Read Me Type:", class_name="text-sm font-medium text-gray-700"),
                    rx.tooltip(
                        rx.icon("circle-help", class_name="w-4 h-4 text-gray-400 ml-2"),
                        content="Select default if this is Read Me language that you use frequently based on the Eval Type, Score Type, and Pre-Eval data you have entered. This selection is used to speed up the process when you're filtering it for use in your project."
                    ),
                    class_name="flex items-center mb-2"
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="readme_type",
                            value="default",
                            checked=EvaluationLibraryState.new_readme_type == "DEFAULT",
                            on_change=lambda: EvaluationLibraryState.set_new_readme_type("DEFAULT"),
                            class_name="mr-2 text-indigo-600 focus:ring-indigo-500"
                        ),
                        "DEFAULT",
                        class_name="flex items-center mr-6 cursor-pointer"
                    ),
                    rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="readme_type",
                            value="custom",
                            checked=EvaluationLibraryState.new_readme_type == "CUSTOM",
                            on_change=lambda: EvaluationLibraryState.set_new_readme_type("CUSTOM"),
                            class_name="mr-2 text-indigo-600 focus:ring-indigo-500"
                        ),
                        "CUSTOM",
                        class_name="flex items-center cursor-pointer"
                    ),
                    class_name="flex items-center"
                ),
                class_name="mb-6"
            ),
            
            # Action buttons
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=EvaluationLibraryState.cancel_add_readme_view,
                    class_name="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 mr-3"
                ),
                rx.el.button(
                    "Continue",
                    on_click=EvaluationLibraryState.proceed_to_step_two,
                    class_name="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
                ),
                class_name="flex justify-end"
            ),
            
            class_name="space-y-4"
        ),
        class_name="bg-white rounded-lg p-6"
    )


def add_readme_step_two() -> rx.Component:
    """
    Step 2: Rich text editor for README content.
    """
    return rx.el.div(
        # Header showing selected values
        rx.el.div(
            rx.el.h2(
                EvaluationLibraryState.new_readme_title,
                class_name="text-2xl font-semibold text-gray-900 mb-3"
            ),
            rx.el.div(
                # Display selected values
                rx.el.div(
                    rx.el.span("Eval Type: ", class_name="font-medium"),
                    rx.el.span(EvaluationLibraryState.new_eval_type, class_name="text-gray-700"),
                    class_name="mr-6"
                ),
                rx.el.div(
                    rx.el.span("Score Type: ", class_name="font-medium"),
                    rx.el.span(EvaluationLibraryState.new_score_type, class_name="text-gray-700"),
                    class_name="mr-6"
                ),
                rx.el.div(
                    rx.el.span("Pre-Eval: ", class_name="font-medium"),
                    rx.el.span(EvaluationLibraryState.new_pre_eval, class_name="text-gray-700"),
                    class_name="mr-6"
                ),
                rx.el.div(
                    rx.el.span("Type: ", class_name="font-medium"),
                    rx.cond(
                        EvaluationLibraryState.new_readme_type == "DEFAULT",
                        rx.el.span("• DEFAULT", class_name="text-gray-700"),
                        rx.el.span("CUSTOM", class_name="text-gray-700")
                    ),
                ),
                class_name="flex items-center text-sm text-gray-600 border-b pb-3"
            ),
            class_name="mb-4"
        ),
        
        # Rich text editor section
        rx.el.div(
            # Toolbar (visual only for now)
            rx.el.div(
                rx.el.button(
                    rx.el.span("B", class_name="font-bold"),
                    class_name="px-3 py-1 text-white bg-indigo-600 rounded hover:bg-indigo-700 mr-1"
                ),
                rx.el.button(
                    rx.el.span("I", class_name="italic"),
                    class_name="px-3 py-1 text-gray-700 bg-gray-100 rounded hover:bg-gray-200 mr-1"
                ),
                rx.el.button(
                    rx.el.span("U", class_name="underline"),
                    class_name="px-3 py-1 text-gray-700 bg-gray-100 rounded hover:bg-gray-200 mr-3"
                ),
                rx.el.button(
                    "•••",
                    class_name="px-3 py-1 text-gray-700 bg-gray-100 rounded hover:bg-gray-200"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4"),
                    rx.el.span("Tag", class_name="ml-1"),
                    class_name="ml-auto px-3 py-1 text-green-600 bg-green-50 rounded hover:bg-green-100 flex items-center"
                ),
                class_name="flex items-center mb-3 pb-3 border-b"
            ),
            
            # Label for text area
            rx.el.label(
                "Read Me Instructions Label",
                class_name="block text-sm font-medium text-gray-700 mb-2"
            ),
            
            # Text area for content
            rx.el.textarea(
                placeholder="Text",
                value=EvaluationLibraryState.new_readme_content,
                on_change=EvaluationLibraryState.set_new_readme_content,
                rows=20,
                class_name="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none font-mono text-sm",
            ),
            
            # Action buttons
            rx.el.div(
                rx.el.button(
                    "CANCEL",
                    on_click=EvaluationLibraryState.cancel_add_readme_view,
                    class_name="px-6 py-2 bg-gray-100 text-gray-700 font-medium rounded hover:bg-gray-200 transition-colors"
                ),
                rx.el.button(
                    "SAVE",
                    on_click=EvaluationLibraryState.save_new_readme_view,
                    class_name="px-8 py-2 bg-indigo-600 text-white font-medium rounded hover:bg-indigo-700 transition-colors"
                ),
                class_name="flex items-center justify-end gap-3 mt-6"
            ),
            class_name="bg-gray-50 rounded-lg p-6"
        ),
        class_name="bg-white rounded-lg p-6"
    )