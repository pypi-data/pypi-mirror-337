import logging
from abc import ABC, abstractmethod

from download_boss.util.Logs import Logs


logging.basicConfig(level=Logs.LEVEL, format=Logs.FORMAT)


class AbstractAuthGenerator(ABC):

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def refresh(self):
        pass
