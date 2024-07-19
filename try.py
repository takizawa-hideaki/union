import psycopg2
import pandas as pd
from datetime import datetime
def ket_noi_database(host, database, user, password, port):
    try:
        
        conn = psycopg2.connect(
            host='192.168.160.83',
            database='union_hanbai',
            user='unionplate',
            password='etalpnoinu',
            port='5432'
        )
        print(f"アクセスできました。")
        return conn
    except psycopg2.Error as e:
        print(f"アクセスできませんでした。: {e}")
        return None