"""This module is dedicated to support translation settings and options."""

# standard library
import locale
import sys
from pathlib import Path

# project code
from .consts import DefaultValue

# packages
import i18n as lang


# translations folder in source code folder - YAML files
environment_path = sys.exec_prefix
locale_path = Path(environment_path).parent.joinpath("locale")
lang.load_path.append(locale_path)

# locale language as prefered one
locale_language = locale.getlocale()
prefered_language = locale_language[0][0:2].lower()
lang.set("locale", prefered_language.lower())

# default language
default_language = DefaultValue.LANGUAGE.value
lang.set("fallback", default_language.lower())
