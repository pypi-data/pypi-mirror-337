# Copyright 2025 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import http.server
import socketserver
import json
import threading
from enum import Enum
from typing import Union

import requests
import portpicker
import atexit
from google.cloud.spanner_v1 import TypeCode

from spanner_graphs.conversion import get_nodes_edges
from spanner_graphs.database import get_database_instance


# Mapping of string types from frontend to Spanner TypeCode enum values
PROPERTY_TYPE_MAP = {
    'BOOL': TypeCode.BOOL,
    'BYTES': TypeCode.BYTES,
    'DATE': TypeCode.DATE,
    'ENUM': TypeCode.ENUM,
    'INT64': TypeCode.INT64,
    'NUMERIC': TypeCode.NUMERIC,
    'FLOAT32': TypeCode.FLOAT32,
    'FLOAT64': TypeCode.FLOAT64,
    'STRING': TypeCode.STRING,
    'TIMESTAMP': TypeCode.TIMESTAMP
}

class NodePropertyForDataExploration:
    def __init__(self, key: str, value: Union[str, int, float, bool], type: TypeCode):
        self.key = key
        self.value = value
        self.type = type


class EdgeDirection(Enum):
    INCOMING = "INCOMING"
    OUTGOING = "OUTGOING"

def validate_property_type(property_type: str) -> TypeCode:
    """
    Validates and converts a property type string to a Spanner TypeCode.
    
    Args:
        property_type: The property type string from the request
        
    Returns:
        The corresponding TypeCode enum value
        
    Raises:
        ValueError: If the property type is invalid
    """
    if not property_type:
        raise ValueError("Property type must be provided")
        
    # Convert to uppercase for case-insensitive comparison
    property_type = property_type.upper()
    
    # Check if the type is valid
    if property_type not in PROPERTY_TYPE_MAP:
        valid_types = ', '.join(sorted(PROPERTY_TYPE_MAP.keys()))
        raise ValueError(f"Invalid property type: {property_type}. Allowed types are: {valid_types}")
    
    return PROPERTY_TYPE_MAP[property_type]

def validate_node_expansion_request(data) -> (list[NodePropertyForDataExploration], EdgeDirection):
    required_fields = ["project", "instance", "database", "graph", "uid", "node_labels", "direction"]
    missing_fields = [field for field in required_fields if data.get(field) is None]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    node_labels = data.get("node_labels")
    node_properties = data.get("node_properties", [])

    # Validate node_labels
    if not isinstance(node_labels, list):
        raise ValueError("node_labels must be an array")

    for label in node_labels:
        if not isinstance(label, str):
            raise ValueError("Each node label must be a string")

    # Validate node_properties
    if not isinstance(node_properties, list):
        raise ValueError("node_properties must be an array")

    validated_properties: list[NodePropertyForDataExploration] = []
    for idx, prop in enumerate(node_properties):
        if not isinstance(prop, dict):
            raise ValueError(f"Property at index {idx} must be an object")

        if not all(field in prop for field in ["key", "value", "type"]):
            raise ValueError(f"Property at index {idx} is missing required fields (key, value, type)")

        try:
            prop_type_str = prop["type"]
            if isinstance(prop_type_str, str):
                prop_type = validate_property_type(prop_type_str)

                value = prop["value"]
                if prop_type in (TypeCode.INT64, TypeCode.NUMERIC):
                    if not (isinstance(value, int) or (isinstance(value, str) and value.isdigit())):
                        raise ValueError(f"Property '{prop['key']}' value must be a number for type {prop_type_str}")
                elif prop_type in (TypeCode.FLOAT32, TypeCode.FLOAT64):
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        raise ValueError(
                            f"Property '{prop['key']}' value must be a valid float for type {prop_type_str}")
                elif prop_type == TypeCode.BOOL:
                    if not isinstance(value, bool) and not (isinstance(value, str) and value.lower() in ["true", "false"]):
                        raise ValueError(f"Property '{prop['key']}' value must be a boolean for type {prop_type_str}")

                validated_properties.append(NodePropertyForDataExploration(
                    key=prop["key"],
                    value=prop["value"],
                    type=prop_type
                ))
            else:
                raise ValueError(f"Property type at index {idx} must be a string")
        except ValueError as e:
            raise ValueError(f"Invalid property type in property at index {idx}: {str(e)}")

    try:
        direction = EdgeDirection(data.get("direction"))
    except ValueError:
        raise ValueError(f"Invalid direction: must be INCOMING or OUTGOING, got \"{data.get('direction')}\"")

    return validated_properties, direction

