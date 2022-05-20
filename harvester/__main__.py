from datetime import datetime
from pathlib import Path
from typing import Union

import click
import pandas as pd


@click.command()
@click.option(
    "-d", "--directory", default="./", help="Provide the directory to scan for files"
)
@click.option("-o", "--output", default="./", help="Specify the output CSV location")
def harvester(directory: Union[Path, str], output: Union[Path, str]):
    """
    Performs the harvesting of netCDF files within a user-defined directory.

    Args:
        directory (Union[Path, str]): Input directory containing the netCDF files
        output (Union[Path, str]): Directory
    """
    check_directories(directory, output)

    filename_data = scan_directory(directory)

    output_csv(filename_data, output)


def check_directories(directory: Union[Path, str], output: Union[Path, str]):
    """
    Checks if the user-defined directories are existing directories

    Args:
        directory (Union[Path, str]): Input directory containing the netCDF files
        output (Union[Path, str]): Directory
    """

    # Check if input directory is a valid directory
    if not Path.is_dir(Path(directory)):
        raise click.UsageError(f"{directory} is not an existing directory")

    # Check if output directory is a valid directory
    if not Path.is_dir(Path(output)):
        raise click.UsageError(f"{output} is not an existing directory")


def scan_directory(directory: Union[Path, str]):
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
            filename_data.append(fetched_data)

    harvested_data = pd.DataFrame(
        filename_data, columns=["absolute_path", "NAME", "CINE", "DATE"]
    )

    return harvested_data


def fetch_data(file: Path):
    """
    Reads the file name and returns a list of the data elements found in the file name.

    Args:
        file: Union[Path, str]: File name of a netCDF file

    Returns:
        List[Path, str, str, datetime]
    """
    elements = str(file.name).split("_")

    # File name must contain exactly 3 underscores
    if len(elements) == 4:
        return [
            file,
            elements[0],
            elements[1],
            datetime.date(datetime.fromtimestamp(int(elements[2]))),
        ]
    else:
        return []


def output_csv(harvested_data: pd.DataFrame, output: Union[Path, str]):
    """
    Outputs the nested list of data elements read from the netCDF files into a CSV

    Args:
        harvested_data pd.DataFrame: Data elements from the harvested netCDF files.
        output Union[Path, str]: The output directory for the CSV file.d
    """
    harvested_data.to_csv(Path(output) / "harvested_files.csv", index=False)


if __name__ == "__main__":
    harvester()
