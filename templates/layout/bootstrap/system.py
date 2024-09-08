from AIMER2.template_helpers.theme import TemplateHelper

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in AIMER2/__init__.py
"""


class TemplateBootstrapSystem:
    def init(self):
        self.update(
            {
                "layout": "blank",
                "content_layout": "wide",
                "display_customizer": False,
            },
        )
        # map_context according to updated context values
        TemplateHelper.map_context(self)

        return self
