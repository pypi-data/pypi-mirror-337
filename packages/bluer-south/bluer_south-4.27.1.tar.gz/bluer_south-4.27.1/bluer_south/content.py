import bluer_ai
import bluer_options
import bluer_objects
from bluer_objects import README
import gizai


items = README.Items(
    [
        {
            "name": module.NAME,
            "marquee": module.MARQUEE,
            "description": " ".join(
                [
                    module.DESCRIPTION.replace(module.ICON, "").strip(),
                    " [![PyPI version](https://img.shields.io/pypi/v/{}.svg)](https://pypi.org/project/{}/)".format(
                        module.NAME, module.NAME
                    ),
                ]
            ),
            "url": f"https://github.com/kamangir/{module.REPO_NAME}",
        }
        for module in [
            bluer_ai,
            bluer_options,
            bluer_objects,
            gizai,
        ]
    ]
)
