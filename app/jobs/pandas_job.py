import logging

import numpy as np
import os
import pandas as pd
import re

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


class PandasJob:
    def __init__(self):
        pass

    def import_dataframes(
        self, subdirectory="/input", skiprows=[], parse_dates=None, verbose=0
    ) -> pd.DataFrame:
        """
        Import all '.txt' file from the sub directory folder. Input is a
        directory path. The output is a list of dataframes.

        Parameter
        ----------
        path: Path to the directory with dataframe.
        """
        self.dfs = {}
        path = os.getcwd() + subdirectory
        for path, dirc, files in os.walk(path):
            for file in files:
                if ".txt" in file:

                    # Read dataframe
                    file_path = path + "/" + file
                    log.info(f"reading: {file}")
                    df = pd.read_csv(
                        file_path,
                        skiprows=skiprows,
                        parse_dates=parse_dates,
                        sep=r"[|,]",
                    )
                    log.info(f"completed: {file}, shape: {df.shape}")

                    # adding source column
                    df["source"] = file
                    self.dfs[file] = df

    def concat_dataframes(self, pattern: str) -> pd.DataFrame:
        """Concatenate dataframe from files that match the regex pattern

        Args:
            pattern (str): regex file pattern of the dataframes.

        Returns:
            pd.DataFrame: concatenated dataframe.
        """

        dataframes = []
        for path, df in self.dfs.items():
            regexp = re.compile(pattern)
            if regexp.search(path):
                log.info("concatenating: {file}")
                dataframes.append(df)

        self.concat_df = pd.concat(dataframes)
        log.info(f"completed: {self.concat_df.shape}")

        # TODO: remove debug statement
        # print(self.concat_df.head(10))

    def merge_material_dataframe(self):
        """Merge material dataframe to consolidated dataframe."""

        self.concat_df = self.concat_df.merge(
            self.dfs["material_reference.txt"].drop("source", axis=1),
            left_on="material_id",
            right_on="id",
        ).drop("id", axis=1)

    def filter_low_worth(self):
        """Remove low worth products from the dataframe"""

        self.concat_df = self.concat_df.drop(
            self.concat_df[
                (self.concat_df["worth"] <= 1)
                & (self.concat_df["source"] == "sample_data.1.txt")
            ].index,
            axis=0,
        )

    def recalculate_true_worth(self):
        """Recalulate worth for a subset of the consolidated dataframe"""

        self.concat_df["old_worth"] = self.concat_df["worth"]
        self.concat_df.loc[
            (self.concat_df["source"] == "sample_data.3.txt"), "worth"
        ] = (self.concat_df["material_id"] * self.concat_df["old_worth"])

        self.concat_df = self.concat_df.drop("old_worth", axis=1)

    def write_dataframe(self, path="./output/consolidated_output.1.csv"):
        """Write dataframe to output diretory.

        Args:
            path (str, optional): _description_.
                Defaults to "./output/consolidated_output.1.csv".
        """
        self.concat_df.to_csv(path, index=False)

    # TODO: Complete push to database function.
    # def push_to_db(
    #     self,
    #     df: pd.core.frame.DataFrame,
    #     db_table: str,
    #     db_name: str,
    #     dtype=None,
    #     host="localhost",
    #     port="3306",
    #     db_username=None,
    #     db_password=None,
    #     encode=True,
    #     if_exists="replace",
    #     verbose=0,
    # ):
    #     """
    #     Push dataframe to mysql databas.
    #     """
    #     pass