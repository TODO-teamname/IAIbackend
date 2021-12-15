from ..mooclet_connector import MoocletConnector
from abc import ABC, abstractmethod

class DataPipeline(ABC):
    def __init__(self, mooclet_connector: MoocletConnector):
        self.mooclet_connector = mooclet_connector
        self.output_data = {}

    @abstractmethod
    def get_output(self, filename=None):
        raise NotImplementedError






