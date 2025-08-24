# ltx_automation_app/state.py

"""
Global application state management.

This file can be used for shared state across the entire application.
Currently, all state is managed in feature-specific state files:
- ltx_bench_state.py: LTX Bench feature state
- Future: seo_state.py, lingnet_state.py as those features are developed

If global app-wide state is needed in the future, implement it here.
"""

import reflex as rx


class AppState(rx.State):
    """
    Global application state.
    
    Add any app-wide state variables and methods here that need to be
    shared across multiple features/pages.
    
    Examples might include:
    - User authentication state
    - Global app settings
    - Theme preferences
    - Navigation state
    """
    
    # App version for display
    app_version: str = "1.0.0"
    
    # Global loading state
    is_loading: bool = False
    
    def set_loading(self, loading: bool):
        """Set global loading state."""
        self.is_loading = loading