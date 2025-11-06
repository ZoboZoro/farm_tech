
import logging
import time

import pandas as pd
import psycopg2
import requests
from sqlalchemy import create_engine

from utils.dockerconfig import DBNAME, HOST, KEY, LOG_FILE, SQL_FILE, USER, PASS, PORT

# Set logs destination
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s:%(levelname)s:%(message)s',
    level=logging.INFO
    )


# Define database connection and set up table(s)
time.sleep(5)

def db_setup() -> None:
    """ Function to setup postgresql schema and table """
    conn = None
    try:
        logging.info("Initializing database setup...")
        conn = psycopg2.connect(
            database=DBNAME,
            user=USER,
            password=PASS,
            host=HOST,
            port=PORT
            )

        # Open a cursor to perform database operations
        cur = conn.cursor()
        # Execute a query
        with open(SQL_FILE, 'r') as file:
            script = file.read()

        cur.execute(script)
        conn.commit()
    except Exception as e:
        logging.info(f"An error has occurred:", {e})
    finally:
        if conn:
            cur.close()
            conn.close()
            logging.info("Connection closed.")


# Setup extraction and load pipeline
url = "https://api.apitube.io/v1/news/everything"
querystring = {
    "language.code": "en",
    "category.id": ("medtop:20000759,medtop:20000210"),
    "published_at.start": "2025-01-01",
    "per_page": 10,
    "api_key": KEY,
    }
engine = create_engine(f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DBNAME}")
schema = "silver"
table = "news"


def extract_load(
        url,
        table,
        connection,
        schema="",
        api_params={},
        ) -> None:
    """ Function to extraact and load from API to postgres """

    results = []
    try:
        response = requests.get(url, api_params)
        if "not_ok" in response.text:
            logging.info(f"Status code error has been encountered: \
                         {response.json()['errors'][0]['status']}")
        else:
            page = 1
            logging.info(f"Now ingesting data on page: {page}...")
            data = response.json()
            dataframe = pd.json_normalize(data['results'])

            results.append(dataframe)

            # ingest new data while new page exists
            # and append the dataframe to existing list

            while data.get('has_next_pages'):
                response = requests.get(data['next_page'])
                page += 1
                logging.info(f"Now ingesting data on page: {page}...")
                data = response.json()
                dataframe = pd.json_normalize(data['results'])
                results.append(dataframe)
            logging.info("No next page. Combining data")

    except requests.exceptions.RequestException as e:
        logging.error(
            f"An exception during API request has been encountered: {e}"
            )
    except Exception as e:
        logging.exception(f"An exception has been encountered: {e}")
    finally:
        if results:
            results_df = pd.concat(results, axis=0, ignore_index=True)
            results_df.drop(
            ['categories',
                'topics',
                'industries',
                'entities',
                'summary',
                'keywords',
                'links',
                'media',
                'source.home_page_url',
                'source.domain',
                'author'],
            inplace=True,
            axis=1
            )
            try:
                logging.info(f"Initializing connection to Database: {DBNAME}")
                logging.info(f"Writing {len(results_df)} \
                            records to {schema}.{table}...")
                results_df.to_sql(
                    name=table,
                    con=connection,
                    schema=schema,
                    if_exists="append",
                    chunksize=100000,
                    index=False
                )
                logging.info("Done")
            except Exception as e:
                logging.exception(f" Error with insertion: {e}")
        else:
            logging.warning("No DataFrames to concatenate. Returning empty DataFrame.")
            results_df = pd.DataFrame()
            return results_df

def pipeline():
    db_setup()
    extract_load(
        url=url,
        table=table,
        connection=engine,
        schema=schema,
        api_params=querystring
    )


if __name__ == "__main__":
    pipeline()