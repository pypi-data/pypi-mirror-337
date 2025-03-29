import json
import pathlib


def recreate_file_structure(
    file_structure: dict[str, dict | list],
    target_path: pathlib.Path,
) -> None:
    for file_path, content in file_structure.items():
        # Create a full path object combining the target and relative file path
        full_path = target_path / pathlib.Path(file_path.strip("/"))
        # Ensure the directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Write the content to the file
        with full_path.open("w") as file:
            json.dump(content, file)
