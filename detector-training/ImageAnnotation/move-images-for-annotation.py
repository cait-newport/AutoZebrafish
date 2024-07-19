import shutil
import click
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

@click.command()
@click.argument('source_file', type=click.Path(exists=True))
@click.argument('destination_dir', type=click.Path())
def move_images(source_file, destination_dir):
    source_file = Path(source_file)
    destination_dir = Path(destination_dir)
    logging.info(f"Moving images listed in {source_file} to {destination_dir}")
    with open(source_file, "r") as file:
        for line in file:
            file_path = line.strip()
            if Path(file_path).is_file():
                folder_path = Path(file_path).parent
                folder_structure = folder_path.relative_to(folder_path.parent)
                destination_folder = destination_dir / folder_structure
                destination_folder.mkdir(parents=True, exist_ok=True)
                shutil.copy(file_path, destination_folder)

if __name__ == '__main__':
    move_images()
