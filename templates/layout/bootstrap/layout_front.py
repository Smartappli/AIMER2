from AIMER2.template_helpers.theme import TemplateHelper

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in AIMER2/__init__.py
"""


class TemplateBootstrapLayoutFront:
    def init(self):
        self.update(
            {
                "layout": "front",
                "is_front": True,
                "display_customizer": True,
                "content_layout": "wide",
                "navbar_type": "fixed",
            },
        )
        # map_context according to updated context values
        TemplateHelper.map_context(self)

        return self
