from blueness import module
from bluer_options.help.functions import help_main

from blue_south import NAME
from blue_south.help.functions import help_functions

NAME = module.name(__file__, NAME)


help_main(NAME, help_functions)
