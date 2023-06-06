import os
import yaml

class YAMLFileManager:
    """Class for managing YAML files in a directory."""

    def __init__(self, directory, file_name=None):
        self.set_directory(directory)
        self.set_file_name(file_name)
    
    def set_file_name(self, file_name):
        """Set the file name."""

        if file_name is None:
            self._file_name = None
        elif isinstance(file_name, str):
            if not file_name.endswith('.yaml'):
                file_name += '.yaml'
            self._file_name = file_name
        else:
            raise TypeError("File name must be a string.")
    
    def set_directory(self, directory):
        """Set the directory."""

        if isinstance(directory, str):
            if os.path.isdir(directory):
                self._directory = directory
            else:
                raise NotADirectoryError(f"Directory '{directory}' does not exist.")
        else:
            raise TypeError("Directory must be a string.")
    
    def get_file_name(self):
        return self._file_name
    
    def get_directory(self):
        return self._directory
    
    def load_file(self):
        """Load the YAML file and return its contents as a Python object."""

        if self._file_name is not None:
            file_path = os.path.join(self._directory, self._file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding="utf-8") as file:
                    return yaml.safe_load(file)
            else:
                raise FileNotFoundError(f"File '{self._file_name}' does not exist in '{self._directory}'")
        else:
            raise ValueError("No file name specified.")
    
    def write_to_file(to_yaml):
        """Writes the passed values to a file."""

        with open('sw_templates.yaml', 'w', encoding="utf-8") as f:
            yaml.dump(to_yaml, f)
    
    def get_yaml_files(self):
        """Get the names of all YAML files in the directory."""

        file_names = [file for file in os.listdir(self._directory) if file.endswith('.yaml')]
        
        return file_names

if __name__ == "__main__":
    maneger = YAMLFileManager("./lang", "ru")
    print(maneger.load_file())