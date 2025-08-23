import reflex as rx


def placeholder_page(title: str) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.icon(
                "arrow-left",
                class_name="w-6 h-6 text-indigo-600",
            ),
            href="/",
            class_name="absolute top-8 left-8 p-2 rounded-full hover:bg-gray-100 transition-colors",
        ),
        rx.el.h1(
            f"{title} - Page Placeholder",
            class_name="text-4xl font-bold text-gray-800",
        ),
        rx.el.p(
            "This page is under construction.",
            class_name="text-lg text-gray-600 mt-4",
        ),
        class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-center p-8 relative font-['Inter']",
    )


def seo_page() -> rx.Component:
    return placeholder_page(title="SEO")


def lingnet_page() -> rx.Component:
    return placeholder_page(title="LingNet")