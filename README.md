# punk-api-beer-challenge
The Punk API Beer Challenge is a project aimed at collecting and analyzing data from the Punk API, which provides information about various beers. This repository contains the code and resources to fetch data from the Punk API, store it in a PostgreSQL database, and perform analysis on the collected beer data.

## Project Structure
The project is organized into the following components:

load_data.py: Python script to fetch data from the Punk API and store it in a PostgreSQL database.
analyze.py: Python script to analyze the collected beer data from the database.
db_connector.py: Configuration file containing the database connection details.
README.md: Documentation file (you're reading it right now).

## Setup
I used Python 3.10.8 for this script. Run the following commands:
1. `make venv`
2. `source .venv/bin/activate`
3. `export PYTHONPATH="$PWD"`
4. `make build-all`
5. `make build-docker-image`
6. `make open-db-for-localhost`
## Usage
### Load data to database.
    python beer_challenge/load_data.py
### Analyzing Data
    python beer_challenge/analyze.py

## Scheduling
Run the following commands in crontab:
```
0 1 * * * path/to/analyze.sh >> /path/to/analyze.log 2>&1
```

The script will run every day at 1:00 AM but folder must be outside of user directories and other restricted ones. I advise you to do it in `/usr/local/bin` for example.
You will be able to see the logs in the `analyze.log` file.