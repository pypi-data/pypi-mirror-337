from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.factory import Factory

from setuptools_scm import Configuration, ScmVersion, get_version
from setuptools_scm._get_version_impl import parse_scm_version
from setuptools_scm.version import guess_next_date_ver

import warnings

def fxn():
    warnings.warn("deprecated", UserWarning)


class CalculateVersion(Command):
    """
    Calculates the version of the package.

    command:name {version-calculate : Controls output format}
    """

    name = "version-calculate"
    description = "Calculates the version of the package relying on setuptools_scm"

    args_description = """
        scm: formats according to setuptools_scm default behavior. e.g. 0.1.dev1+g1e0ede4
        date: formats using last commit distance and dirty tag, e.g. 2025.3.31.1.dev1+g1e0ede4
        dist: formats using last commit distance only, e.g. 2025.3.31.1.dev1
    """
    arguments = [
        Argument(name="format", description=args_description, default="scm", required=False),
    ]


    def __do_default(self, c: Configuration) -> str:
        return get_version(root=c.root, relative_to=c.relative_to)

    def __do_inc(self, c: Configuration) -> str:
        scm_version: ScmVersion = parse_scm_version(c)

        return scm_version.format_next_version(
            guess_next_date_ver,
            date_fmt="%Y.%m.%d",
            fmt="{guessed}.dev{distance}+{node}",
        )

    def __do_distance(self, c: Configuration) -> str:
        scm_version: ScmVersion = parse_scm_version(c)

        return scm_version.format_next_version(
            guess_next_date_ver,
            date_fmt="%Y.%m.%d",
            fmt="{guessed}.dev{distance}",
        )


    def handle(self) -> int:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            poetry = Factory().create_poetry()
            c = Configuration.from_file(str(poetry.file))

            format_to_use = self.argument("format")
            if format_to_use == "scm":
                v = self.__do_default(c)
            elif format_to_use == "dist":
                v = self.__do_distance(c)
            elif format_to_use == "date":
                v = self.__do_inc(c)
            else:
                self.line_error(f"Unknown format: {format_to_use}")
                return 0

            confirm = self.ask(f'Dumping version "{v}" [Y/n]', 'Y')
            if confirm == "Y":
                poetry.pyproject.data.item('project').update(version=v)
                poetry.pyproject.file.write(poetry.pyproject.data)

            return 0


def factory():
    return CalculateVersion()

class ScmPlugin(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [CalculateVersion]

    def activate(self, application):
        application.command_loader.register_factory("version-calculate", factory)
