import cyclopts
import pytest

APP = cyclopts.App(version='0.0.0')


@APP.default
def main(*, expect_full: bool = False, verbosity: int = 0):
    args = [
        '--cov=uv_glci_bump_version',
        '--cov-branch',
        '--cov-report=html',
        f'--verbosity={verbosity}',
    ]
    if expect_full:
        args.append('--cov-fail-under=100')

    return pytest.main(args)


if __name__ == '__main__':
    APP.__call__(print_error=True, exit_on_error=False)
