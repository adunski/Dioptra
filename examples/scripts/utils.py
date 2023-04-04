# This Software (Dioptra) is being made available as a public service by the
# National Institute of Standards and Technology (NIST), an Agency of the United
# States Department of Commerce. This software was developed in part by employees of
# NIST and in part by NIST contractors. Copyright in portions of this software that
# were developed by NIST contractors has been licensed or assigned to NIST. Pursuant
# to Title 17 United States Code Section 105, works of NIST employees are not
# subject to copyright protection in the United States. However, NIST may hold
# international copyright in software created by its employees and domestic
# copyright (or licensing rights) in portions of software that were assigned or
# licensed to NIST. To the extent that NIST holds copyright in this software, it is
# being made available under the Creative Commons Attribution 4.0 International
# license (CC BY 4.0). The disclaimers of the CC BY 4.0 license apply to all parts
# of the software developed or licensed by NIST.
#
# ACCESS THE FULL CC BY 4.0 LICENSE HERE:
# https://creativecommons.org/licenses/by/4.0/legalcode
from __future__ import annotations

import tarfile
from pathlib import Path


def make_tar(
    source_dir: list[str | Path],
    tarball_filename: str,
    tarball_write_mode: str = "w:gz",
    working_dir: str | Path | None = None,
) -> Path:
    """Archives a list of directories and files and compresses the archive.

    Args:
        source_dir: The directories and files which should be archived.
        tarball_filename: The filename to use for the archived tarball.
        tarball_write_mode: The write mode for the tarball, see :py:func:`tarfile.open`
            for the full list of compression options. The default is `"w:gz"` (gzip
            compression).
        working_dir: The location where the file should be saved. If `None`, then the
            current working directory is used. The default is `None`.

    Returns:
        Path to the archive.

    See Also:
        - :py:func:`tarfile.open`
    """
    if working_dir is None:
        working_dir = Path.cwd()

    working_dir = Path(working_dir)
    tarball_path = working_dir / tarball_filename

    with tarfile.open(tarball_path, tarball_write_mode) as f:
        for dir in source_dir:
            dir = Path(dir)
            f.add(dir, arcname=dir.name)

    return tarball_path
