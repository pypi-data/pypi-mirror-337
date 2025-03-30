import pandas as pd
import dataload.utils.logger as l
import dataload.conf.model.connection as con
import dataload.model.datastorageconnection as src

import requests

# API REST definition object for connection
class RESTAPISource(src.DataStorageConnection):
    def __init__(self, source):
        self.logger = l.Logger()

        # definition des parameter de la connexion API REST
        self.params = con.Params(
            select=source['PARAMS']['SELECT'],
            where=source['PARAMS']['WHERE']
        )
        self.api_connect = con.RestAPI(
            base_url=source['BASE_URL'],
            authorization=source['AUTHORIZATION'],
            accept=source['ACCEPT'],
            key=source['KEY'],
            param= self.params
        )
        self.connection = con.Connection(
            alias=source['ALIAS'],
            type='RESTAPI',
            restapi = self.api_connect
        )

    def read_data(self, query=None):
        self.logger.debug('lecture de la source RESTAPI....')

        # define connection parameter
        base_url = self.api_connect.base_url
        auth = self.connection.restapi.authorization
        accept = self.connection.restapi.accept

        if (auth is not None) and (accept is not None) :
            headers = {
                'Authorization': auth,
                'accept': accept
            }
        else:
            print("param null dans le header")
            headers = {
                'Authorization': auth,
                'accept': accept
            }

        params = {
            "select": self.connection.restapi.param.select,
            "where": self.connection.restapi.param.where
        }
        serie_key_1 = "MIR1.M.FR.B.L23FRLA.D.R.A.2230U6.EUR.O"

        # api request execution
        session = requests.Session()
        response = session.get(base_url, headers=headers, params=params)

        # process the api result
        if response.status_code == 200:
            data = response.json()
            print(data)
            # Conversion en DataFrame pandas
            df = pd.DataFrame(data)
            # df['time_period_end'] = pd.to_datetime(df['time_period_end'])
            return df
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None