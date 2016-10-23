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
