from django.shortcuts import render
from django.http import HttpResponse
from graph_loader import GraphLoader
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

# Create your views here.

endpoint_url = "https://query.wikidata.org/sparql"
prefix = """
PREFIX : <http://localhost:8000/> 
"""


def home(request):  # pake filter contains
    graph = GraphLoader().graph

    query = prefix + """
            SELECT DISTINCT ?uri ?rank ?title ?subscribers ?video_views ?channel_type ?created_date 
            WHERE {{
                ?uri :Title ?title ;
                :rank ?rank ;
                :subscribers ?subscribers ;
                :channel_type ?channel_type ;
                :video_views ?video_views ;
                :created_date ?created_date .

        }}
        ORDER BY asc(?rank)
        """

    qres = graph.query(query)
    res = []
    for row in qres:
        res.append({
            "uri": row.uri.split('/')[-1],
            "title": row.title,
            "rank": row.rank,
            "subscribers": row.subscribers,
            "channel_type": row.channel_type,
            "video_views": row.video_views,
            "created_date": row.created_date
        })

    context = {'rdf_data': res}

    return render(request, 'main/index.html', context)