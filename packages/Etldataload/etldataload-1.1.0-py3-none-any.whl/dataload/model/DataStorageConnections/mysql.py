import pandas as pd
import dataload.utils.logger as l
import dataload.conf.model.connection as con
import dataload.model.datastorageconnection as src

# from mysql.connector import Error, connect
from sqlalchemy import create_engine

class MYSQLSource(src.DataStorageConnection):
    def __init__(self, source):
        self.logger = l.Logger()

        self.mysql_connect = con.Mysql(
            host=source['HOST'],
            user=source['USER'],
            password=source['PASSWORD'],
            port=source['PORT'],
            database=source['DATABASE']
        )
        self.connection = con.Connection(
            alias=source['ALIAS'],
            type='MYSQL',
            mysql=self.mysql_connect
        )

    def read_data(self, query=None):
        self.logger.debug('lecture de la source MYSQL....')
        engine = None
        try:
            user=self.connection.mysql.user
            password=self.connection.mysql.password
            host=self.connection.mysql.host
            database=self.connection.mysql.database
            db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            engine = create_engine(db_uri)
            df = pd.read_sql(self.connection.query, engine)
            return df

        except Exception as e:
            print(f"Erreur lors de la lecture de la base de données : {e}")

        finally:
            engine.dispose()

    def write_data(self, df=None, table=None):
        self.logger.debug('ecriture des données dans la BDD Mysql....')
        engine = None
        try:
            user = self.connection.mysql.user
            password = self.connection.mysql.password
            host = self.connection.mysql.host
            database = self.connection.mysql.database
            db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            engine = create_engine(db_uri)

            existing_data = pd.read_sql_table(table, engine)
            key_columns = ['Coin', 'Timestamp']
            if not all(col in df.columns for col in key_columns):
                raise ValueError("Les colonnes {} ne sont pas présentes dans le DataFrame".format(key_columns))
            if not all(col in existing_data.columns for col in key_columns):
                raise ValueError(
                    "Les colonnes {} ne sont pas présentes dans le DataFrame existing_data".format(key_columns))
            new_rows = df[~df.set_index(key_columns).index.isin(existing_data.set_index(key_columns).index)]
            if not new_rows.empty:
                new_rows.to_sql(table, con=engine, if_exists='append', index=False)

            print(f"Données insérées dans la table {table}.")

        except Exception as e:
            print(f"Erreur lors de l ecriture de la base de données : {e}")

        finally:
            engine.dispose()