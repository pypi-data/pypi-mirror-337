from uv_glci_bump_version import app


def main():
    app.APP.__call__(print_error=False, exit_on_error=False)
