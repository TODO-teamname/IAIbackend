from .DataPipeline import DataPipeline
from ..mooclet_connector import MoocletConnector
import json
import pandas as pd
from typing import TextIO

class MoocletPipeline(DataPipeline):
    def __init__(self, mooclet_connector: MoocletConnector):
        super().__init__(mooclet_connector)
        self.values = mooclet_connector.get_values()

    def _parse_data(self):
        values = pd.DataFrame(self.values["results"])
        values["timestamp"] = pd.to_datetime(values["timestamp"])
        values.sort_values(by=["timestamp"])
        self.output_data = values


    def get_output(self, file: TextIO=None):
        self._parse_data()

        if not file:
            return self.output_data
        else:
            file.seek(0)
            self.output_data.to_csv(file)
            file.flush()
            file.seek(0)

