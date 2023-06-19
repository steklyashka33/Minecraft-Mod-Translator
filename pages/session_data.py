from dataclasses import dataclass

@dataclass
class SessionData:
    path_to_mods: str
    path_to_save: str
    to_language: str
    startwith: str
    
    hide_inactive_file: str = 1
    save_untranslated_files: str = 0
    create_subfolder: str = 1

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)