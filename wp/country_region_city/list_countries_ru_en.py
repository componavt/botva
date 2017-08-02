#!/usr/bin/python
# -*- coding: utf-8 -*-

# See https://en.wikiversity.org/wiki/Research_in_programming_Wikidata/Countries

import pywikibot
#from pywikibot import pagegenerators as pg

#with open('lang_list.rq', 'r') as query_file:
#    QUERY = query_file.read().replace('\n', '')

#wikidata_site = pywikibot.Site("wikidata", "wikidata")
#generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)
#generator = pg.get(QUERY, site=wikidata_site)

from pywikibot import pagegenerators

# item is 'country'
# https://query.wikidata.org/#%23List of countries in English and Russian%0ASELECT %3Fcountry %3Flabel_en %3Flabel_ru%0AWHERE%0A{%0A %3Fcountry wdt%3AP31 wd%3AQ6256.%0A %3Fcountry rdfs%3Alabel %3Flabel_en filter (lang(%3Flabel_en) %3D "en").%0A %3Fcountry rdfs%3Alabel %3Flabel_ru filter (lang(%3Flabel_ru) %3D "ru").%0A}
query = 'SELECT ?item ?label_en ?label_ru ' + \
        'WHERE { ' + \
        '  ?item wdt:P31 wd:Q6256.' + \
        '  ?item rdfs:label ?label_en filter (lang(?label_en) = "en").' + \
        '  ?item rdfs:label ?label_ru filter (lang(?label_ru) = "ru").' + \
        '}' # LIMIT 3'

wikidata_site = pywikibot.Site('wikidata', 'wikidata')
generator = pagegenerators.WikidataSPARQLPageGenerator(query, site=wikidata_site)

repo = wikidata_site.data_repository()

line = 'Wikidata_country_ID | Country name in English | in Russian'
print line

file_out = open('countries.txt', 'w')
file_out.write( line + "\n" )
file_sql = open('countries.sql', 'w')

for item in generator:

    item_dict = item.get()
    wikidata_id = item.getID()[1:] # removes first element: 'Q123' -> '123'
    
    name_en = item_dict["sitelinks"]["enwiki"]
    name_ru = item_dict["sitelinks"]["ruwiki"]
    
    line = u'{0} | {1} | {2}'.format(wikidata_id, name_en, name_ru)
    print line
    file_out.write( line.encode('utf-8') + "\n" )
                        # wikidata_id
    sql = u"INSERT INTO countries (id, name_en, name_ru) VALUES ({0}, '{1}', '{2}');".format(wikidata_id, name_en, name_ru)

    file_sql.write( sql.encode('utf-8') + "\n" )
file_out.close()
file_sql.close()

    # print item.properties()
    # print item_dict["sitelinks"]["ruwiki"]
