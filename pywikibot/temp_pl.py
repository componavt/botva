#!/usr/bin/python3

import pywikibot
#from pywikibot import pagegenerators as pg

#with open('lang_list.rq', 'r') as query_file:
#    QUERY = query_file.read().replace('\n', '')

#wikidata_site = pywikibot.Site("wikidata", "wikidata")
#generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)
#generator = pg.get(QUERY, site=wikidata_site)
#.select(query, full_data=True)



from pywikibot import pagegenerators

site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()

query = 'SELECT ?item ?population WHERE{ ?item wdt:P31 wd:Q515 . ?item wdt:P1082 ?population . FILTER (?population > 100000) MINUS { ?item wdt:P31 wd:Q1549591 }} ORDER BY DESC(?population)'

generator = pagegenerators.WikidataSPARQLPageGenerator(query, site=site)







#for item in generator:
#    print(item)
