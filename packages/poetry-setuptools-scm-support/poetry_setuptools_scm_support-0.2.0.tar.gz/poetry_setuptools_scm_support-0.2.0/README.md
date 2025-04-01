A Poetry plugin that integrates setuptools_scm <https://pypi.org/project/setuptools-scm/> to console

Updates pyproject.toml file version with a calculated one

The idea is to add a mechanism for managing dev builds' versions guaranteeing uniqueness of them at deploy time  

usage:

    poetry version-calculate [scm:date]
        scm: Formats according to setuptools_scm default behavior,  e.g. 0.1.dev1+g1e0ede4
        date: Formats versions as date. Result format is {guessed}.dev{distance}+{node}, date format is Y.m.d,  e.g. 2025.3.31.1.dev1+g1e0ede4
        dist: Same as date, but without dirty tag, e.g. 2025.3.31.1.dev1

See setuptools_scm documentation and project sources for details

