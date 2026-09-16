import json
from typing import Dict


class Config:
    @staticmethod
    def get_configuration(file_path: str) -> Dict:
        with open(file_path, "r") as f:
            lines = f.readlines()
        valid_config = ''.join(ln for ln in lines if "#" not in ln)
        config: Dict = json.loads(valid_config)

        return config
