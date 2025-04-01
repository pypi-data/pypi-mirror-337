import json
import logging
import os
from typing import List, Optional, Union

import click
import tqdm

from mapchete.cli import options
from mapchete.io import copy
from mapchete.path import MPath

logger = logging.getLogger(__name__)

opt_recursive = click.option("--recursive", "-r", is_flag=True)


@click.group()
def mpath():
    pass


@mpath.command(help="Check whether path exists.")
@options.arg_path
def exists(path: MPath):
    click.echo(path.exists())


@mpath.command(help="copy path.")
@options.arg_path
@options.arg_out_path
@options.opt_src_fs_opts
@options.opt_dst_fs_opts
@options.opt_overwrite
@opt_recursive
@click.option("--skip-existing", is_flag=True)
@options.opt_debug
def cp(
    path: MPath,
    out_path: MPath,
    overwrite: bool = False,
    recursive: bool = False,
    skip_existing: bool = False,
    debug: bool = False,
    **_,
):
    try:
        if path.is_directory():
            if not recursive:  # pragma: no cover
                raise click.UsageError(
                    "source path is directory, --recursive flag required"
                )
            for _, __, files in tqdm.tqdm(path.walk(), disable=debug):
                for src_file in tqdm.tqdm(
                    [file for file in files if not file.is_directory()],
                    leave=False,
                    disable=debug,
                ):
                    dst_file = out_path / os.path.relpath(
                        str(src_file.without_protocol()),
                        start=str(path.without_protocol()),
                    )
                    message = f"copy {str(src_file)} to {str(dst_file)} ..."
                    if debug:  # pragma: no cover
                        logger.debug(message)
                    else:
                        tqdm.tqdm.write(message)
                    copy(
                        src_file, dst_file, overwrite=overwrite, exists_ok=skip_existing
                    )
        else:
            copy(path, out_path, overwrite=overwrite, exists_ok=skip_existing)
    except Exception as exc:  # pragma: no cover
        if debug:
            raise
        raise click.ClickException(str(exc))


@mpath.command(help="Remove path.")
@options.arg_path
@options.opt_src_fs_opts
@opt_recursive
@options.opt_force
def rm(path: MPath, recursive: bool = False, force: bool = False, **_):
    try:
        if force or click.confirm(
            f"do you really want to permanently delete {str(path)}?"
        ):
            path.rm(recursive=recursive)
    except Exception as exc:  # pragma: no cover
        raise click.ClickException(str(exc))


@mpath.command(help="List path contents.")
@options.arg_path
@options.opt_src_fs_opts
@click.option(
    "--date-format", type=click.STRING, default="%y-%m-%d %H:%M:%S", show_default=True
)
@click.option("--absolute-paths", is_flag=True)
@click.option("--spacing", type=click.INT, default=4, show_default=True)
@click.option("--max-depth", type=click.INT, default=None, show_default=True)
@opt_recursive
def ls(
    path: MPath,
    date_format: str = "%y-%m-%d %H:%M:%S",
    absolute_paths: bool = False,
    spacing: int = 4,
    recursive: bool = False,
    max_depth: Optional[int] = None,
    **_,
):
    size_column_width = 10

    def _print_rows(
        directories: List[MPath],
        files: List[MPath],
        last_modified_column_width: int = 0,
        size_column_width: int = 10,
        spacing: int = 4,
    ):
        for subpath in directories:
            click.echo(
                _row(
                    columns=[
                        "",
                        "",
                        (
                            f"{str(subpath)}/"
                            if absolute_paths
                            else f"{subpath.relative_to(path)}/"
                        ),
                    ],
                    widths=[last_modified_column_width, size_column_width, None],
                    spacing=spacing,
                )
            )
        for subpath in files:
            click.echo(
                _row(
                    columns=[
                        subpath.last_modified().strftime(date_format),
                        subpath.pretty_size(),
                        str(subpath) if absolute_paths else subpath.relative_to(path),
                    ],
                    widths=[last_modified_column_width, size_column_width, None],
                    spacing=spacing,
                )
            )

    try:
        last_modified_column_width = len(date_format)
        click.echo(
            _row(
                columns=["last modified", "size", "path"],
                widths=[last_modified_column_width, size_column_width, None],
                spacing=spacing,
                underlines=True,
            )
        )
        if recursive:
            for root, _, files in path.walk(absolute_paths=True, maxdepth=max_depth):
                _print_rows(
                    [root],  # type: ignore
                    files,  # type: ignore
                    last_modified_column_width=last_modified_column_width,
                    spacing=spacing,
                )
        else:
            directories = []
            files = []
            for subpath in path.ls(absolute_paths=True):
                if subpath.is_directory():  # type: ignore
                    directories.append(subpath)
                else:
                    files.append(subpath)
            _print_rows(
                directories,
                files,
                last_modified_column_width=last_modified_column_width,
                spacing=spacing,
            )

    except Exception as exc:  # pragma: no cover
        raise click.ClickException(str(exc))


def _row(
    columns: List[str],
    widths: List[Union[int, None]],
    spacing: int = 4,
    underlines: bool = False,
) -> str:
    def _column(text: str = "", width: Optional[int] = None):
        if width is None or len(text) > width:
            width = len(text)
        return text + " " * (width - len(text))

    def _column_underline(text: str = "", width: int = 4, symbol: str = "-") -> str:
        if width is None or len(text) > width:
            width = len(text)
        return symbol * len(text) + " " * (width - len(text))

    space = " " * spacing

    out = space.join([_column(column, width) for column, width in zip(columns, widths)])

    if underlines:
        out += "\n"
        out += space.join(
            [_column_underline(column, width) for column, width in zip(columns, widths)]  # type: ignore
        )

    return out


@mpath.command(help="Print contents of file as text.")
@options.arg_path
def read_text(path: MPath):
    try:
        click.echo(path.read_text())
    except Exception as exc:  # pragma: no cover
        raise click.ClickException(str(exc))


@mpath.command(help="Print contents of file as JSON.")
@options.arg_path
@click.option("--indent", "-i", type=click.INT, default=4)
def read_json(path: MPath, indent: int = 4):
    try:
        click.echo(json.dumps(path.read_json(), indent=indent))
    except Exception as exc:  # pragma: no cover
        raise click.ClickException(str(exc))