def execute_node_expansion(
    params_str: str,
    request: dict) -> dict:
    """Execute a node expansion query to find connected nodes and edges.
    
    Args:
        params_str: A JSON string containing connection parameters (project, instance, database, graph, mock).
        request: A dictionary containing node expansion request details (uid, node_labels, node_properties, direction, edge_label).
    
    Returns:
        dict: A dictionary containing the query response with nodes and edges.
    """

    params = json.loads(params_str)
    node_properties, direction = validate_node_expansion_request(params | request)

    project = params.get("project")
    instance = params.get("instance")
    database = params.get("database")
    graph = params.get("graph")
    uid = request.get("uid")
    node_labels = request.get("node_labels")
    edge_label = request.get("edge_label")

    edge = "e" if not edge_label else f"e:{edge_label}"

    # Build the path pattern based on direction
    path_pattern = (
        f"(n)-[{edge}]->(d)"
        if direction == EdgeDirection.OUTGOING
        else f"(n)<-[{edge}]-(d)"
    )

    node_label_str = ""
    if node_labels and len(node_labels) > 0:
        node_label_str = f": {' & '.join(node_labels)}"

    node_property_strings: list[str] = []
    for node_property in node_properties:
        value_str: str
        if node_property.type in (TypeCode.INT64, TypeCode.NUMERIC, TypeCode.FLOAT32, TypeCode.FLOAT64, TypeCode.BOOL):
            value_str = node_property.value
        else:
            value_str = f"\'''{node_property.value}\'''"
        node_property_strings.append(f"n.{node_property.key}={value_str}")

    query = f"""
        GRAPH {graph}
        LET uid = "{uid}"
        MATCH (n{node_label_str})
        WHERE {' and '.join(node_property_strings)} {'and' if node_property_strings else ''} STRING(TO_JSON(n).identifier) = uid
        RETURN n

        NEXT

        MATCH {path_pattern}
        RETURN TO_JSON(e) as e, TO_JSON(d) as d
        """

    return execute_query(project, instance, database, query, mock=False)

def execute_query(project: str, instance: str, database: str, query: str, mock = False):
    database = get_database_instance(project, instance, database, mock)

    try:
        query_result, fields, rows, schema_json, err = database.execute_query(query)
        if len(rows) == 0 : # if query returned an error
            if schema_json: # if the schema exists
                return {
                    "response": {
                        "schema": schema_json,
                        "query_result": query_result,
                        "nodes": [],
                        "edges": [],
                        "rows": []
                    },
                    "error": f"We've detected an error in your query. To help you troubleshoot, the graph schema's layout is shown above." + "\n\n" + f"Query error: \n{getattr(err, 'message', str(err))}"
                }
            if not schema_json: # if the schema does not exist
                return {
                    "response": {
                        "schema": schema_json,
                        "query_result": query_result,
                        "nodes": [],
                        "edges": [],
                        "rows": []
                    },
                    "error": f"Query error: \n{getattr(err, 'message', str(err))}"
                }
        nodes, edges = get_nodes_edges(query_result, fields, schema_json)
        
        return {
            "response": {
                "nodes": [node.to_json() for node in nodes],
                "edges": [edge.to_json() for edge in edges],
                "schema": schema_json,
                "rows": rows,
                "query_result": query_result
            }
        }
    except Exception as e:
        return {
            "error": getattr(e, "message", str(e))
        }


