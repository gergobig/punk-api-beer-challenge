import os
import logging
import requests
import json
from typing import Dict, List, Any

import pandas as pd
from sqlalchemy.types import TEXT, DOUBLE_PRECISION, INTEGER


from beer_challenge.db_connector import PostgresConnector


BASE_URL = 'https://api.punkapi.com/v2/beers'

SCHEMA = {
    'id': INTEGER,
    'name': TEXT,
    'tagline': TEXT,
    'first_brewed': TEXT,
    'abv': DOUBLE_PRECISION,
}

# Please use 0 or 1 values only.
os.environ['is_pandas_allowed'] = str(0)


def main():
    is_pandas_allowed = bool(int(os.getenv('is_pandas_allowed')))
    beers = get_all_beers(1)
    write_data_to_file(beers[:10], 'beer_challenge/check_data.txt')
    create_beers_table(beers, is_pandas_allowed)
    create_food_pairing_table(beers)


def _get_beers(**kwargs) -> List[Dict[str, Any]]:
    response = requests.get(BASE_URL, params=kwargs)
    return response.json() if response.status_code == 200 else None


def _filter_list_of_dicts_by_keys(beers: List[Dict[str, Any]], keys_to_keep: List[str]) -> List[Dict[str, Any]]:
    return [{key: beer[key] for key in keys_to_keep if key in beer} for beer in beers]


def get_all_beers(max_page: int = 10**9) -> List[Dict[str, Any]]:
    all_beers = []
    page=1
    while page <= max_page:
        page_of_beers = _get_beers(per_page=25, page=page)
        if not page_of_beers:
            break
        all_beers.extend(page_of_beers)
        page += 1
    return all_beers


def create_beers_table(beers: List[Dict[str, Any]], is_pandas_allowed: bool) -> None:
    beers = _filter_list_of_dicts_by_keys(beers, ['id', 'name', 'tagline', 'first_brewed', 'abv'])
    with PostgresConnector() as pg:
        pg.run_command_from_file('beer_challenge/queries/create_beers_table.sql')
        pg.load_data(beers, 'beers', SCHEMA, is_pandas_allowed)


def create_food_pairing_table(beers: List[Dict[str, Any]]) -> None:
    beers = _filter_list_of_dicts_by_keys(beers, ['id', 'food_pairing'])
    df = pd.DataFrame(beers, columns = ['id', 'food_pairing']).explode('food_pairing').reset_index(drop=True)
    with PostgresConnector() as pg:
        pg.load_data(df.to_dict(), 'food_pairings', {'id': INTEGER, 'food_pairing': TEXT}, True)


def write_data_to_file(data: List[Dict[str, Any]], file_path: str) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    main()