import os
from importlib import import_module, util

from django.conf import settings


# Core TemplateHelper class
class TemplateHelper:
    # Init the Template Context using TEMPLATE_CONFIG
    def init_context(self):
        self.update(
            {
                "layout": settings.TEMPLATE_CONFIG.get("layout"),
                "theme": settings.TEMPLATE_CONFIG.get("theme"),
                "style": settings.TEMPLATE_CONFIG.get("style"),
                "rtl_support": settings.TEMPLATE_CONFIG.get("rtl_support"),
                "rtl_mode": settings.TEMPLATE_CONFIG.get("rtl_mode"),
                "has_customizer": settings.TEMPLATE_CONFIG.get(
                    "has_customizer",
                ),
                "display_customizer": settings.TEMPLATE_CONFIG.get(
                    "display_customizer",
                ),
                "content_layout": settings.TEMPLATE_CONFIG.get(
                    "content_layout",
                ),
                "navbar_type": settings.TEMPLATE_CONFIG.get("navbar_type"),
                "header_type": settings.TEMPLATE_CONFIG.get("header_type"),
                "menu_fixed": settings.TEMPLATE_CONFIG.get("menu_fixed"),
                "menu_collapsed": settings.TEMPLATE_CONFIG.get(
                    "menu_collapsed",
                ),
                "footer_fixed": settings.TEMPLATE_CONFIG.get("footer_fixed"),
                "show_dropdown_onhover": settings.TEMPLATE_CONFIG.get(
                    "show_dropdown_onhover",
                ),
                "customizer_controls": settings.TEMPLATE_CONFIG.get(
                    "customizer_controls",
                ),
            },
        )
        return self

    # ? Map context variables to template class/value/variables names
    def map_context(self) -> None:
        #! Header Type (horizontal support only)
        if self.get("layout") == "horizontal":
            if self.get("header_type") == "fixed":
                self["header_type_class"] = "layout-menu-fixed"
            elif self.get("header_type") == "static":
                self["header_type_class"] = ""
            else:
                self["header_type_class"] = ""
        else:
            self["header_type_class"] = ""

        #! Navbar Type (vertical/front support only)
        if self.get("layout") != "horizontal":
            if self.get("navbar_type") == "fixed":
                self["navbar_type_class"] = "layout-navbar-fixed"
            elif self.get("navbar_type") == "static":
                self["navbar_type_class"] = ""
            else:
                self["navbar_type_class"] = "layout-navbar-hidden"
        else:
            self["navbar_type_class"] = ""

        # Menu collapsed
        self["menu_collapsed_class"] = (
            "layout-menu-collapsed" if self.get("menu_collapsed") else ""
        )

        #! Menu Fixed (vertical support only)
        if self.get("layout") == "vertical":
            if self.get("menu_fixed") is True:
                self["menu_fixed_class"] = "layout-menu-fixed"
            else:
                self["menu_fixed_class"] = ""

        # Footer Fixed
        self["footer_fixed_class"] = (
            "layout-footer-fixed" if self.get("footer_fixed") else ""
        )

        # RTL Supported template
        self["rtl_support_value"] = "/rtl" if self.get("rtl_support") else ""

        # RTL Mode/Layout
        self["rtl_mode_value"], self["text_direction_value"] = (
            ("rtl", "rtl") if self.get("rtl_mode") else ("ltr", "ltr")
        )

        #!  Show dropdown on hover (Horizontal menu)
        self["show_dropdown_onhover_value"] = (
            "true" if self.get("show_dropdown_onhover") else "false"
        )

        # Display Customizer
        self["display_customizer_class"] = (
            "" if self.get("display_customizer") else "customizer-hide"
        )

        # Content Layout
        if self.get("content_layout") == "wide":
            self["container_class"] = "container-fluid"
            self["content_layout_class"] = "layout-wide"
        else:
            self["container_class"] = "container-xxl"
            self["content_layout_class"] = "layout-compact"

        # Detached Navbar
        if self.get("navbar_detached"):
            self["navbar_detached_class"] = "navbar-detached"
        else:
            self["navbar_detached_class"] = ""

    # Get theme variables by scope
    def get_theme_variables(self):
        return settings.THEME_VARIABLES[self]

    # Get theme config by scope
    def get_theme_config(self):
        return settings.TEMPLATE_CONFIG[self]

    # Set the current page layout and init the layout bootstrap file
    def set_layout(self, context=None) -> str:
        # Extract layout from the view path
        if context is None:
            context = {}
        layout = os.path.splitext(self)[0].split("/")[0]

        # Get module path
        module = f"templates.{settings.THEME_LAYOUT_DIR.replace('/', '.')}.bootstrap.{layout}"

        # Check if the bootstrap file is exist
        if util.find_spec(module) is not None:
            # Auto import and init the default bootstrap.py file from the theme
            TemplateBootstrap = TemplateHelper.import_class(
                module,
                f"TemplateBootstrap{layout.title().replace('_', '')}",
            )
            TemplateBootstrap.init(context)
        else:
            module = f"templates.{settings.THEME_LAYOUT_DIR.replace('/', '.')}.bootstrap.default"

            TemplateBootstrap = TemplateHelper.import_class(
                module,
                "TemplateBootstrapDefault",
            )
            TemplateBootstrap.init(context)

        return f"{settings.THEME_LAYOUT_DIR}/{self}"

    # Import a module by string
    def import_class(self, import_className):
        module = import_module(self)
        return getattr(module, import_className)
