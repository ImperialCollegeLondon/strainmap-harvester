import os.path
from datetime import datetime
from os import path

import click
import pandas as pd


@click.command()
@click.argument("directory")
def harvester(directory):
    directory_encoded = os.fsencode(directory)

    # Check if argument is a valid directory
    if not path.isdir(directory_encoded):
        raise click.UsageError(directory + " is not an existing directory")

    parsed_files = pd.DataFrame(columns=["absolute_path", "NAME", "CINE", "DATE"])

    for file in os.listdir(directory_encoded):
        filename = os.fsdecode(file)

        if filename.endswith(".nc"):
            # We can split the filename to extract the data we need
            elements = filename.split("_")

            new_row = pd.DataFrame(
                [
                    [
                        os.fsdecode(os.path.abspath(file)),
                        elements[0],
                        elements[1],
                        datetime.date(datetime.fromtimestamp(int(elements[2]))),
                    ]
                ],
                columns=["absolute_path", "NAME", "CINE", "DATE"],
            )

            parsed_files = pd.concat([parsed_files, new_row])

    parsed_files.to_csv(os.path.join(directory, "harvested_files.csv"), index=False)


if __name__ == "__main__":
    harvester()
