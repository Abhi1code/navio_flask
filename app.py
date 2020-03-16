from flask import Flask, request, jsonify, json
import logging as logger
import pymysql
import math
import sys
import re
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

logger.basicConfig(level="DEBUG")

app = Flask(__name__)

# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'ips'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# conn = mysql.connect()
# cursor =conn.cursor()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ips'
#db = SQLAlchemy(app)


# class FloorDetails(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     floorid = db.Column(db.Integer, primary_key=False)
#     type = db.Column(db.Integer, primary_key=False)
#     xcord = db.Column(db.Float, nullable=False)
#     ycord = db.Column(db.Float, nullable=False)
#     name = db.Column(db.String(50), nullable=False)
#
# db.create_all()
# if __name__ == '__main__':
#     logger.debug("starting the application")
#     from api import *
#     app.run(host="127.0.0.1", port=5000, debug=True, load_dotenv=True)

@app.route("/", methods=["POST"])
def hello():
    #space = FloorDetails.query.all()
    db = pymysql.connect("localhost", "root", "", "ips")
    cursor = db.cursor()
    sql = "SELECT * FROM `pathdetails` WHERE  `floorid` = %s"
    cursor.execute(sql, (request.json['floorid'],))
    results = cursor.fetchall()
    # for i in results:
    #     print(i[0])

    return jsonify(results)

@app.route("/path", methods=["GET"])
def hello1():
    #space = FloorDetails.query.all()
    db = pymysql.connect("localhost", "root", "", "ips")
    cursor = db.cursor()
    sql = "SELECT * FROM `pathdetails` WHERE  `floorid` = %s"
    cursor.execute(sql, (request.args.get('floorid'),))
    results = cursor.fetchall()
    # for i in results:
    #     print(i[0])

    return jsonify(results)

@app.route("/qrcodes", methods=["GET"])
def hello2():
    #space = FloorDetails.query.all()
    db = pymysql.connect("localhost", "root", "", "ips1")
    cursor = db.cursor()
    sql = "SELECT * FROM `floordetails` WHERE  `floorid` = %s"
    cursor.execute(sql, (request.args.get('id'),))
    results = cursor.fetchall()
    # for i in results:
    #     print(i[0])

    return jsonify(results)

@app.route("/item", methods=["GET"])
def hello3():
    #space = FloorDetails.query.all()
    db = pymysql.connect("localhost", "root", "", "ips1")
    cursor = db.cursor()
    sql = "SELECT * FROM `qrcodedetails` WHERE  `floorid` = %s"
    cursor.execute(sql, (request.args.get('id'),))
    results = cursor.fetchall()
    # for i in results:
    #     print(i[0])

    return jsonify(results)

@app.route("/slots", methods=["GET"])
def hello4():
    #space = FloorDetails.query.all()
    db = pymysql.connect("localhost", "root", "", "ips1")
    cursor = db.cursor()
    sql = "SELECT * FROM `pathslots` WHERE  `floorid` = %s"
    cursor.execute(sql, (request.args.get('id'),))
    results = cursor.fetchall()
    # for i in results:
    #     print(i[0])

    return jsonify(results)

@app.route('/login/', methods=["POST"])
def login_page():

        if request.method == "POST":
            data = request.json['key']
            print(data)
            # attempted_password = request.form['password']
            return "Hello " + data

        if request.method == "GET":
            key = request.json['key']
            # attempted_password = request.form['password']
            return {"message" : "inside post method " + key}


class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printSolution(self, dist):
        for node in range(self.V):
            print(node, "t", dist[node])

    def printTrace(self, trace, src, dst):
        stack = []
        stack.append(dst+1)
        temp = dst
        count = 0
        while temp != src or count > self.V:
            stack.append(trace[temp]+1)
            temp = trace[temp]
            count = count + 1
        # for v in stack:
        #     print(str(stack.pop()) + " ")
        # print(str(stack.pop()) + " ")
        print(stack)
        return stack

    def minDistance(self, dist, sptSet):

        # Initilaize minimum distance for next node
        min = sys.maxsize
        min_index = -1
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

        # Funtion that implements Dijkstra's single source

    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        trace = [-1] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shotest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and \
                        sptSet[v] == False and \
                        dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    trace[v] = u

        #self.printSolution(dist)
        #self.printTrace(trace, src, dst)
        fresult = []
        fresult.append(dist)
        fresult.append(trace)
        return fresult

    def dijkstra1(self, src, dst):

        dist = [sys.maxsize] * self.V
        trace = [-1] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shotest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and \
                        sptSet[v] == False and \
                        dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    trace[v] = u

        #self.printSolution(dist)
        return self.printTrace(trace, src, dst)


