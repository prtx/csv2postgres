# csv2postgres

Load a csv file to postgres.

## Running it

Clone the repo: 
```
git clone https://github.com/prtx/csv2postgres.git
```

Create virtual environment and install dependencies.
```
virtualenv venv -p /usr/bin/python3.6
source venv/bin/activate
pip install -r requirements.txt
```

Add .env for database connection.

Sample:
```
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test
```

Add data to postgres
```
python csv2pg.py sample.csv
```

**NOTE:** Header should have data-type information. Please refer to [sample.csv](sample.csv)