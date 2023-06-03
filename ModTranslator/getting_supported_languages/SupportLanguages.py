
from googletrans import LANGUAGES
import json
dir = '/'.join(__file__.split('\\')[:-1])

with open(dir+r"/supported_languages_Minecraft.json", 'r', encoding="utf8") as f:
    SUPPORT_LANGUAGES_MINECRAFT = json.loads(f.read())

#print(LANGUAGES)