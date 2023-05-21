import logging
from typing import Dict, Any

from sqlalchemy.types import DOUBLE_PRECISION

from beer_challenge.db_connector import PostgresConnector


def main():
    # From the collected beers what is the min, max and average abv.
    generate_report_table('abv_stats', 'abv_stats', {'min': DOUBLE_PRECISION, 'max': DOUBLE_PRECISION, 'average': DOUBLE_PRECISION})


def generate_report_table(file_name: str, table_name: str, schema: Dict[str,Any]):
    with PostgresConnector() as pg:
        df = pg.select(f'beer_challenge/queries/{file_name}.sql')
        pg.load_data(df, table_name=table_name, schema=schema, is_pandas_allowed=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    main()
