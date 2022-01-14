from app.auth.src.common.rds import RDS
import pandas as pd
from sqlalchemy import create_engine

def insert_malicious_links_in_rds():

    engine = create_engine('postgresql://unicorn:welcome123@mydatabase.cvqngijdukip.us-east-2.rds.amazonaws.com/unicorn_db')
    df = pd.read_csv('./app/auth/src/tools/resources/links_without_http_https.csv')
    df = df.drop(['Unnamed: 0'], axis=1)
    df.columns = ['link', 'class_of_malicious_link']
    print(df.columns)
    df.to_sql('malicious_links', engine, if_exists='append', index=False)
