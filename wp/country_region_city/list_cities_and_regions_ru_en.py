#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywikibot

from pywikibot import pagegenerators

# List of `instances of` "subjects of Russia" 
# https://query.wikidata.org/#SELECT%20%3Fitem%20%3Flabel_en%20%3Flabel_ru%20%3Fadm_territory%20%3Fcountry%0AWHERE%0A%7B%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ515%20%7D%20UNION%20%23%20City%0A%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ1549591%20%7D%20%23%20Big%20city%0A%20%0A%20%3Fitem%20wdt%3AP131%20%3Fadm_territory.%20%23%20located%20in%20the%20administrative%20territorial%20entity%20%28P131%29%20%0A%20%3Fitem%20wdt%3AP17%20%3Fcountry.%20%23%20country%20%28P17%29%20%0A%20%0A%20%3Fitem%20rdfs%3Alabel%20%3Flabel_en%20filter%20%28lang%28%3Flabel_en%29%20%3D%20%22en%22%29.%0A%20%3Fitem%20rdfs%3Alabel%20%3Flabel_ru%20filter%20%28lang%28%3Flabel_ru%29%20%3D%20%22ru%22%29.%0A%7D%20LIMIT%2013
query = ' '.join([
    'SELECT ?item ?label_en ?label_ru ?adm_territory ?country',
    'WHERE { ',
        '{ ?item wdt:P31 wd:Q515 } UNION',  # City
        '{ ?item wdt:P31 wd:Q1549591 }',    # Big city

        '?item wdt:P131 ?adm_territory.',   # located in the administrative territorial entity (P131)
        '?item wdt:P17 ?country.',     # country (P17)

        '?item rdfs:label ?label_en filter (lang(?label_en) = "en").',
        '?item rdfs:label ?label_ru filter (lang(?label_ru) = "ru").',
    '}']) # LIMIT 7

wikidata_site = pywikibot.Site('wikidata', 'wikidata')
generator = pagegenerators.WikidataSPARQLPageGenerator(query, site=wikidata_site)

repo = wikidata_site.data_repository()


mysql_string = """
-- -----------------------------------------------------
-- Table `cities`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cities` ;

CREATE TABLE IF NOT EXISTS `cities` (
  `id` INT NOT NULL,
  `country_id` INT NULL,
  `region_id` INT NULL,
  `name_en` VARCHAR(45) NULL,
  `name_ru` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
"""


line = 'Wikidata City ID | Region ID | Country ID | City name in English | in Russian'
print line

file_out = open('cities.txt', 'w')
file_out.write( line + "\n" )

file_sql = open('cities.sql', 'w')
file_sql.write( mysql_string + "\n" )

sql = "\n-- INSERT INTO cities (id, region_id, country_id, name_en, name_ru) VALUES ...\n"
file_sql.write( sql + "\n" )

region_dict = dict()
#region_dict['Q12'] = {}
#region_dict['Q12']['en'] = 'q12 en'
#region_dict['Q12']['ru'] = 'q12 ru'

for item in generator:
    item.get()
    qcity_id = item.getID()
    city_id  = qcity_id[1:] # removes first character: 'Q123' -> '123'
    sitelinks = item.sitelinks

    if 'enwiki' in sitelinks:
        name_en = sitelinks["enwiki"]
    if "ruwiki" in sitelinks:
        name_ru = sitelinks["ruwiki"]
    else:
        name_ru = name_en

    country = False
    adm_territory = False
    if item.claims:
        claims = item.claims
        if 'P17' in claims: # country
            country = claims['P17']

        if 'P131' in claims: # located in the administrative territorial entity (P131)
            adm_territory = claims['P131']

    if not country: # city should belong to some country
        continue
    qcountry_id = country[0].getTarget().getID()
    country_id = qcountry_id[1:]


    # regions or administrative territorial entity ----------------------------------------
    #
    if not adm_territory: # city should be located in some administrative territorial entity
        continue

    region_item = adm_territory[0].getTarget()
    qregion_id = region_item.getID()
    region_id = qregion_id[1:]

    region_item.get()
    region_sitelinks = region_item.sitelinks

    if "enwiki" not in region_sitelinks:
        continue
    reg_name_en = region_sitelinks["enwiki"]
    if "ruwiki" in region_sitelinks:
        reg_name_ru = region_sitelinks["ruwiki"]
    else:
        reg_name_ru = name_en
    
    if region_id not in region_dict:  # add new (unique) region names in English and Russian to dictionary
        region_dict[ region_id ] = {}
        region_dict[ region_id ]['en'] = reg_name_en
        region_dict[ region_id ]['ru'] = reg_name_ru
        region_dict[ region_id ]['country_id'] = country_id
    # print u'{0} | {1} | {2} '.format(region_id, reg_name_en, reg_name_ru) # debug info
    #
    # -------------------------------------- eo regions or administrative territorial entity

 
    line = u'{0} | {1} | {2} | {3} | {4}'.format(qcity_id, qregion_id, qcountry_id, name_en, name_ru)
    print line
    file_out.write( line.encode('utf-8') + "\n" )

                         # city_id                                             # city_id     country_id
    sql = u"INSERT INTO cities VALUES ({0}, {1}, {2}, '{3}', '{4}');".format(city_id, region_id, country_id, name_en, name_ru)

    file_sql.write( sql.encode('utf-8') + "\n" )

file_out.close()
file_sql.close()



# print regions to region.txt and region.sql 

mysql_string = """
-- -----------------------------------------------------
-- Table `regions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `regions` ;

CREATE TABLE IF NOT EXISTS `regions` (
  `id` INT NOT NULL,
  `country_id` INT NULL,
  `name_en` VARCHAR(45) NULL,
  `name_ru` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
"""

print "\nRegions (administrative territorial entity)\n"

line = 'Wikidata Region ID | Country ID | Region name in English | in Russian'
print line

rfile_out = open('regions.txt', 'w')
rfile_out.write( line + "\n" )

rfile_sql = open('regions.sql', 'w')
rfile_sql.write( mysql_string + "\n" )

sql = "\n-- INSERT INTO regions (id, country_id, name_en, name_ru) VALUES ...\n"
rfile_sql.write( sql + "\n" )


for r in region_dict:
    name_en    = region_dict[r]['en']
    name_ru    = region_dict[r]['ru']
    country_id = region_dict[r]['country_id']
                                            # region_id
    line = u'Q{0} | Q{1} | {2} | {3}'.format( r, country_id, name_en, name_ru)
    print line
    rfile_out.write( line.encode('utf-8') + "\n" )

    sql = u"INSERT INTO regions VALUES ({0}, {1}, '{2}', '{3}');".format(r, country_id, name_en, name_ru)
    rfile_sql.write( sql.encode('utf-8') + "\n" )

rfile_out.close()
rfile_sql.close()
