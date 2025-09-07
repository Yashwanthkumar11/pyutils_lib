import os
from dataclasses import dataclass
from abc import ABC, abstractmethod

from pyutils_lib_modules.services.config_manager import ConfigManager

@dataclass
class AbstractReport(ABC):
    report_name:str                 = None
    file_name:str                   = None

    @abstractmethod
    def generate(self):
        raise Exception("generate method not implemented")

    @abstractmethod
    def write(self):
        raise Exception("write method not implemented")

