import json
from typing import Dict


class Config:
    @staticmethod
    def get_configuration(file_path: str) -> Dict:
        with open(file_path, "r") as f:
            lines = f.readlines()

        valid_config = ""
        for ln in lines:
            if '#' in ln:
                split_line = ln.split('#')
                ln = split_line[0]
            valid_config += ln
        config: Dict = json.loads(valid_config)

        return config
