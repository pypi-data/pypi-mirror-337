import tomllib
from pathlib import Path
from typing import Optional


class PyprojectParseError(Exception):
    """Exception raised when the pyproject.toml file cannot be parsed."""


class PyprojectInfo:
    """
    Parses and stores relevant information from a pyproject.toml file.

    Attributes:
        path (Path): The path to the pyproject.toml file.
        name (Optional[str]): The project name.
        version (Optional[str]): The project version.
        description (Optional[str]): The project description.
    """

    def __init__(self, path: Optional[str | Path] = None):
        """
        Initializes the PyprojectInfo instance and attempts to parse the file.

        :param path: Optional path to the pyproject.toml file.
                     Defaults to "pyproject.toml" in the current directory.
        :raises FileNotFoundError: If the file does not exist.
        :raises PyprojectParseError: If the file is not a valid TOML file.
        """
        self.path: Path = Path(path).resolve() if path else Path("pyproject.toml").resolve()
        self.name: Optional[str] = None
        self.version: Optional[str] = None
        self.description: Optional[str] = None

        self._parse_pyproject()

    def _parse_pyproject(self) -> None:
        """Parses the pyproject.toml file and extracts relevant project information."""
        if not self.path.exists():
            raise FileNotFoundError(f"Error: The file '{self.path}' was not found.")

        try:
            with self.path.open("rb") as f:
                data = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise PyprojectParseError(f"Error: Failed to parse TOML file '{self.path}': {e}") from e

        project = data.get("project", {})
        self.name = project.get("name")
        self.version = project.get("version")
        self.description = project.get("description")

    def __repr__(self) -> str:
        """Returns a string representation of the PyprojectInfo instance."""
        return f"PyprojectInfo(name={self.name}, version={self.version}, description={self.description})"

    def is_valid(self) -> bool:
        """Checks if the required project information is available."""
        return self.name is not None and self.version is not None