class GraphServer:
    port = portpicker.pick_unused_port()
    host = 'http://localhost'
    url = f"{host}:{port}"

    endpoints = {
        "get_ping": "/get_ping",
        "post_ping": "/post_ping",
        "post_query": "/post_query",
        "post_node_expansion": '/post_node_expansion',
    }

    _server = None

    @staticmethod
    def build_route(endpoint):
        return f"{GraphServer.url}{endpoint}"

    @staticmethod
    def start_server():
        class ThreadedTCPServer(socketserver.TCPServer):
            # Allow socket reuse to avoid "Address already in use" errors
            allow_reuse_address = True
            # Daemon threads automatically terminate when the main program exits
            daemon_threads = True

        with ThreadedTCPServer(("", GraphServer.port), GraphServerHandler) as httpd:
            GraphServer._server = httpd
            print(f"Spanner Graph Notebook loaded")
            GraphServer._server.serve_forever()

    @staticmethod
    def init():
        server_thread = threading.Thread(target=GraphServer.start_server)
        server_thread.start()
        return server_thread

    @staticmethod
    def stop_server():
        if GraphServer._server:
            GraphServer._server.shutdown()
            print("Spanner Graph Notebook shutting down...")

    @staticmethod
    def set_port(port):
        """Set a specific port for the server to use"""
        GraphServer.port = port
        GraphServer.url = f"{GraphServer.host}:{GraphServer.port}"

    @staticmethod
    def get_ping():
        route = GraphServer.build_route(GraphServer.endpoints["get_ping"])
        response = requests.get(route)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return False

    @staticmethod
    def post_ping(data):
        route = GraphServer.build_route(GraphServer.endpoints["post_ping"])
        response = requests.post(route, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return False

class GraphServerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_json_response(self, data):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_message_response(self, message):
        self.do_json_response({'message': message})

    def do_data_response(self, data):
        self.do_json_response(data)

    def do_error_response(self, message):
        if isinstance(message, Exception):
            message = str(message)
        self.do_json_response({'error': message})

    def parse_post_data(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        return json.loads(post_data)

    def handle_get_ping(self):
        self.do_message_response("pong")

    def handle_post_ping(self):
        data = self.parse_post_data()
        self.do_data_response({"your_request": data})

    def handle_post_query(self):
        data = self.parse_post_data()
        params = json.loads(data["params"])
        response = execute_query(            
            project=params["project"],
            instance=params["instance"],
            database=params["database"],
            query=data["query"],
            mock=params["mock"]
        )
        self.do_data_response(response)

    def handle_post_node_expansion(self):
        """Handle POST requests for node expansion.
        
        Expects a JSON payload with:
        - params: A JSON string containing connection parameters (project, instance, database, graph)
        - request: A dictionary with node details (uid, node_labels, node_properties, direction, edge_label)
        """
        try:
            data = self.parse_post_data()

            # Execute node expansion with:
            # - params_str: JSON string with connection parameters (project, instance, database, graph)
            # - request: Dict with node details (uid, node_labels, node_properties, direction, edge_label)
            self.do_data_response(execute_node_expansion(
                params_str=data.get("params"),
                request=data.get("request")
            ))
        except BaseException as e:
            self.do_error_response(e)
            return

    def do_GET(self):
        if self.path == GraphServer.endpoints["get_ping"]:
            self.handle_get_ping()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == GraphServer.endpoints["post_ping"]:
            self.handle_post_ping()
        elif self.path == GraphServer.endpoints["post_query"]:
            self.handle_post_query()
        elif self.path == GraphServer.endpoints["post_node_expansion"]:
            self.handle_post_node_expansion()

atexit.register(GraphServer.stop_server)
