from django.shortcuts import render
from django.http import HttpResponse
from graph_loader import GraphLoader
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from django.views.decorators.cache import cache_page

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

@cache_page(60 * 60 * 24)
def details(request, ytb):
    graph = GraphLoader().graph
    query = f"""
        {prefix}
        SELECT DISTINCT ?uri ?country ?title ?category ?channel_type ?created_date
                ?rank ?subscribers ?subscribers_for_last_30_days
                ?uploads ?video_views ?video_views_for_the_last_30_days
                ?video_views_rank
        WHERE {{
            ?uri rdf:type :Channel ;
            :Country ?country ;
            :Title ?title ;
            :category ?category ;
            :channel_type ?channel_type ;
            :created_date ?created_date ;
            :rank ?rank ;
            :subscribers ?subscribers ;
            :subscribers_for_last_30_days ?subscribers_for_last_30_days ;
            :uploads ?uploads ;
            :video_views ?video_views ;
            :video_views_for_the_last_30_days ?video_views_for_the_last_30_days ;
            :video_views_rank ?video_views_rank .
        FILTER(?uri = :{ytb})
        }}
        """

    qres = graph.query(query)
    res = []
    for row in qres:
        country_name = row.country

        # Query to retrieve the Wikidata QID for a given country name
        wikidata_query = f"""
            SELECT DISTINCT ?country ?countryLabel
            WHERE {{
                ?country wdt:P31 wd:Q6256;  # Instance of country
                rdfs:label ?countryLabel.
                FILTER(LANG(?countryLabel) = "en")
                FILTER regex(?countryLabel, "{country_name}","i")
            }}
        """

        # Execute the Wikidata Query
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(wikidata_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        wikidata_id = results['results']['bindings'][0]['country']['value'].split('/')[-1]
        print(wikidata_id)
        print(row.country)


        res.append({
            "uri": row.uri.split('/')[-1],
            "title": row.title,
            "rank": row.rank,
            "country": row.country,
            "wikidata_id": wikidata_id,
            "subscribers": int(float(row.subscribers)),
            "channel_type": row.channel_type,
            "category": row.category,
            "uploads": row.uploads,
            "video_views": int(float(row.video_views)),
            "video_views_for_the_last_30_days": int(float(row.video_views_for_the_last_30_days)),
            "video_views_rank": row.video_views_rank,
            "created_date": row.created_date,
            # "highest_monthly_earnings": row.highest_monthly_earnings,
            # "highest_yearly_earnings": row.highest_yearly_earnings,
            # "lowest_monthly_earnings": row.lowest_monthly_earnings,
            # "lowest_yearly_earnings": row.lowest_yearly_earnings,
            "subscribers_for_last_30_days": int(float(row.subscribers_for_last_30_days)),
        })

    context = {'rdf_data': res, 'wikidata_id': wikidata_id}

    return render(request, 'details.html', context)