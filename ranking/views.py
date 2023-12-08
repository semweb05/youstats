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


def rank_by_subscribers(request):  # pake filter contains
    graph = GraphLoader().graph

    query = prefix + """
            SELECT DISTINCT ?uri ?rank ?title ?subscribers ?subscribers_for_last_30_days ?channel_type ?created_date 
            WHERE {{
                ?uri :Title ?title ;
                :rank ?rank ;
                :subscribers ?subscribers ;
                :channel_type ?channel_type ;
                :subscribers_for_last_30_days ?subscribers_for_last_30_days ;
                :created_date ?created_date .

        }}
        ORDER BY desc(?subscribers)
        LIMIT 100
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
            "subscribers_for_last_30_days": row.subscribers_for_last_30_days,
            "created_date": row.created_date
        })

    context = {'rdf_data': res}

    return render(request, 'ranking.html', context)

def rank_by_viewers(request):  # pake filter contains
    graph = GraphLoader().graph

    query = prefix + """
            SELECT DISTINCT ?uri ?rank ?title ?video_views ?video_views_for_the_last_30_days ?channel_type ?created_date 
            WHERE {{
                ?uri :Title ?title ;
                :rank ?rank ;
                :video_views ?video_views ;
                :channel_type ?channel_type ;
                :video_views_for_the_last_30_days ?video_views_for_the_last_30_days ;
                :created_date ?created_date .

        }}
        ORDER BY desc(?video_views)
        LIMIT 100
        """

    qres = graph.query(query)
    res = []
    for row in qres:
        res.append({
            "uri": row.uri.split('/')[-1],
            "title": row.title,
            "rank": row.rank,
            "video_views": row.video_views,
            "channel_type": row.channel_type,
            "video_views_for_the_last_30_days": row.video_views_for_the_last_30_days,
            "created_date": row.created_date
        })

    context = {'rdf_data': res}

    return render(request, 'ranking.html', context)