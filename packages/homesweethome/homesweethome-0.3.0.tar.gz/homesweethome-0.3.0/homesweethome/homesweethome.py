import os
import tempfile
from typing import Optional
from pathlib import Path

from dynaconf import Dynaconf
import yaml

import logging

log = logging.getLogger("homesweethome")

class SweetHome:

    def __init__(self, application: str,  base_dir: Optional[Path] = Path.home()):
        # Application name
        self._application = application
        self._application_env_prefix = self._application.upper().replace("-", "")
        
        # Base directory
        base_from_from_env = os.getenv(f"{self._application_env_prefix}_BASEDIR")
        if base_from_from_env:
            self._base_dir = Path(base_from_from_env)
        else:    
            self._base_dir = base_dir

        # Home directory
        self._home_dir = self._base_dir / f".{self._application}"
        self._home_dir.mkdir(parents=True, exist_ok=True)
        
        # YML config file
        self._yml_file = self._home_dir / f"{self._application}.yml"
        self._yml_file.touch(exist_ok=True)

        log.debug(f"Creating Dynaconf from: {self._yml_file}")
        self._dynaconf = Dynaconf(
            settings_files=[self._yml_file],
            envvar_prefix=self._application_env_prefix
        )
        log.debug("Dynaconf created.")
    
    @staticmethod
    def create_temporary(name="test-app"):
        base_dir = Path(tempfile.TemporaryDirectory(dir="/tmp").name)
        return SweetHome(
            name,
            base_dir)

    def read_setting(self, path: str, default=None):
        return self._dynaconf.get(path, default=default)

    def write_setting(self, path: str, value):
        with open(self._yml_file, "r") as file:
            config_yml = yaml.safe_load(file) or {}
            self._set_nested_value(config_yml, path, value)
            with open(self._yml_file, "w") as file:
                yaml.dump(config_yml, file)
                self._dynaconf.reload()

    def _set_nested_value(self, config, key, value):
        keys = key.split(".")
        d = config
        for k in keys[:-1]:  # Traverse until the second-last key
            if k not in d:
                d[k] = {}  # Create a new dictionary if the key doesn't exist
            d = d[k]
        d[keys[-1]] = value  # Set the final key to the value

    def home_dir(self) -> Path:
        return self._home_dir

    def directory(self, config_path: str) -> Path:
        directory = self._home_dir / config_path
        directory.mkdir(parents=True, exist_ok=True)
        return directory
