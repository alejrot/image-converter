"""This module is dedicated to support translation settings and options."""

import locale

from code.consts import DefaultValue

import i18n as lang


# translations folder - YAML files
lang.load_path.append('locale/')

# locale language as prefered one
locale_language = locale.getlocale()
prefered_language = locale_language[0][0:2].lower()
lang.set('locale', prefered_language.lower() )

# default language
default_language = DefaultValue.LANGUAGE.value
lang.set('fallback', default_language.lower())
