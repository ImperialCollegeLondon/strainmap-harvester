"""Harvester for netCDF files"""

from datetime import datetime
from pathlib import Path
from typing import Union, Tuple

import click
import pandas as pd


@click.command()
@click.option(
    "-d", "--directory", default="./", help="Provide the directory to scan for files"
)
@click.option("-o", "--output", default="./", help="Specify the output CSV location")
@click.option(
    "-f",
    "--filename",
    default="harvested_files.csv",
    help="Specify the output CSV filename",
)
def harvester(
    directory: Union[Path, str], output: Union[Path, str], filename: Union[Path, str]
):
    """
    Performs the harvesting of netCDF files within a user-defined directory.

    Args:
        directory (Union[Path, str]): Input directory containing the netCDF files
        output (Union[Path, str]): Directory of the output CSV file
        filename (Union[Path, str]): Name of the CSV file
    """
    check_directories(directory, output)

    filename_data = scan_directory(directory)

    filename_data.to_csv(Path(output) / filename, index=False)


def check_directories(*directories: Union[Path, str]) -> None:
    """
    Checks if the user-defined directories are existing directories

    Args:
        directories (Union[Path, str]): Directories to check its existence
    """

    for directory in directories:
        # Check if input directory is a valid directory
        if not Path(directory).is_dir():
            raise click.UsageError(f"{directory} is not an existing directory")


def scan_directory(directory: Union[Path, str]) -> pd.DataFrame:
    """
    Recursively scans the directory for files we want harvesting,
    returning a dataframe of data elements from each file.

    Args:
        directory (Union[Path, str]): Input directory containing the netCDF files

    Returns:
        pd.DataFrame
            Columns:
                Name: absolute_path, dtype: str
                Name: NAME, dtype: str
                Name: CINE", dtype: str
                Name: DATE, dtype: datetime
    """

    filename_data = []
    for file in Path(directory).rglob("*_train.nc"):
        fetched_data = fetch_data(file)
        if fetched_data:
            filename_data.append(list(fetched_data))

    harvested_data = pd.DataFrame(
        filename_data, columns=["absolute_path", "NAME", "CINE", "DATE"]
    )

    return harvested_data


def fetch_data(file: Path) -> Tuple[Path, str, str, datetime]:
    """
    Reads the file name and returns a list of the data elements found in the file name.

    Args:
        file: Union[Path, str]: File name of a netCDF file

    Returns:
        Tuple[Path, str, str, datetime]
    """
    elements = str(file.name).split("_")

    # File name must contain exactly 3 underscores
    if len(elements) == 4:
        return (
            file,
            elements[0],
            elements[1],
            datetime.date(datetime.fromtimestamp(int(elements[2]))),
        )
    else:
        return ()




if __name__ == "__main__":
    harvester()
