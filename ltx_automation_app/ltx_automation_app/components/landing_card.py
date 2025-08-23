# ltx_automation_app/components/landing_card.py
"""
Landing card component for main page navigation.
Clean and reusable.
"""

import reflex as rx


def landing_card(title: str, description: str, href: str, icon_name: str) -> rx.Component:
    """
    Navigation card for landing page.
    
    Args:
        title: Card title
        description: Card description text
        href: Navigation link
        icon_name: Icon to display
    """
    return rx.el.a(
        rx.el.div(
            # Icon
            rx.icon(
                icon_name,
                class_name="w-12 h-12 text-indigo-600 mb-4",
            ),
            
            # Title
            rx.el.h2(
                title,
                class_name="text-xl font-semibold text-gray-800 mb-2",
            ),
            
            # Description
            rx.el.p(
                description,
                class_name="text-gray-600",
            ),
            
            class_name="p-6 text-center",
        ),
        
        href=href,
        class_name="block bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg hover:border-indigo-300 transition-all",
    )