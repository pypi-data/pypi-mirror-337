import click
import ollama
from yaspin import yaspin

from src.pyapidocs import PyDoc


@click.command()
@click.option("--model", "-m", default="gemma3:12b", help="Ollama model to use.")
@click.option("--extension", "-e", help="File extension to make documentation for")
@click.option(
    "--dir",
    "-d",
    multiple=True,
    default=[],
    help="Specify a directory to recursively make documentation for.",
)
@click.option("--file", "-f", multiple=True, default=(), help="Specify a file to make documentation for.")
@click.option("--ignore", "-i", multiple=True, default=(), help="Specify a file or dir to make documentation for.")
def cli(model, extension, dir, file, ignore):
    with yaspin(text="Checking model"):
        models = ollama.list()
        has_model = next(
            (True for ollama_model in models["models"] if ollama_model.model == model),
            False,
        )

    if not has_model:
        with yaspin(text="Pulling model"):
            try:
                ollama.pull(model)
            except ollama.ResponseError as e:
                if e.status_code == 500:
                    raise click.BadParameter(f"{model} is not a valid ollama model")

    pydoc = PyDoc(model, extension, dir, file, ignore)
    pydoc.generate_documentation()
