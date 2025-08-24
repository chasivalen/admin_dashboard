# ltx_automation_app/ltx_automation_app.py
"""
Main app file - updated to use new state structure.
Cleaned and simplified.
"""

import reflex as rx
from ltx_automation_app.components.landing_card import landing_card
from ltx_automation_app.pages.placeholder_page import seo_page, lingnet_page
from ltx_automation_app.pages.ltx_bench_page import ltx_bench_page


def index() -> rx.Component:
    """
    Landing page for LTX Automation Tool.
    Displays navigation cards for the three main features.
    """
    return rx.el.div(
        # Header section
        rx.el.header(
            rx.el.div(
                rx.icon(
                    "bot",
                    class_name="w-16 h-16 text-indigo-600",
                ),
                rx.el.h1(
                    "LTX Automation Tool",
                    class_name="text-4xl font-bold text-gray-800 tracking-tight ml-4",
                ),
                class_name="flex items-center justify-center py-12 bg-white border-b border-gray-200",
            )
        ),
        
        # Main content section
        rx.el.main(
            rx.el.div(
                # Feature cards
                landing_card(
                    title="SEO",
                    description="Automate the SEO process the LTX team utilizes.",
                    href="/seo",
                    icon_name="search",
                ),
                landing_card(
                    title="LingNet",
                    description="View automation created for LingNet billing and reporting.",
                    href="/lingnet",
                    icon_name="users",
                ),
                landing_card(
                    title="LTX Bench",
                    description="Automate file prep, final summaries, and Tableau for the LTX Bench process.",
                    href="/ltx-bench",
                    icon_name="bar-chart-2",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto p-8",
            ),
            class_name="flex-grow container mx-auto px-4 py-8",
        ),
        
        # Footer section
        rx.el.footer(
            rx.el.p(
                "© 2025 LTX Automation Tool. All rights reserved.",
                class_name="text-sm text-gray-500",
            ),
            class_name="py-8 text-center border-t border-gray-200 bg-white",
        ),
        
        class_name="min-h-screen flex flex-col bg-gray-50",
    )


# Initialize the Reflex app with light theme
app = rx.App()

# Register pages
app.add_page(index, route="/")
app.add_page(seo_page, route="/seo")
app.add_page(lingnet_page, route="/lingnet")
app.add_page(ltx_bench_page, route="/ltx-bench")


# ============ CLEANUP NOTES ============
"""
CLEANED UP:
1. Main app file remains simple and clean
2. No changes needed here - routing stays the same
3. All state management happens in individual pages

The app structure is now:
- Landing page (/)
- SEO page (/seo) - placeholder
- LingNet page (/lingnet) - placeholder  
- LTX Bench page (/ltx-bench) - full implementation with dashboard
"""