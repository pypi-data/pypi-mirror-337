from pathlib import Path
from typing import Annotated, Any

import typer
from rich import box
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from bmhub.backend_hf import (
    download_hf_model,
    list_hf_models,
    remove_hf_model,
    update_hf_model,
)
from bmhub.backend_ms import (
    download_ms_model,
    list_ms_models,
    remove_ms_model,
    update_ms_model,
)
from bmhub.schema import Backend, CachedModelInfo
from bmhub.utils import format_size

app = typer.Typer(no_args_is_help=True, help="BigModel Hub CLI Toolkit")

BACKEND_ARGUMENT: Any = typer.Argument(help="Model hub backend", show_default=False)
MODEL_ID_ARGUMENT: Any = typer.Argument(help="Model ID", show_default=False)
PATTERN_OPTION: Any = typer.Option(
    "--pattern", "-p", help="Glob pattern to match model IDs", show_default=False
)
LOCAL_DIR_OPTION: Any = typer.Option(
    "--local-dir",
    help="The local model directory",
    show_default=False,
    exists=True,
    file_okay=False,
    dir_okay=True,
    resolve_path=True,
)


def print_model_table(console: Console, models: list[CachedModelInfo]) -> None:
    table = Table(box=box.SIMPLE)
    table.add_column(header="MODEL ID", no_wrap=True)
    table.add_column(header="SIZE ON DISK", justify="right", no_wrap=True)
    table.add_column(header="NB FILES", justify="right", no_wrap=True)
    table.add_column(header="LAST ACCESSED", no_wrap=True)
    table.add_column(header="LAST MODIFIED", no_wrap=True)
    table.add_column(header="MODEL PATH", no_wrap=True)
    for model in models:
        table.add_row(
            model.id,
            model.size_on_disk_str,
            str(object=model.num_files),
            model.last_accessed_str,
            model.last_modified_str,
            str(object=model.path),
        )

    num_models: int = len(models)
    size_on_disk_str: str = format_size(
        size=sum(model.size_on_disk for model in models)
    )

    console.print(table)
    console.print(f"Scanned {num_models} repo(s) for a total of {size_on_disk_str}.")


@app.command(name="list")
def list_(
    backend: Annotated[Backend, BACKEND_ARGUMENT],
    *,
    pattern: Annotated[str | None, PATTERN_OPTION] = None,
    local_dir: Annotated[Path | None, LOCAL_DIR_OPTION] = None,
) -> None:
    """List downloaded models."""
    models: list[CachedModelInfo]
    match backend:
        case Backend.HUGGING_FACE:
            models = list_hf_models(pattern=pattern, local_dir=local_dir)
        case Backend.MODEL_SCOPE:
            models = list_ms_models(pattern=pattern, local_dir=local_dir)
    print_model_table(console=Console(), models=models)


@app.command()
def download(
    backend: Annotated[Backend, BACKEND_ARGUMENT],
    model_id: Annotated[str, MODEL_ID_ARGUMENT],
    *,
    local_dir: Annotated[Path | None, LOCAL_DIR_OPTION] = None,
) -> None:
    """Download a model from the model hub."""
    model_path: Path | None = None if local_dir is None else local_dir / model_id
    model_path_str: str = "cache" if model_path is None else f"<{model_path}>"
    Console().print(f"Downloading <{model_id}> to the {model_path_str}...")
    match backend:
        case Backend.HUGGING_FACE:
            download_hf_model(model_id=model_id, model_path=model_path)
        case Backend.MODEL_SCOPE:
            download_ms_model(model_id=model_id, model_path=model_path)


@app.command()
def update(
    backend: Annotated[Backend, BACKEND_ARGUMENT],
    *,
    pattern: Annotated[str | None, PATTERN_OPTION] = None,
    local_dir: Annotated[Path | None, LOCAL_DIR_OPTION] = None,
) -> None:
    """Update downloaded models."""
    models: list[CachedModelInfo]
    match backend:
        case Backend.HUGGING_FACE:
            models = list_hf_models(pattern=pattern, local_dir=local_dir)
        case Backend.MODEL_SCOPE:
            models = list_ms_models(pattern=pattern, local_dir=local_dir)

    console = Console()
    for model in models:
        console.print(f"Updating <{model.id}> in the <{model.path}>...")
        match backend:
            case Backend.HUGGING_FACE:
                update_hf_model(model=model)
            case Backend.MODEL_SCOPE:
                update_ms_model(model=model)


@app.command()
def remove(
    backend: Annotated[Backend, BACKEND_ARGUMENT],
    *,
    pattern: Annotated[str | None, PATTERN_OPTION] = None,
    local_dir: Annotated[Path | None, LOCAL_DIR_OPTION] = None,
) -> None:
    """Remove downloaded models."""
    models: list[CachedModelInfo]
    match backend:
        case Backend.HUGGING_FACE:
            models = list_hf_models(pattern=pattern, local_dir=local_dir)
        case Backend.MODEL_SCOPE:
            models = list_ms_models(pattern=pattern, local_dir=local_dir)

    console = Console()
    console.print("The following models will be removed:")
    print_model_table(console=console, models=models)
    console.print(escape(markup="Do you want to remove these models? [y/N] "), end="")
    if not console.input().lower() == "y":
        return
    for model in models:
        console.print(f"Removing <{model.id}> in the <{model.path}>...")
        match backend:
            case Backend.HUGGING_FACE:
                remove_hf_model(model=model)
            case Backend.MODEL_SCOPE:
                remove_ms_model(model=model)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
