from pymongo import MongoClient
from py2neo import Node, Relationship, NodeMatcher, Graph
import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mongo_url", type=str, default="localhost")
parser.add_argument("--neo4j_url", type=str, default="bolt://localhost:7687")
parser.add_argument("--neo4j_name", type=str, default="neo4j")
parser.add_argument("--neo4j_password", type=str, default="pkusz")

args = parser.parse_args()

client = MongoClient(args.mongo_url)
graph = Graph(args.neo4j_url, auth=(args.neo4j_name, args.neo4j_password))

matcher = NodeMatcher(graph)
db = client.MedicalKG
collection = db.MedicalKG
# triples = collection.find({})
# nodes = []
# for triple in triples:
#     nodes.append(triple['head'])
#     nodes.append(triple['tail'])
# nodes = list(set(nodes))
# print('there are {} entities in database'.format(len(nodes)))
# print('start creating nodes in neo4j knowledge graph')
# for node in tqdm.tqdm(nodes):
#     graph.merge(Node('Entity', name=node), 'Entity', 'name')
print('start creating relations in neo4j knowledge graph')
triples = collection.find({})
for triple in tqdm.tqdm(triples):
    head_node = matcher.match('Entity', name=triple['head']).first()
    tail_node = matcher.match('Entity', name=triple['tail']).first()
    graph.create(Relationship(head_node, triple['relation'], tail_node))

