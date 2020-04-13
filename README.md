# readability

Evaluates the readability level of one or more titles. It uses **known.db** from [MorphMan](https://github.com/kaegi/MorphMan), without the need to interact with Anki.

A nice distant idea would be an online cloud service/database, where any user could submit their own known.db and get recommendation of titles based on their level. Study plans too?
### Some Considerations
1. All the evaluations are handled over unique instances. So if there are  **2 known and equal** lines in a total of 3 lines, the end result would actually be 50%. Same applies to morphs.

2. The reason for **morphdata** type is to save on time when evaluating large lists of titles. (And still, it is quite slow over large collections)/

3. If one wishes to use the server.py, one has to put all collections (in morphdata) in the folder **library** (or link it there). I'll try to be updating this library [Link](asd). In the repo there are two titles as an example. It was an automated job with scraping all subs from the japanese shows on **kitsunekko net** nad using the **generate_collection_morphs** command.
```
library/
library/anime/
library/anime/DeathNote.morphdata
library/book/
library/book/時の凱歌.txt.morphdata
```

4. Again, large libraries do take a bit of time, depending on the size.

### Available commands:
* **server.py** : serves a local page where one can submit their **known_db** and have an evaluation over the total library. It comes with a table with basic sorting and filtering capabilities. (Check point 3. from before.)
```
python3 server.py
```

* **raw_analysis**: looks into one folder, extracts the morphs for every text file of the folder and makes an evaluation. It presents the results, and the files it looked into.
```
$ python3 main.py raw_analysis known.db folder_with_subtitles
        ['Mob_Psycho_100_024.srt', 'Mob_Psycho_100_010.srt', 'Mob_Psycho_100_022.srt', 'Mob_Psycho_100_018.srt', 'Mob_Psycho_100_021.srt', 'Mob_Psycho_100_019.srt', 'Mob_Psycho_100_013.srt', 'Mob_Psycho_100_017.sr
t', 'Mob_Psycho_100_023.srt', 'Mob_Psycho_100_012.srt', 'Mob_Psycho_100_009.srt', 'Mob_Psycho_100_014.srt', 'Mob_Psycho_100_020.srt', 'Mob_Psycho_100_011.srt', 'Mob_Psycho_100_015.srt', 'Mob_Psycho_100_016.srt']

        Mob Psycho 100
        Line Readability  5%
        Morph Readability 15%
        
```

* **generate_title_morphs**: it generates a data file with all the morphs present in a folder. Similar to **raw_analysis**, but it makes no analyzis and saves the extracted morphs for future use in a "morphdata" type.
```
 $ python3 main.py generate_title_morphs folder_with_subtitles title_name output_folder
 $ ls output_folder/title_name.morphdata
```

* **generate_collection_morphs**: applies **generate_title_morphs** into a folder of titles. It maintains folder structure in a newly given folder. Example:

Before:
```
TVShowCollection/
TVShowCollection/Show1/
TVShowCollection/Show1/e01.srt
TVShowCollection/Show1/e02.srt
TVShowCollection/Show2/
TVShowCollection/Show2/e03.ass
TVShowCollection/Show3.ass
```
```
generate_collection_morphs TVShowCollection output_folder
```
```
output_folder/
output_folder/Show1.morphdata
output_folder/Show2.morphdata
output_folder/Show3.morphdata
```

* **evaluate_title_morphs**: makes an analysis over a single morphdata file. Output similar to the one from **raw_analysis**.
```
$ python3 main.py evaluate_title_morphs known_db_path, morphdata_path
```
* **evaluate_collection_morphs**: makes an analysis over a folder like the one created at **generate_collection_morphs**. It outputs a csv format text with a list of all readability levels.
```
$ python3 main.py known_db_path collection_path
title,line-readability,morphs-readability
Death Note,0.05,0.12
Boku No Hero Academia,0.07,0.16
```

