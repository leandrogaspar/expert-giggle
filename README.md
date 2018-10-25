# expert-giggle

################################################################
    Preparing the database:
################################################################
Importing the dataset:
mongoimport --type csv --headerline -d leandro -c estudantes --file dataset_estudantes.csv

After import:
python after_import.py

################################################################
    Running the app:
################################################################
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

pip install Flask
pip install pymongo

FLASK_APP=main.py flask run
