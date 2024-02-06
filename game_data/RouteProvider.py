import json


def get_route_by_name(route_name, object_type):
    print(route_name, object_type)
    with open("C:\\Users\\danth\\PycharmProjects\\Cookie_Factory\\game_data\\routes.json", 'r') as file:
        return json.load(file)["routeData"][object_type][route_name]