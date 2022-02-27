from jproperties import Properties
from pathlib import Path
from dataclasses import dataclass


@dataclass
class KryptoProperties:

    db_url: str

    @staticmethod
    def load_properties():
        """todo"""
        configs = Properties()
        with open(Path('utils/krypto.properties'), 'rb') as config_file:
            configs.load(config_file)
            KryptoProperties.db_url = configs.get("db_url").data
