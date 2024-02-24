import os.path
from pathlib import Path

from split_settings.tools import include, optional  # type:ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

STATIC_ROOT = BASE_DIR / 'staticfiles'

ENVVAR_SETTINGS_PREFIX = 'WASHDAY_SETTINGS_'
LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'
if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    'base.py',
    'custom.py',
    optional(LOCAL_SETTINGS_PATH),
    'docker.py',
    'envvars.py',
)
