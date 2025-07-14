
import os
import yaml
from typing import Dict, Any, List
from .config import DEFAULT_ADMINS_YAML

class Admins:

    def __init__(self, path:str):
        if path is None:
            self.path = DEFAULT_ADMINS_YAML
        else:
            self.path = path

        self._load()
    

    def _load(self) -> List[str]:
        if not os.path.exists(self.path):
            self.admins = {}
        else:
            with open(self.path, 'r') as file:
                self.admins = yaml.safe_load(file)
                if self.admins is None:
                    self.admins = {}
        
        print(f"Loaded {len(self.admins)} admins from {self.path}.")
        return self.admins
    
    def is_admin(self, user_id: str) -> bool:
        return user_id in self.admins
    
    def add_admin(self, user_id: str, user_name: str) -> bool:
        if not user_id in self.admins:
            self.admins[user_id] = user_name
            self._store()
    
    def _store(self):
        with open(self.path, 'w') as file:
            file.write(yaml.dump(self.admins, indent=2))

    