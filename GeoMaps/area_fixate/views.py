
from django.shortcuts import render
import rosreestr2coord as r2c
import osmapi as osm
from .utils import flatten, lon_lat_to_dict, get_node_id, divide_coords
from .config import OSM_BASE_URL, USER, PASSWORD, MAP_URL
import time
from .forms import GetMapAreaForm


def get_by_cadastral(request):
    nodes = []
    map_link = ''
    done = False
    res_time = None
    if request.method == 'POST':
        start = time.time()
        cadastral_form = GetMapAreaForm(request.POST)
        if cadastral_form.is_valid():
            cadastral = str(cadastral_form.cleaned_data['cadastral_number'])
            area = r2c.Area(cadastral, with_log=False, with_proxy=True)
            lat_and_lon = flatten(area.get_coord(), 2)
            formatted_coordinates = lon_lat_to_dict(lat_and_lon)
            api = osm.OsmApi(USER, PASSWORD, api=OSM_BASE_URL)
            with api.Changeset({"comment": "Test postion"}):
                for coord in formatted_coordinates:
                    nodes.append(api.NodeCreate(coord))
                nodes.append(nodes[0])
                node_ids = get_node_id(nodes)
                way = api.WayCreate({
                    u"nd": node_ids,
                    u"tag": {
                        u"cadastral_number": cadastral,
                        u"name": "Test drawing",
                        u"area": "yes",
                        u"landuse": "construction",
                        u"is_in:country": "Russia",
                    }
                })
                map_link = MAP_URL + str(way['id'])
                done = True
                res_time = round(time.time() - start, 2)
    else:
        cadastral_form = GetMapAreaForm()
    return render(request, 'area_fixate/index.html',
                  {'form': cadastral_form, 'url_name': get_by_cadastral, 'status': done, 'map_link': map_link, 'time': res_time})
