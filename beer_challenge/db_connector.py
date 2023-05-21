import logging
from typing import Dict, List, Any

import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from psycopg2.extras import execute_batch


class PostgresConnector:
    def __init__(self, host='localhost', database='punk_api', user='gbig', password='gbig'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def __enter__(self):
        logging.info('Opening connection.')
        self.conn = psycopg2.connect(
            host=self.host, database=self.database, user=self.user, password=self.password
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        logging.info('Changes has been committed.')
        self.conn.close()
        logging.info('Connection closed.')

    def __read_query_from_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf8') as f:
            return ' '.join(f.readlines()).replace('\n', '')

    def __load_data_with_pandas(self, data: List[Dict[str, Any]], table_name: str, schema: Dict[str, str]):
        engine = create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:5432/{self.database}'
        )
        pd.DataFrame(data).to_sql(
            f'{table_name}_pandas',
            engine,
            if_exists='replace',
            index=False,
            dtype=schema,
        )
        logging.info(f'Data has been loaded to {table_name} table with pandas.')

    def __load_data_with_psycopg2(self, data: List[Dict[str, Any]], table_name: str, schema: Dict[str,str]):
        columns = schema.keys()
        values = [tuple(d.values()) for d in data]

        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        with self.conn.cursor() as cur:
            execute_batch(cur, query, values)
        logging.info(f'Data has been loaded to {table_name} table with psycopg2.')

    def load_data(self, data: List[Dict[str, Any]], table_name: str, schema: Dict[str,str], is_pandas_allowed: bool):
        if is_pandas_allowed:
            self.__load_data_with_pandas(data, table_name, schema)
            return
        self.__load_data_with_psycopg2(data, table_name, schema)

    def run_command_from_file(self, file_path: str) -> int:
        query = self.__read_query_from_file(file_path)
        with self.conn.cursor() as cur:
            cur.execute(query)
        logging.info(f'SQL query ({query[:50]}...) has been successfully executed. New row count is: {cur.rowcount}')

    def select(self, file_path: str) -> pd.DataFrame:
        query = self.__read_query_from_file(file_path)
        return pd.read_sql_query(query, self.conn)
