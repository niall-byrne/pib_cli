"""Localization support for the pib_cli."""

import gettext
import pathlib

LOCALEDIR = str(pathlib.Path(__file__).parent)

translation = gettext.translation(
    'base',
    localedir=LOCALEDIR,
    fallback=True,
)
translation.install()

_ = translation.gettext
