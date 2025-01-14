from django.apps import AppConfig
import pandas as pd
from sqlalchemy import create_engine
from src.FarsiAid_website import secret


def create_excel_from_database():

    db_url = f"mysql+mysqlconnector://{secret.DB_USER}:{secret.DB_PASSWORD}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}"
    engine = create_engine(db_url, connect_args={"ssl_ca": "/path/to/ca-certificate.crt"})
    print("start read.")
    query = "SELECT word FROM G2_5_dataset"
    df = pd.read_sql(query, con=engine)
    print("start write.")
    file_path = (r"src\group5\logic\confs\resource\updated_persian_dic3"
                 r".xlsx")
    df.to_excel(file_path, index=False, header=False, sheet_name='Words', engine='openpyxl')

    print(f"Saved Successfully.")


class Group5Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group5'

    # def ready(self):
    #     create_excel_from_database()
