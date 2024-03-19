from argparse import ArgumentParser
from typing import Any

from crytic_compile.cryticparser.cryticparser import init as crytic_parser_init
from pygls.server import LanguageServer


def get_command_line_args(ls: LanguageServer, params: Any) -> Any:
    """
    Handler which obtains data regarding all command line arguments available in crytic-compile.
    """

    # Read our argument parser
    parser = ArgumentParser()
    crytic_parser_init(parser)

    # Loop through all option groups and underlying options and populate our result.
    # (this is a bit hacky as it accesses a private variable, but we don't have that much of an option).
    results = []
    for arg_group in parser._action_groups:
        # Compile a list of args, skipping the help command.
        args_in_group = []
        for arg in arg_group._group_actions:
            if "--help" not in arg.option_strings:
                args_in_group.append(
                    {
                        "names": arg.option_strings,
                        "help": arg.help,
                        "default": arg.default,
                        "dest": arg.dest,
                    }
                )

        # If after filtering we still ahve arguments, add this argument group to our results
        if len(args_in_group) > 0:
            results.append({"title": arg_group.title, "args": args_in_group})

    # Return our argument group -> arguments hierarchy.
    return results
