# punk-api-beer-challenge
I like beer so I wanted to analyze them a bit.

I used Python 3.10.8 for this script.

## How to run
Run the following commands:
1. `make venv`
2. `source .venv/bin/activate`
3. `export PYTHONPATH="$PWD"`
4. `make build-all`
5. `make build-docker-image`
6. `make open-db-for-localhost`

### Load data to database.
    python beer_challenge/load.py

### Generate reports
    python beer_challenge/analyze.py

## Scheduling
Run the following commands in crontab:
    0 1 * * * path/to/beer_challenge/analyze.sh >> /path/to/analyze.log 2>&1

The script will run every day at 1:00 AM but folder must be outside of user directories and other restricted ones. I advise you to do it in `/usr/local/bin` for example.
You will be able to see the logs in the `analyze.log` file.