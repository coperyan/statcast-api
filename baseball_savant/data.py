from collections import OrderedDict
import pandas as pd
import os
import csv
import time

from .client import BaseballSavant


class BaseballSavantDataException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BaseballSavantData:
    def __init__(self, bsclient, data_directory):
        """Initiatlize Class"""
        self._bsclient = bsclient
        self._bsdata = pd.DataFrame()
        self._modules = list()
        self._data_directory = data_directory
        self._base_directory = os.path.join(data_directory, "data")
        if not os.path.isdir(self._base_directory):
            os.makedirs(self._base_directory)

    def fetch_data(self):
        """This function will be used once we have more
        data sources, imports, etc.
        """
        self._bsdata = self._bsclient.get_data()
        self._modules = zip(["statcast"], [self._bsdata])
        for module_name, module_data in self._modules:
            print(f"Writing data for : {module_name}")
            self._write_to_disk(module_name, module_data)

    def get_data_df(self):
        """Function will return dataframe with yesterday's
        statcast data..
        """
        if not self._bsdata.empty:
            return self._bsdata
        else:
            raise BaseballSavantDataException(
                "The data has not been grabbed yet. Please run BaseballSavantData.fetch_data() first."
            )

    def _write_to_disk(self, module_name, module_data):
        """Write a module to local storage"""
        file = os.path.join(self._base_directory, f"{module_name}.csv")
        write_mode, header = ("a", False) if os.path.isfile(file) else ("w", True)

        if len(module_data) > 0:
            pd.DataFrame(module_data).to_csv(
                path_or_buf=file,
                index=False,
                mode=write_mode,
                header=header,
                quoting=csv.QUOTE_MINIMAL,
            )
