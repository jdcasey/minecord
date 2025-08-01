
import os
import yaml
from typing import Dict, Any, List
from .config import DEFAULT_ADMINS_YAML

KEY_ROLE = 'role'
KEY_DISPLAY_NAME = 'display-name'

ROLE_ROOT = 'root'
ROLE_DELEGATE = 'delegate'
ROLES = [ROLE_ROOT, ROLE_DELEGATE]

class Admins:

    def __init__(self, path:str):
        if path is None:
            self.path = DEFAULT_ADMINS_YAML
        else:
            self.path = path

        self._load()

    async def check_authorization(self, interaction, command: str) -> bool:
        """
        Check if the user is authorized to run admin commands.
        
        Args:
            interaction: Discord interaction object
            command: Name of the command being executed
            
        Returns:
            True if authorized, False otherwise (and sends denial message)
        """
        print(f"Checking for authorization: {interaction.user.display_name} ({interaction.user.id})")
            
        if self.is_admin(interaction.user.id):
            return True

        print(f"DENIED: {command} was denied to user: {interaction.user.display_name} ({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to access this command. Your attempt has been logged.", ephemeral=True)
        return False
    

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
    
    def can_add_admin(self, user_id: str ) -> bool:
        return self.admins.get(user_id, {}).get(KEY_ROLE, '') == ROLE_ROOT

    def add_admin(self, user_id: str, user_name: str) -> bool:
        if not user_id in self.admins:
            self.admins[user_id] = { KEY_DISPLAY_NAME: user_name, KEY_ROLE: ROLE_DELEGATE }
            self._store()
    
    def _store(self):
        with open(self.path, 'w') as file:
            file.write(yaml.dump(self.admins, indent=2))

    