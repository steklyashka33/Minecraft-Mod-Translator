import glob
import os
import yaml


class MultilingualManager():
    def __init__(self, translations_folder, locale='en'):
        # initialization
        self.data = {}
        self._locale = locale
        file_format = 'yaml'

        # get list of files with specific extensions
        files = glob.glob(os.path.join(translations_folder, f'*.{file_format}'))
        for file in files:
            # get the name of the file without extension, will be used as locale name
            loc = os.path.splitext(os.path.basename(file))[0]
            with open(file, 'r', encoding='utf8') as f:
                self.data[loc] = yaml.safe_load(f)

    def set_locale(self, loc):
        if loc in self.data:
            self._locale = loc
        else:
            print('Invalid locale')

    def get_locale(self):
        return self._locale
    
    def get_localization_data(self):
        if self._locale in self.data:
            return self.data[self._locale]

    def translate(self, key):
        # return the "" instead of translation text if locale is not supported
        if self._locale not in self.data:
            return ""

        text = self.data[self._locale].get(key, key)
        
        return text



if __name__ == "__main__":
    print(MultilingualManager(".").data)
    print(MultilingualManager(".").get_localization_data())
    print(MultilingualManager(".", "ru").translate("hi"))