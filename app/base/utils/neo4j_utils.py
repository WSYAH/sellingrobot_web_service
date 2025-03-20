from py2neo import Graph, Node, Relationship,RelationshipMatcher,NodeMatcher

from app.base.utils.base_utils import get_neo4j_config

def connect_neo4j(host, username, password,port):
    """
    获取neo4j连接
    :param host: neo4j ip
    :param username: 用户名
    :param password: 密码
    :param port: 端口
    """
    url="http://"+host+":"+port
    return Graph(url, auth=(username, password))

neo4j_config = get_neo4j_config()
g = connect_neo4j(neo4j_config['neo4j_ip'], neo4j_config['username'], neo4j_config['password'], neo4j_config['port'])

def create_node(graph=g,name=None, type='computer'):
    """
    创建节点
    :param graph: neo4j连接
    :param name: 节点名称
    :param type: 节点类型
    :return:
    """
    node = Node(type, name=name)
    graph.create(node)
    return node

def create_onebyone_relation(graph=g,name1=None,description='0.8',name2=None):
    """
    两个关键词创建关系
    :param graph: neo4j连接
    :param name1: 节点1名称
    :param name2: 节点2名称
    :param description: 关系描述
    :return:
    """
    relation = Relationship(name1,description,name2)
    graph.create(relation)
    return relation

def get_type_all(graph=g,type='computer'):
    """
    获取所有节点
    :param graph: neo4j连接
    :param type: 节点类型
    :return:
    """
    return list(graph.nodes.match(type).all())

def delete_all(graph=g):
    """
    删除所有节点
    :param graph: neo4j连接
    """
    graph.delete_all()

def getallbyname(graph=g,word=None,type='computer'):
    """
    获取有关系的所有节点
    :param graph: neo4j连接
    :param word: 节点名称
    :param type: 节点类型
    :return:
    """
    cypher_ ="MATCH (n)-[r]-(m) WHERE n.name='"+word+"'RETURN type(r) AS type,m.name AS name"
    df = graph.run(cypher_).to_data_frame()
    similist = list(df.to_dict().values()) #.get('name')
    return similist

def changerelationship(graph=g,word1=None,word2=None,description='0.8'):
    """
    修改关系
    :param graph: neo4j连接
    :param word1: 节点1名称
    :param word2: 节点2名称
    :param description: 关系描述
    :return:
    """

    cypher_ ="MATCH (n)-[r]-(m) WHERE n.name='"+word1+"' AND m.name='"+word2+"'\nDELETE r \n CREATE (n)-[r2:`"+description+"`]->(m) RETURN type(r2) AS type "
    return graph.run(cypher_).to_data_frame()

def getallinfo(graph=g):
    """
    获取所有节点和关系
    :param graph: neo4j连接
    :return:
    """
    cypher_ ="MATCH(n)-[r]->(m) RETURN n,m,type(r)"
    return graph.run(cypher_).to_table()