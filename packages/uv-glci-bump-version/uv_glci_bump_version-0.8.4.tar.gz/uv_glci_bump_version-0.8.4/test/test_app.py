import os
import pathlib
import sys

import pytest

import test.mock
import test.mock.git
import test.mock.uv
import test.projects
from uv_glci_bump_version import app, util, version


def create_executable(script: util.HasDunderFile, bin_dir: pathlib.Path):
    script_path = pathlib.Path(script.__file__)
    bin_dir.mkdir(parents=True, exist_ok=True)
    executable_path = bin_dir / script_path.stem
    executable_path.write_text('\n'.join(['#!/bin/bash', f'{sys.executable} {script_path} "$@"']))
    executable_path.chmod(0o555)


def run_app(
    project_name: str,
    *,
    increment_kind: version.IncrementKind = version.IncrementKind.PATCH,
    gitlab_domain: str = 'exemple.com',
    access_token: str = 'access-token',
    disable_uv: bool = False,
    disable_git: bool = False,
    disable_project_name: bool = False,
    disable_project_path: bool = False,
    commit_ref_name: str | None = 'commit-ref-name',
):
    with util.make_tmp_dir_copy(util.module_path(test.projects) / project_name) as project_dir:
        os.chdir(project_dir)
        bin_dir = project_dir / 'bin'
        if not disable_git:
            create_executable(test.mock.git, bin_dir)
        if not disable_uv:
            create_executable(test.mock.uv, bin_dir)
        with (
            util.set_env('CI_PROJECT_NAME', project_name if not disable_project_name else None),
            util.set_env(
                'CI_PROJECT_PATH',
                f'{project_dir.parent.parent.name}/{project_name}'
                if not disable_project_path
                else None,
            ),
            util.set_env('CI_COMMIT_REF_NAME', commit_ref_name),
            util.set_env('PATH', bin_dir),
        ):
            app.app(
                increment=increment_kind, gitlab_domain=gitlab_domain, access_token=access_token
            )
            return test.mock.git.get_state(project_dir)


def test_simple():
    git_state = run_app('simple')
    assert git_state == test.mock.git.State(
        user_name='simple-ci',
        user_email='simple-ci@exemple.com',
        remote_name_url_map={
            'ci_origin': 'https://simple-ci:access-token@exemple.com/projects/simple.git'
        },
        staged_files={},
        commits=[],
        pushed=[
            test.mock.git.Pushed(
                commit=test.mock.git.Commit(
                    message='Bumped version to 0.1.1',
                    files={
                        pathlib.Path(
                            'pyproject.toml'
                        ): '[project]\nname = "simple"\nversion = "0.1.1"\n',
                        pathlib.Path('uv.lock'): '',
                    },
                ),
                repository='ci_origin',
                refspec='HEAD:commit-ref-name',
                option='ci.skip',
            )
        ],
    )


def test_cannot_find_git(capsys: pytest.CaptureFixture[str]):
    with pytest.raises(SystemExit):
        run_app('simple', disable_git=True)

    assert 'Cannot find git' in capsys.readouterr().out


def test_cannot_find_uv(capsys: pytest.CaptureFixture[str]):
    with pytest.raises(SystemExit):
        run_app('simple', disable_uv=True)

    assert 'Cannot find uv' in capsys.readouterr().out


def test_cannot_find_project_name(capsys: pytest.CaptureFixture[str]):
    with pytest.raises(SystemExit):
        run_app('simple', disable_project_name=True)
    assert 'CI_PROJECT_NAME' in capsys.readouterr().out


def test_cannot_find_project_path(capsys: pytest.CaptureFixture[str]):
    with pytest.raises(SystemExit):
        run_app('simple', disable_project_path=True)
    assert 'CI_PROJECT_PATH' in capsys.readouterr().out


def test_cannot_find_commit_ref_name(capsys: pytest.CaptureFixture[str]):
    with pytest.raises(SystemExit):
        run_app('simple', commit_ref_name=None)
    assert 'CI_COMMIT_REF_NAME' in capsys.readouterr().out
