from django.shortcuts import render
from django.http import HttpResponse
from graph_loader import GraphLoader
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

# Create your views here.

endpoint_url = "https://query.wikidata.org/sparql"
prefix = """
PREFIX : <http://localhost:8000/> 
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX pqn: <http://www.wikidata.org/prop/qualifier/value-normalized/>
PREFIX pqv: <http://www.wikidata.org/prop/qualifier/value/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX prn: <http://www.wikidata.org/prop/reference/value-normalized/>
PREFIX prv: <http://www.wikidata.org/prop/reference/value/>
PREFIX psv: <http://www.wikidata.org/prop/statement/value/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdata: <http://www.wikidata.org/wiki/Special:EntityData/>
PREFIX wdno: <http://www.wikidata.org/prop/novalue/>
PREFIX wdref: <http://www.wikidata.org/reference/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdtn: <http://www.wikidata.org/prop/direct-normalized/>
PREFIX wdv: <http://www.wikidata.org/value/>
"""

wikidata_query = f"""
    SELECT DISTINCT ?country ?countryLabel
    WHERE {{
        ?country wdt:P31 wd:Q6256;  # Instance of country
        rdfs:label ?countryLabel.
        FILTER(LANG(?countryLabel) = "en")
        FILTER regex(?countryLabel, "India","i")
    }}
"""

# Execute the Wikidata Query
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(wikidata_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Debugging: Print the results
print(results)

# Attempt to extract the Wikidata ID
try:
    wikidata_id = results['results']['bindings'][0]['country']['value'].split('/')[-1]
    print("Extracted Wikidata ID:", wikidata_id)
except IndexError:
    print("No results found or issue with result structure.")
except KeyError:
    print("Key 'country' not found in results.")
