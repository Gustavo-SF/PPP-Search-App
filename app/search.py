import json
import textwrap

import pyodbc
import pandas as pd
import requests

from config import Config
from app.models import Material

def get_materials_by_id(material: str):
    # Specify the Driver.
    driver = '{ODBC Driver 17 for SQL Server}'

    # Specify Server Name and Database Name.
    server_name = Config.AZURE_SERVER_NAME
    database = Config.DATABASE_NAME

    # Create our Server URL.
    server = f'{server_name}.database.windows.net,1433'

    # Define Username & Password
    login = Config.DB_LOGIN
    password = Config.DB_PASSWORD

    # Create the full connection string.
    connection_string = textwrap.dedent(f'''
        Driver={driver};
        Server={server};
        Database={database};
        Uid={login};
        Pwd={password};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
    ''')
    # Create a new PYODBC Connection Object
    cnxn: pyodbc.Connection = pyodbc.connect(connection_string)

    # Create a new Cursor Object from the connection
    crsr: pyodbc.Cursor = cnxn.cursor()

    # Selection Query
    select_query = f"""
    SELECT material_id, material_description FROM proc_db.zmm001 WHERE material_id IN (SELECT material_prox
    FROM   
    (SELECT * FROM [proc_db].[material_proximity] WHERE material_id = '{material}') AS pivot_proximity
    UNPIVOT  
    (
    material_prox FOR material IN   
        (
        material_id, similar_1, similar_2, similar_3, similar_4, 
        similar_5, similar_6, similar_7, similar_8, similar_9, similar_10
        )  
        ) AS unpivot_proximity
    )
    """

    # We get the first row of data that matches the material
    dataframe = pd.read_sql(select_query, cnxn)

    # Cluster_of_materials
    list_of_materials = [Material(id=row["material_id"], description=row["material_description"]) for i, row in dataframe.iterrows()]

    return list_of_materials


def get_materials_by_query(material: str):
    # Configure headers
    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"Bearer {Config.ENDPOINT_KEY}"

    # Data
    data = {"query": material}
    data = json.dumps(data)

    # Make the request
    resp = requests.post(Config.SCORING_URI, data=data, headers=headers)

    # We get the first row of data that matches the material
    dataframe = pd.DataFrame(json.loads(resp.text))

    # Cluster_of_materials
    list_of_materials = [Material(id=row["material_id"], description=row["material_description"]) for _, row in dataframe.iterrows()]

    return list_of_materials





        

