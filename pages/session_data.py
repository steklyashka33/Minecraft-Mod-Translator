from dataclasses import dataclass

@dataclass
class SessionData:
    #Page1
    path_to_mods: str
    path_to_save: str
    to_language: str
    startwith: str
    
    #Page2
    inactive_files_state: bool = True
    save_untranslated_files: bool = False
    create_subfolder: bool = True
    normal_switches: list[str, bool] = None
    disabled_switches: list[str, bool] = None
    mods_for_translation: list = None

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)