# Python Test
> Simple Python application using MongoDB

You can find the API doc [here](https://documenter.getpostman.com/view/4045821/RWgxtuNV)

## Preparing the database

### Importing the dataset
```
mongoimport --type csv --headerline -d leandro -c estudantes --file dataset_estudantes.csv
```

### After import
```
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

pip install Flask
pip install pymongo

python after_import.py
```

## Running the app
```
FLASK_APP=main.py flask run
```

If you see the following error:

```
This system supports the C.UTF-8 locale which is recommended.
You might be able to resolve your issue by exporting the
following environment variables:

    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8
```

Just export the variables running.
```
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```
