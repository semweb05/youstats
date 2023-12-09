from django.shortcuts import render
from django.http import HttpResponse
from graph_loader import GraphLoader
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.cache import cache_page

# Create your views here.

endpoint_url = "https://query.wikidata.org/sparql"
prefix = """
PREFIX : <http://localhost:8000/> 
"""


def home(request):
    graph = GraphLoader().graph

    query = prefix + """
            SELECT DISTINCT ?uri ?rank ?title ?subscribers ?country ?channel_type ?created_date 
            WHERE {{
                ?uri :Title ?title ;
                :rank ?rank ;
                :subscribers ?subscribers ;
                :channel_type ?channel_type ;
                :Country ?country ;
                :created_date ?created_date .
            }}
            ORDER BY asc(?rank)
        """

    qres = graph.query(query)
    total_results = list(qres)

    # Number of items to show per page
    items_per_page = 10
    paginator = Paginator(total_results, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)

    try:
        # Get the page of items
        current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        current_page = paginator.page(paginator.num_pages)

    res = []
    for row in current_page.object_list:
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


        res.append({
            "uri": row.uri.split('/')[-1],
            "title": row.title,
            "rank": row.rank,
            "subscribers": int(float(row.subscribers)),
            "channel_type": row.channel_type,
            "country": row.country,
            "wikidata_id": wikidata_id,
            "created_date": row.created_date
        })

    context = {
        'rdf_data': res,
        'wikidata_id': wikidata_id,
        'paginator': paginator,
        'current_page': current_page,
    }

    return render(request, 'main/index.html', context)

def search(request):  # pake filter contains
    title = request.GET.get('title', '')
    country = request.GET.get('country', '')
    channel_type = request.GET.get('channel_type', '')
    graph = GraphLoader().graph

    query = f"""
            {prefix}
            SELECT DISTINCT ?uri ?rank ?title ?subscribers ?video_views ?channel_type ?created_date 
            WHERE {{
                ?uri :Title ?title ;
                :subscribers ?subscribers ;
                :channel_type ?channel_type ;
                :video_views ?video_views ;
                :rank ?rank;
                :created_date ?created_date .
                FILTER regex(?title, "{title}","i")
            }}
        """

    qres = graph.query(query)
    res = []
    for row in qres:
        res.append({"uri": row.uri.split('/')[-1],
                    "channel_type": row.channel_type,
                    "title": row.title,
                    "rank":row.rank,
                    "subscribers": row.subscribers,
                    "video_views": row.video_views,
                    "created_date": row.created_date,
                    })

    context = {'rdf_data': res}

    return render(request, 'main/index.html', context)