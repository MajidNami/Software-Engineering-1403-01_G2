import os

from django.apps import AppConfig
import pandas as pd
from sqlalchemy import create_engine
from src.FarsiAid_website.secret import *


def create_excel_from_database():
    db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url, connect_args={"ssl_disabled": True})
    print("Start reading data from database...")
    query = "SELECT word FROM G2_5_dataset"
    df = pd.read_sql(query, con=engine)
    file_path = (r"C:\Users\Amir hosein\Desktop\spell-correction\src\group5\logic\confs\resource/updated_persian_dic4"
                 r".xlsx")
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_excel(file_path, index=False, header=False, sheet_name='Words', engine='openpyxl')
    print(f"Data successfully saved to {file_path}")


class Group5Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group5'

    def ready(self):
        create_excel_from_database()
