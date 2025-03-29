import os

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform

from carbonkivy.theme.size_tokens import (
    font_style_tokens,
    spacing_tokens,
    button_size_tokens,
)
from carbonkivy.config import IBMPlex


def get_font_name(typeface: str, weight_style: str) -> str:
    font_dir = os.path.join(
        IBMPlex,
        typeface.replace(" ", "_"),
        "static",
        f"{typeface.replace(' ', '')}-{weight_style}.ttf",
    )
    return font_dir


def get_font_style(token: str) -> float:
    return font_style_tokens[token]


def get_spacing(token: str) -> float:
    return spacing_tokens[token]


def get_button_size(token: str) -> float:
    return button_size_tokens[token]


button_background_tokens = {
    "active": {
        "Primary": "button_primary_active",
        "Secondary": "button_secondary_active",
        "Tertiary": "button_tertiary_active",
        "Ghost": "background_active",
        "Danger Primary": "button_danger_active",
        "Danger Tertiary": "button_danger_active",
        "Danger Ghost": "button_danger_active",
    },
    "normal": {
        "Primary": "button_primary",
        "Secondary": "button_secondary",
        "Tertiary": "transparent",
        "Ghost": "transparent",
        "Danger Primary": "button_danger_primary",
        "Danger Tertiary": "transparent",
        "Danger Ghost": "button_danger_active",
    },
    "disabled": {
        "Primary": "button_disabled",
        "Secondary": "button_disabled",
        "Tertiary": "transparent",
        "Ghost": "transparent",
        "Danger Primary": "button_disabled",
        "Danger Tertiary": "transparent",
        "Danger Ghost": "transparent",
    },
}


def get_button_token(state: str, type: str) -> str:
    return button_background_tokens[state][type]


class _Dict(dict):
    """Implements access to dictionary values via a dot."""

    def __getattr__(self, name):
        return self[name]


# Feel free to override this const if you're designing for a device such as
# a GNU/Linux tablet.
DEVICE_IOS = platform == "ios" or platform == "macosx"
if platform != "android" and platform != "ios":
    DEVICE_TYPE = "desktop"
elif Window.width >= dp(738) and Window.height >= dp(738):
    DEVICE_TYPE = "tablet"
else:
    DEVICE_TYPE = "mobile"
