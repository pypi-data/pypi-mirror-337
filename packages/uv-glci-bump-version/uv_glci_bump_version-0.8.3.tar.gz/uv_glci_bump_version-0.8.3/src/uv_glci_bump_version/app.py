import pathlib
import subprocess

import cyclopts
import tomlkit
import tomlkit.items

import uv_glci_bump_version
from uv_glci_bump_version import util, version

APP = cyclopts.App(version=uv_glci_bump_version.__version__)


def update_pyproject_version(increment_kind: version.IncrementKind):
    pyproject_path = pathlib.Path('pyproject.toml')
    pyproject_document = tomlkit.parse(pyproject_path.read_text())
    project_item = pyproject_document['project']
    assert isinstance(project_item, tomlkit.items.Table)
    version_item = project_item['version']
    assert isinstance(version_item, tomlkit.items.String)
    old_version = version.Version.load(version_item)
    new_version = old_version.incremented(increment_kind)
    project_item['version'] = new_version.dump()
    pyproject_path.write_text(pyproject_document.as_string())
    return new_version


def update_lock_file():
    uv_exe_path = util.get_exe_path('uv')
    subprocess.run([uv_exe_path, 'lock'], check=True)


def push_changes(access_token: str, gitlab_domain: str, new_version: version.Version):
    git_exe_path = util.get_exe_path('git')

    def git(*args: str, no_check: bool = False):
        subprocess.run([git_exe_path, *args], check=not no_check)

    project_name = util.get_env_var('CI_PROJECT_NAME')
    project_path = util.get_env_var('CI_PROJECT_PATH')
    commit_ref_name = util.get_env_var('CI_COMMIT_REF_NAME')
    username = f'{project_name}-ci'
    email = f'{username}@{gitlab_domain}'
    origin_name = 'ci_origin'
    origin_url = f'https://{username}:{access_token}@{gitlab_domain}/{project_path}.git'

    git('config', 'user.name', username)
    git('config', 'user.email', email)
    git('remote', 'remove', origin_name, no_check=True)
    git('remote', 'add', origin_name, origin_url)
    git('add', 'pyproject.toml', 'uv.lock')
    git('commit', '-m', f'Bumped version to {new_version.dump()}')
    git('push', origin_name, f'HEAD:{commit_ref_name}', '-o', 'ci.skip')


@APP.default
def app(increment: version.IncrementKind, *, gitlab_domain: str = 'gitlab.com', access_token: str):
    new_version = update_pyproject_version(increment)
    update_lock_file()
    push_changes(access_token=access_token, gitlab_domain=gitlab_domain, new_version=new_version)
