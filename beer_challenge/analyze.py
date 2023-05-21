import logging
from typing import Dict, Any

from sqlalchemy.types import DOUBLE_PRECISION

from beer_challenge.db_connector import PostgresConnector


def main():
    # From the collected beers what is the min, max and average abv.
    with PostgresConnector() as pg:
        pg.run_command_from_file('beer_challenge/queries/abv_stats.sql')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    main()
