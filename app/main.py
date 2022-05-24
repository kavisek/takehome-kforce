import logging
import numpy as np
import pandas as pd

from jobs.pandas_job import PandasJob
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


def main():

    # Run pipeline
    job = PandasJob()
    job.import_dataframes(subdirectory="/input")
    job.concat_dataframes(pattern=r"_data.*.txt")

    # Bonuses
    job.merge_material_dataframe()
    job.filter_low_worth()
    job.recalculate_true_worth()
    job.write_dataframe()
    # job.push_to_database()


if __name__ == "__main__":
    main()
