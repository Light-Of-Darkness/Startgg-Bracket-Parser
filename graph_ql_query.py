import os
from dotenv import load_dotenv
from graphql_query import Operation, Query, Argument, Field
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import argparse

load_dotenv()

apiKey = os.getenv('START_GG_API_KEY')

parser = argparse.ArgumentParser(
    prog='Start.gg Bracket Win Gatherer',
    description='Gets number of wins per registered player in a start.gg bracket'
)

parser.add_argument('-e')
args = parser.parse_args()
print("Bracket URL: {}".format(args.e))
#bracketUrl = 'https://www.start.gg/tournament/mtl-underground-fridays-30/event/street-fighter-6-pc'
bracketUrl = args.e

transport = AIOHTTPTransport(
    url="https://api.start.gg/gql/alpha",
    headers={'Authorization':'Bearer {}'.format(apiKey)}
)

#get the slug from the bracket URL
slug = bracketUrl.replace('https://www.start.gg/', '')

#get an event ID from an event link
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

#print(operation.render())

client = Client(transport=transport, fetch_schema_from_transport=False)

query = gql(operation.render())
result = client.execute(query)
print(result)
eventNum = result['event']['id']
print("Event ID is {}".format(eventNum))

#get all sets for an event ID
queryAllSets = Query(
    name="event",
    arguments=[
        Argument(name="id", value=eventNum)
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

#print(operation.render())

query = gql(operation.render())
result = client.execute(query)
#print(result)

for fSet in result['event']['sets']['nodes']:
    print(fSet)