import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

df_user = pd.read_csv('user_recommendations.csv')
df_rec_info = pd.read_csv('recommendations_info.csv')
df_user_rec = pd.read_csv('final_recommendations_ids_users.csv')

engine = create_engine('mysql://bcschiffler:6bo@XGXyO8Y3eJpkF8ym@bcschiffler.mysql.eu.pythonanywhere-services.com/bcschiffler$letterboxd?charset=utf8mb4')
with engine.connect() as conn, conn.begin():
    df_user.to_sql('Movie', conn, if_exists='replace')
    df_rec_info.to_sql('Info', conn, if_exists='replace')
    df_user_rec.to_sql('User', conn, if_exists='replace')
