import reflex as rx

# Database configuration
DATABASE_URL = "sqlite:///data/ltx_automation.db"

config = rx.Config(
    app_name="ltx_automation_app",
    # Add database URL
    db_url=DATABASE_URL,
    # Explicitly declare plugins to avoid warnings
    plugins=[
        # Tailwind V3 with configuration
        rx.plugins.tailwind_v3.TailwindV3Plugin(
            config={
                "theme": {
                    "extend": {}
                },
                "safelist": [
                    "text-indigo-600",
                    "bg-indigo-600", 
                    "hover:bg-indigo-700",
                    "border-indigo-600",
                    "ring-indigo-500",
                    "focus:ring-indigo-500",
                    "focus:border-indigo-500"
                ]
            }
        ),
        # Explicitly include sitemap plugin to avoid warning
        rx.plugins.sitemap.SitemapPlugin(),
    ],
)