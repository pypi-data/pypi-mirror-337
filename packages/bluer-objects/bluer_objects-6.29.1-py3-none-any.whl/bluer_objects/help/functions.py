from bluer_ai.help.generic import help_functions as generic_help_functions

from bluer_objects import ALIAS
from bluer_objects.help.download import help_download
from bluer_objects.help.upload import help_upload

help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "download": help_download,
        "upload": help_upload,
    }
)
