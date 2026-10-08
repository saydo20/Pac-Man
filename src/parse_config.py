"""Configuration parsing module for game settings."""

import json
from typing import Dict, Any


class Config:
    """Handles loading and validating game configuration from JSON files."""

    @staticmethod
    def get_configuration(file_path: str) -> Dict:
        """Read and validate a JSON configuration file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dictionary of validated configuration values.
        """
        with open(file_path, "r") as f:
            lines = f.readlines()

        valid_config = ""
        for ln in lines:
            if '#' in ln:
                split_line = ln.split('#')
                ln = split_line[0]
            valid_config += ln
        config: Dict = json.loads(valid_config)

        defaul_config: Dict[str, Any] = {}
        defaul_config['highscore_filename'] = "scores.json"
        defaul_config['lives'] = 3
        defaul_config['points_per_pacgum'] = 10
        defaul_config['points_per_super_pacgum'] = 50
        defaul_config['points_per_ghost'] = 200
        defaul_config['level_max_time'] = 90

        try:
            for k, v in config.items():
                if k == 'highscore_filename':
                    if ".json" not in v:
                        config[k] = defaul_config[k]
                    continue
                v = int(v)
                if k == "lives":
                    if v <= 0 or v > 5:
                        config[k] = defaul_config[k]
                elif k == 'points_per_pacgum':
                    if v <= 0 or v > 100:
                        config[k] = defaul_config[k]
                elif k == 'points_per_super_pacgum':
                    if v <= 0 or v > 500:
                        config[k] = defaul_config[k]
                elif k == 'points_per_ghost':
                    if v <= 0 or v > 1000:
                        config[k] = defaul_config[k]
                elif k == 'level_max_time':
                    if v < 90 or v > 9999:
                        config[k] = defaul_config[k]
        except Exception:
            return defaul_config

        return config
