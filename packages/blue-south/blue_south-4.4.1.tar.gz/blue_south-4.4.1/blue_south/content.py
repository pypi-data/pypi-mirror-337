import abcli
import blue_options
import gizai
from blue_objects import README


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
            "url": f"https://github.com/kamangir/{module.NAME}",
        }
        for module in [
            gizai,
            abcli,
            blue_options,
        ]
    ]
)
