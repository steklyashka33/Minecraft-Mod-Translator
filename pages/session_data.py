from dataclasses import dataclass
from typing import List, Tuple, Union

@dataclass
class SessionData:
    #Page1
    path_to_mods: str
    path_to_save: str
    to_language: Union[str, None]
    startwith: str
    
    #Page2
    inactive_files_state: bool = True
    save_untranslated_files: bool = False
    create_subfolder: bool = True
    normal_switches: Union[List[Tuple[str, bool]], None] = None
    disabled_switches: Union[List[Tuple[str, bool]], None] = None
    mods_for_translation: Union[list, None] = None

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)