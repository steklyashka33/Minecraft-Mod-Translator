from dataclasses import dataclass

@dataclass
class SessionData:
    path_to_mods: str
    path_to_save: str
    to_language: str
    startwith: str
    
    inactive_files_state: bool = True
    save_untranslated_files: bool = False
    create_subfolder: bool = True
    mods: list = None

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)