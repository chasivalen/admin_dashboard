"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Welcome to Reflex!", class_name="text-6xl font-bold"),
            rx.el.p(
                "Get started by editing ",
                class_name="xl:text-xl text-lg",
            ),
            rx.el.p(f"{config.app_name}/{config.app_name}.py", class_name="inline"),
            rx.el.a(
                rx.el.button(
                    "Check out our docs!",
                    class_name="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600",
                ),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            rx.el.p(f"Running at {rx.State.router.url}", class_name="mt-8 text-xs"),
            class_name="flex flex-col items-center justify-center space-y-5 min-h-[85vh] px-4",
        ),
    )


app = rx.App()
app.add_page(index)
