from YAMLFileManager import YAMLFileManager

class DataFileManager():
    def __init__(self, main_folder):
        self.main_folder = main_folder
    
    def get_data(self):
        pass

if __name__ == "__main__":
    maneger = YAMLFileManager("/lang", "ru")
    print(maneger.load_file())