from py2neo import Graph, Node, Relationship, NodeMatcher


class Query:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="zx")

    def query(self, cql):
        # find_rela  = test_graph.run("match (n:Person{name:'张学友'})-[actedin]-(m:Movie) return m.title")
        result = []
        find_rela = self.graph.run(cql)
        for i in find_rela:
            result.append(i.items()[0][1])
            # result.append(i.items())
        return result


if __name__ == '__main__':
    SQL = Query()
    # result = SQL.query("match (m:Movie) where m.title='卧虎藏龙' return m.rating")
    result = SQL.query("match (m:Movie)-[:is]->(c:Category)  where m.title='卧虎藏龙' return c")[0]['name']
    print(result)
