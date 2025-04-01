import pathlib
import sys

import cyclopts

APP = cyclopts.App()


@APP.command
def lock() -> None:
    pathlib.Path('uv.lock').write_text('')


if __name__ == '__main__':
    APP.__call__(sys.argv[1:], print_error=True, exit_on_error=False)
