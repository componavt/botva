Download Pywikibot to this folder from site:
https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation








-------- Misc notes & ideas --------------

argument every time you run the bot:
"-dir:/data/all/projects/git/botva/pywikibot/aka_scripts" 

or set the environment variable "PYWIKIBOT2_DIR" equal to this
directory name in your operating system


python pwb.py login -dir:/data/all/projects/git/botva/pywikibot/aka_scripts

pwb.py listpages -lang:ru -weblink:"petrsu.ru

python pwb.py listpages -lang:en -catr:Programming_languages -limit:7
2939 pages, faile, list is very noisy

+ filter by Wikidata: instance of=programming language


----------- List of pages in Category:Russian mathematicians (Категория:Математики России) -----

python pwb.py listpages -lang:ru -catr:Математики_Российской_империи -limit:7
python pwb.py listpages -lang:ru -catr:Математики_СССР -limit:7
python pwb.py listpages -lang:ru -catr:Математики_России -limit:7

let's create three lists in text files
cd ruwiki
python pwb.py listpages -lang:ru -catr:Математики_Российской_империи -limit:7 > ruwiki_Imperial_Russian_mathematicians.txt
python pwb.py listpages -lang:ru -catr:Математики_СССР -limit:7
python pwb.py listpages -lang:ru -catr:Математики_России -limit:7
