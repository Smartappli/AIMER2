import json

from django.conf import settings

from AIMER2.template_helpers.theme import TemplateHelper

menu_file_path = (
    settings.BASE_DIR
    / "templates"
    / "layout"
    / "partials"
    / "menu"
    / "vertical"
    / "json"
    / "vertical_menu.json"
)

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in AIMER2/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(self):
        self.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            },
        )

        # map_context according to updated context values
        TemplateHelper.map_context(self)

        TemplateBootstrapLayoutVertical.init_menu_data(self)

        return self

    def init_menu_data(self) -> None:
        # Load the menu data from the JSON file
        menu_data = (
            json.load(menu_file_path.open()) if menu_file_path.exists() else []
        )

        # Updated context with menu_data
        self.update({"menu_data": menu_data})
