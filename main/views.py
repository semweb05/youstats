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
        LIMIT 200
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