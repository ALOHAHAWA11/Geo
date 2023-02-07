def flatten(lst: list, depth: int = -1) -> list:
    result = []
    for element in lst:
        if depth == 0 or type(element) is not list:
            result.append(element)
        else:
            result.extend(flatten(element, depth - 1))
    return result


def lon_lat_to_dict(lst: list) -> list:
    coordinates = list()
    for coord_pair in lst:
        coordinates.append(
            {
                u"lon": coord_pair[0],
                u"lat": coord_pair[1],
                u"tag": {
                    u"visible": "yes",
                    u"log_name": "my_sector"
                }
            }
        )
    return coordinates


def get_node_id(lst: list) -> list:
    nodes = []
    for node in lst:
        nodes.append(node['id'])
    return nodes


def divide_coords(lst: list) -> (list, list):
    lons = []
    lats = []
    for coord in lst:
        lons.append(coord[0])
        lats.append(coord[1])
    return lons, lats
