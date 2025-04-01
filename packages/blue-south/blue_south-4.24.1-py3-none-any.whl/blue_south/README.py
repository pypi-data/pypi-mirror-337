import os

from bluer_objects import file, README

from blue_south import NAME, VERSION, ICON, REPO_NAME
from blue_south.content import items


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
