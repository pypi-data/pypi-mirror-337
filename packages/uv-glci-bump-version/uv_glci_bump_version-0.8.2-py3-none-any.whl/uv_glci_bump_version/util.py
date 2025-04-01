import contextlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import typing


def get_exe_path(name: str):
    exe_path = shutil.which(name)
    if exe_path is None:
        print(f'Cannot find {name} executable')
        sys.exit(1)
    subprocess.run([exe_path, '--version'], check=True)
    return pathlib.Path(exe_path)


def get_env_var(name: str):
    value = os.getenv(name, '')
    if len(value) == 0:
        print(f'{name} is not set')
        sys.exit(1)
    return value


class HasDunderFile(typing.Protocol):
    @property
    def __file__(self) -> str: ...


def module_path(module: HasDunderFile):
    return pathlib.Path(module.__file__).parent.absolute()


@contextlib.contextmanager
def make_tmp_dir_copy(dir_path: pathlib.Path):
    with tempfile.TemporaryDirectory(dir=dir_path.parent) as tmp_dir:
        tmp_dir_copy_path = pathlib.Path(tmp_dir).absolute() / dir_path.name
        shutil.copytree(dir_path, tmp_dir_copy_path)
        yield tmp_dir_copy_path


@contextlib.contextmanager
def set_env(name: str, value: object):
    old_value = os.getenv(name)
    if value is not None:
        os.environ[name] = str(value)
    elif old_value is not None:
        del os.environ[name]
    try:
        yield
    finally:
        if old_value is not None:
            os.environ[name] = old_value
        elif value is not None:
            del os.environ[name]
