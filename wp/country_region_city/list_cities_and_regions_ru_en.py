#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywikibot

from pywikibot import pagegenerators

# List of `instances of` "subjects of Russia" 
# https://query.wikidata.org/#SELECT%20%3Fitem%20%3Flabel_en%20%3Flabel_ru%0AWHERE%0A%7B%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ835714%20%7D%20UNION%20%23%20Oblast%20of%20Russia%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ41162%20%7D%20UNION%20%23%20Republic%20of%20Russia%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ831740%20%7D%20UNION%20%23%20Krai%20of%20Russia%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ309166%20%7D%20UNION%20%23%20Autonomus%20oblast%20of%20Russia%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ184122%20%7D%20%23%20Autonomus%20okrug%20of%20Russia%0A%20%0A%20FILTER%20NOT%20EXISTS%20%7B%3Fitem%20wdt%3AP31%20wd%3AQ19953632%7D%20%23%20Former%20administrative%20territorial%20entity%0A%20%0A%20%3Fitem%20rdfs%3Alabel%20%3Flabel_en%20filter%20%28lang%28%3Flabel_en%29%20%3D%20%22en%22%29.%0A%20%3Fitem%20rdfs%3Alabel%20%3Flabel_ru%20filter%20%28lang%28%3Flabel_ru%29%20%3D%20%22ru%22%29.%0A%7D%20LIMIT%203%0A
query = ' '.join([
    'SELECT ?item ?label_en ?label_ru ?adm_territory ?country',
    'WHERE { ',
        '{ ?item wdt:P31 wd:Q515 } UNION',  # City
        '{ ?item wdt:P31 wd:Q1549591 }',    # Big city

        '?item wdt:P131 ?adm_territory.',   # located in the administrative territorial entity (P131)
        '?item wdt:P17 ?country.',     # country (P17)

        '?item rdfs:label ?label_en filter (lang(?label_en) = "en").',
        '?item rdfs:label ?label_ru filter (lang(?label_ru) = "ru").',
    '}']) #  LIMIT 3

wikidata_site = pywikibot.Site('wikidata', 'wikidata')
generator = pagegenerators.WikidataSPARQLPageGenerator(query, site=wikidata_site)

repo = wikidata_site.data_repository()

line = 'Region ID | Wikidata country ID | Region name in English | in Russian'
print line

wd_Russia_id = 159

file_out = open('regions_of_Russia.txt', 'w')
file_out.write( line + "\n" )
file_sql = open('regions_of_Russia.sql', 'w')

for item in generator:

    item_dict = item.get()
    wikidata_id = item.getID()[1:] # removes first element: 'Q123' -> '123'
    
    name_en = item_dict["sitelinks"]["enwiki"]
    name_ru = item_dict["sitelinks"]["ruwiki"]

    line = u'{0} | 159 | {1} | {2}'.format(wikidata_id, name_en, name_ru)
    print line
    file_out.write( line.encode('utf-8') + "\n" )

                      # wikidata_id
    sql = u"INSERT INTO regions (id, country_id, name_en, name_ru) VALUES ({0}, 159, '{1}', '{2}');".format(wikidata_id, name_en, name_ru)

    file_sql.write( sql.encode('utf-8') + "\n" )

file_out.close()
file_sql.close()
