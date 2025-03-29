import traceback
import os
import tempfile
import time
from uuid import uuid4
from term_image.image import from_file
import requests
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from typing_extensions import Annotated


DEFAULT_IMG_URL = "https://formless-data.s3.us-west-1.amazonaws.com/0.png"
API_URL = "https://andrewhinh--formless-api-modal-get.modal.run"

# Typer CLI
app = typer.Typer(
    rich_markup_mode="rich",
)
state = {"image_url": DEFAULT_IMG_URL, "image_path": None, "verbose": 0}


# helper
def call_api() -> None:
    image_url, image_path = state["image_url"], state["image_path"]

    response = requests.post(f"{API_URL}/api-key")
    assert response.ok, response.status_code
    api_key = response.json()

    if image_url:
        response = requests.post(API_URL, json={"image_url": image_url}, headers={"X-API-Key": api_key})
    else:
        response = requests.post(
            f"{API_URL}/upload",
            files={"image_file": open(image_path, "rb")},
            headers={
                "X-API-Key": api_key,
            },
        )
    assert response.ok, response.status_code
    return response.json()


# CLI cmd
@app.command(
    help="Hard handwriting OCR.",
    epilog="Made by [bold blue]Andrew Hinh.[/bold blue] :mechanical_arm::person_climbing:",
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
)
def scan(
    image_url: Annotated[
        str, typer.Option("--image-url", "-i", help="Image URL", rich_help_panel="Inputs")
    ] = DEFAULT_IMG_URL,
    image_path: Annotated[str, typer.Option("--image-path", "-p", help="Image Path", rich_help_panel="Inputs")] = None,
    verbose: Annotated[
        int, typer.Option("--verbose", "-v", count=True, help="Verbose mode", rich_help_panel="General")
    ] = 0,
):
    try:
        start = time.monotonic_ns()
        request_id = uuid4()

        state.update(
            {
                "image_url": image_url,
                "image_path": image_path,
                "verbose": verbose > 0,
            }
        )

        if state["verbose"]:
            if image_url and image_path:
                raise ValueError("Cannot accept both image_url and image_path yet.")
            elif image_url:
                response = requests.get(image_url)
                response.raise_for_status()
                image_filename = image_url.split("/")[-1]
                image_path = os.path.join(tempfile.gettempdir(), f"{uuid4()}-{image_filename}")
                with open(image_path, "wb") as file:
                    file.write(response.content)
            else:
                if not os.path.isfile(image_path):
                    raise ValueError("The provided image path is not valid.")
            terminal_image = from_file(image_path)
            terminal_image.draw()

        if state["verbose"]:
            print("[red]Press[/red] [blue]Ctrl+C[/blue] [red]to stop at any time.[/red]")
            with Progress(
                SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
            ) as progress:
                progress.add_task(f"Generating response to request {request_id}", total=None)
                generated_text = call_api()
        else:
            generated_text = call_api()
        print(f"[bold green]{generated_text}[/bold green]")

        if state["verbose"]:
            print(
                f"[red]request[/red] [blue]{request_id}[/blue] [red]completed in[/red] [blue]{round((time.monotonic_ns() - start) / 1e9, 2)}[/blue] [red]seconds[/red]"
            )

    except KeyboardInterrupt:
        if state["verbose"]:
            print("[red]\n\nExiting...[/red]")
    except Exception as e:
        if state["verbose"]:
            print(f"[red]Failed with error: {e}[/red]")
            print(traceback.format_exc())
            print("[red]\n\nExiting...[/red]")


# TODO:
# - add multiple uploads/urls
# - add user authentication:
#   - save gens and keys to user account
#   - complete file upload security: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
#       - Only allow authorized users to upload files: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
