from pathlib import Path

import click
import ollama
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern
from yaspin import yaspin

from src.constants import documentation_message, readme_message


class PyDoc:
    def __init__(self, model: str, extension: str, dir: tuple, file: tuple, ignore: tuple):
        self.model = model
        self.messages = []
        self.extension = extension if extension.startswith(".") else f".{extension}"
        self.cwd = Path.cwd()
        self.dir = list(set(dir))
        self.file = list(set(file))
        self.ignore = list(set(ignore))

    def generate_documentation(self):
        with yaspin(text="Generating documentation..."):
            files = self.get_files()

            for file in files:
                self.messages = [documentation_message]
                self.messages.append({"role": "user", "content": file.read_text()})

                doc_path = Path(f"{self.cwd}/docs/")
                md_file = doc_path.joinpath(file.parent, file.name.replace(file.suffix, ".md"))

                if md_file.exists():
                    self.messages.append(
                        {
                            "role": "user",
                            "content": f"""A markdown file already exists use this as a reference,
                            keeping the same format/styling and add whats missing {md_file.read_text()}""",
                        },
                    )

                response = ollama.chat(model=self.model, messages=self.messages)
                self.write_md_file(response.message.content, file)

    def generate_readme(self):
        with yaspin(text="Generating readme..."):
            self.get_files()

            for file in self.files:
                self.messages = [readme_message]
                self.messages.append({"role": "user", "content": file.read_text()})
                response = ollama.chat(model=self.model, messages=self.messages)
                self.write_md_file(response.message.content, file)
                break

    def get_files(self):
        gitignore = self.cwd.joinpath(".gitignore")
        ignore = PathSpec.from_lines(GitWildMatchPattern, self.ignore)

        if gitignore.exists():
            with open(gitignore, "r") as f:
                patterns = []
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    patterns.append(line)
                ignore += PathSpec.from_lines(GitWildMatchPattern, patterns)

        search_files = []

        if not self.dir and not self.file:
            search_files = list(self.cwd.rglob(f"*{self.extension}"))

        if self.dir:
            for dir in self.dir:
                search_files += list(Path(dir).rglob(f"*{self.extension}"))

        if self.file:
            search_files += [Path(file) for file in self.file]

        files = []
        for path in search_files:
            if not path.exists():
                raise click.BadParameter(f"File {path} does not exist")

            if ignore and ignore.match_file(path):
                continue

            files.append(path)
        return files

    def write_md_file(self, content: str, file: Path):
        doc_path = Path(f"{self.cwd}/docs/")

        md_file = doc_path.joinpath(file.parent.relative_to(self.cwd), file.name.replace(file.suffix, ".md"))
        md_file.parent.mkdir(exist_ok=True, parents=True)

        md_file.write_text(content)
