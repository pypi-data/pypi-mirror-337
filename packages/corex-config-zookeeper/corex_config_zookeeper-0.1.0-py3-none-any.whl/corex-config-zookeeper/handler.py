# Handler for zookeeper implementing config interface
from corex.core.interfaces.config import ConfigInterface

class ZookeeperHandler(ConfigInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling config with zookeeper")
