import sys
import ray
from morph import morphemes
import os
import pickle
from title import Title

def get_known_db(path):
    known_db = morphemes.MorphDb(path, ignoreErrors=True)
    return known_db


def _generate_title_morphs(path, title_name):
    title = Title(title_name)

    if os.path.isfile(path):
        title.find_morphs_from_file(path)
    else:
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                title.find_morphs_from_file(os.path.join(path, filename))

    return title


def create_morph_file(title, title_name, output_folder):
    if len(title.morphs) > 0:
        pickle.dump(title, open(os.path.join(output_folder, title_name + ".morphdata"), "wb"))

@ray.remote
def create_morph_file_title(path, title_name, output_folder, progress = ""):
    ret = (True,)
    try:
        print(progress + title_name)
        if os.path.exists(os.path.join(output_folder, title_name + ".morphdata")):
            message = title_name + " already exists. Skipping"
            print(message)
            ret = (False, message)
        else:
            title = _generate_title_morphs(
                os.path.join(path, title_name), title_name)
            create_morph_file(title, title_name, output_folder)
    except Exception as e:
        ret = (False, title_name + " | " + (str(e)))
    return ret

def log_generation(results):
    with open('generation_failures.log', "a+") as f:
        for r in results:
            if r[0] == False:
                f.write(r[1]+"\n")

def _generate_collection_morphs(collection_path, output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    assert collection_path != output_folder
    titles = os.listdir(collection_path)
    titles.sort()
    i = 0

    index = 0
    total_titles =  len(titles)
    rets = []


    ray.init()
    t = []
    for title in titles:
        index += 1
        rets.append(create_morph_file_title.remote(collection_path, title, output_folder,f"{100*index/total_titles:.2f}% [{index}/{total_titles}] | {title} "))
    ray.get(rets)
   

def _evaluate_collection_morphs(collection_path, known_db_path):
    known_db = get_known_db(known_db_path)
    stats = {}
    for (dirpath, _, filenames) in os.walk(collection_path):
        for filename in filenames:
            if filename.lower().endswith('.morphdata'):
                title = pickle.load(open(dirpath + "/" + filename, 'rb'))
                line_stats, count_stats = title.evaluate_readability(known_db)
                stats[title.title_name] = {
                    "line": line_stats, "count": count_stats}
    return stats


def into_csv(stats):
    csv = "title,line-readability,morphs-readability\n"
    for title in stats:
        csv += f"{title},{stats[title]['line']},{stats[title]['count']}\n"
    return csv
