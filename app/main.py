import logging

import numpy as np
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


def main():
    log.info("Done")
    pass


if __name__ == "__main__":
    main()
