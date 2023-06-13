import yaml, os
from collections import defaultdict

def find_matching_tuples(lst):
    groups = defaultdict(list)
    for t in lst:
        groups[t[0]].append(t)

    matching_groups = [v for v in groups.values() if len(v) > 1]

    return matching_groups

def dialogue(l: list):
    run = True
    while run:
        question = ' or '.join([f"{i[1:]}" for i in l])
        answer = input(f"{question}?\n(write the answer with the serial number of the variant): ")
        print()
        try:
            result = int(answer)
            if result <= len(l):return result-1
        except:
            pass

def load_file(name):
    with open(name, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    main_folder = os.path.dirname(os.path.abspath(__file__))

    minecraft_languages = load_file(main_folder+"\\minecraft_languages.txt").split("\t")
    google_languages = load_file(main_folder+"\\google_languages.txt").replace("\n", "\t").split("\t")
    #print(minecraft_languages, google_languages)
    
    language = minecraft_languages[3::8]
    in_game = minecraft_languages[4::8]
    s_list = list(zip(language, in_game))
    
    g_language = google_languages[0::2]
    g_code = google_languages[1::2]
    g_list = list(zip(g_language, g_code))

    result = []

    for google_lang, google_code in g_list:
        for mc_lang, mc_code in s_list:
            if google_lang in mc_lang:
                result.append((google_lang, mc_lang, google_code, mc_code))

    
    for variants in find_matching_tuples(result):
        del variants[dialogue(variants)]
        for i in variants:
            result.remove(i)
    
    saving = [(google_lang, {"google_code": google_code, "mc_code": mc_code}) for google_lang, mc_lang, google_code, mc_code in result]

    save = dict(saving)
    with open("supported_languages.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(save, f, encoding="utf-8")