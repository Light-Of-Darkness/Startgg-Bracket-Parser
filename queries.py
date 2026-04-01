import os
from dotenv import load_dotenv
from graphql_query import Operation, Query, Argument, Field
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import argparse

load_dotenv()

apiKey = os.getenv('START_GG_API_KEY')

transport = AIOHTTPTransport(
    url="https://api.start.gg/gql/alpha",
    headers={'Authorization':'Bearer {}'.format(apiKey)}
)
client = Client(transport=transport, fetch_schema_from_transport=False)


def getEventId(slug):
    eventId = Query(
        name="event",
        arguments=[Argument(name="slug", value='"{}"'.format(slug))],
        fields=["id", "name"]
    )

    operation = Operation(
        type="query",
        name="getEventid",
        queries=[eventId]
    )
    
    query = gql(operation.render())
    result = client.execute(query)
    return result
    

def getSets(eventID):
    queryAllSets = Query(
        name="event",
        arguments=[
            Argument(name="id", value=eventID)
        ],
        fields=["id",
            "name", 
            Field(
                name="sets",
                arguments=[
                    Argument(name='page', value=1),
                    Argument(name='perPage', value=100),
                    Argument(name='sortType', value='STANDARD')
                ],
                fields=[
                    Field(
                        name="pageInfo",
                        fields=["total"]
                    ),
                    Field(
                        name='nodes',
                        fields=[
                            "id",
                            Field(
                                name='slots',
                                fields=[
                                    "id",
                                    Field(
                                        name='entrant',
                                        fields=[
                                            "id",
                                            "name"
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
    operation = Operation(
        type="query",
        name="EventSets",
        queries=[queryAllSets]
    )
    
    query = gql(operation.render())
    result = client.execute(query)
    return result

def getSetScore(_setID):
    querySetScore = Query(
        name="set",
        arguments=[
            Argument(name="id", value=_setID)
        ],
        fields=[
            "id",
            Field(
                name="slots",
                fields= [
                    "id",
                    Field(
                        name="standing",
                        fields=[
                            "id",
                            "placement",
                            Field(
                                name="stats",
                                fields=[
                                    Field(
                                        name="score",
                                        fields=[
                                            "label",
                                            "value"
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
    operation = Operation(
        type="query",
        name="set",
        queries=[querySetScore]
    )
    
    query = gql(operation.render())
    result = client.execute(query)
    return result