@app.route("/algo", methods=["GET"])
def algo():

    db = pymysql.connect("localhost", "root", "", "ips1")
    cursor = db.cursor()
    sql = "SELECT * FROM `pathslots` WHERE  `floorid` = %s"
    cursor.execute(sql, (request.args.get('id'),))
    results = cursor.fetchall()

    sql1 = "SELECT * FROM `pathdetails` WHERE  `floorid` = %s"
    cursor.execute(sql1, (request.args.get('id'),))
    results1 = cursor.fetchall()

    # for i in results:
    #     print(i[0])
    # temp = jsonify(results)
    l = results[len(results)-1][0]
    print(l)
    xlist = [0] * l
    ylist = [0] * l

    for i in results:
        xlist[i[0]-1] = i[2]
        ylist[i[0]-1] = i[3]

    #
    # print(results1)

    graph = [[0 for x in range(l)] for x in range(l)]
    #print(graph)
    for i in results1:
        xcord = xlist[i[2]-1]
        ycord = ylist[i[2]-1]
        xcordf = xlist[i[3] - 1]
        ycordf = ylist[i[3] - 1]
        d = round(math.hypot(xcordf-xcord, ycordf-ycord))
        #print("changing " + str(i[2]-1) + " and " + str(i[3]-1) + " data " + str(d))
        graph[i[2]-1][i[3]-1] = d
        graph[i[3]-1][i[2]-1] = d

    #print(graph)
    g = Graph(l)
    g.graph = graph

    # ------------------- original start -----------------------
    src = int(request.args.get('s'))-1
    dst = request.args.get('d')
    dstnode = re.split(",", dst)
    print(dstnode)
    shor_path = []
    shor_coords = []
    for i in (dstnode):
        temp = g.dijkstra(int(i)-1)
        shor_path.append(temp[0])
        shor_coords.append(temp[1])

    data = {}
    distance_matrix = []

    for i in range(len(dstnode)):
        temp = []
        for j in (dstnode):
            temp.append(shor_path[i][int(j)-1])
        distance_matrix.append(temp)

    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['depot'] = src

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        nodeseq = print_solution(manager, routing, solution)
        c = 0
        while c < len(nodeseq):
            nodeseq[c] = int(dstnode[nodeseq[c]])
            c = c + 1
        print(nodeseq)

        count = 0
        trace_output = []
        while count < (len(nodeseq)-1):
            initial_node = nodeseq[count]
            final_node = nodeseq[count+1]
            trace_output.append(g.dijkstra1(initial_node-1, final_node-1))
            # trace_output.append(g.printTrace(shor_coords[count], initial_node-1, final_node-1))
            count = count + 1
        print("Trace output")
        print(trace_output)

        final_output = []
        for i in trace_output:
            temp1 = []
            for j in i:
                temp = []
                temp.append(j)
                temp.append(xlist[j-1])
                temp.append(ylist[j-1])
                temp1.append(temp)
            final_output.append(temp1)
        return jsonify(final_output)
    # print(distance_matrix)
    return jsonify([])
    # ------------------- original ends -----------------------

    # output1 = g.dijkstra(int(request.args.get('s'))-1)
    # output2 = g.dijkstra(11)
    # output3 = g.dijkstra(23)
    #
    # ans = sys.maxsize
    # travelling_node = int(request.args.get('s'))-1
    # for v in range(l):
    #     temp = output1[0][v] + output2[0][v] + output3[0][v]
    #     print(temp)
    #     print(v)
    #     if temp < ans:
    #         ans = temp
    #         travelling_node = v
    # print(travelling_node)
    # print(ans)
    # return ""

def print_solution(manager, routing, solution):
  """Prints solution on console."""
  print('Objective: {} miles'.format(solution.ObjectiveValue()))
  index = routing.Start(0)
  plan_output = 'Route for vehicle 0:\n'
  route_distance = 0
  nodeseq = []
  while not routing.IsEnd(index):
    plan_output += ' {} ->'.format(manager.IndexToNode(index))
    previous_index = index
    nodeseq.append(previous_index)
    index = solution.Value(routing.NextVar(index))
    route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
  plan_output += ' {}\n'.format(manager.IndexToNode(index))
  print(plan_output)
  plan_output += 'Route distance: {}miles\n'.format(route_distance)
  print(nodeseq)
  return nodeseq

app.run(host='0.0.0.0')