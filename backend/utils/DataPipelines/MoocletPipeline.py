from .DataPipeline import DataPipeline
from ..mooclet_connector import MoocletConnector
import json

class MoocletPipeline(DataPipeline):
    def __init__(self, mooclet_connector: MoocletConnector):
        super().__init__(mooclet_connector)
        self.input_data = mooclet_connector.get_values()

    def _parse_data(self):
        self.output_data = self.input_data


    def get_output(self, file=None):
        self._parse_data()

        if not file:
            return self.output_data
        else:
            file.seek(0)
            json.dump(self.output_data, file)
            file.flush()
            file.seek(0)

