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
        res.append({
            "uri": row.uri.split('/')[-1],
            "title": row.title,
            "rank": row.rank,
            "country": row.country,
            "subscribers": row.subscribers,
            "channel_type": row.channel_type,
            "category": row.category,
            "uploads": row.uploads,
            "video_views": row.video_views,
            "video_views_for_the_last_30_days": row.video_views_for_the_last_30_days,
            "video_views_rank": row.video_views_rank,
            "created_date": row.created_date,
            "subscribers_for_last_30_days": row.subscribers_for_last_30_days,
        })

    context = {'rdf_data': res}

    return render(request, 'details.html', context)