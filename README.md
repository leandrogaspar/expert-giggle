# Python Test
> Simple Python application usin MongoDB

You can find the API doc [here](https://documenter.getpostman.com/view/4045821/RWgxtuNV)

## Preparing the database

### Importing the dataset
```
mongoimport --type csv --headerline -d leandro -c estudantes --file dataset_estudantes.csv
```

### After import
```
python after_import.py
```

## Running the app
```
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

pip install Flask
pip install pymongo

FLASK_APP=main.py flask run
```
