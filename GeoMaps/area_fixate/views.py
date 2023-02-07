import copy

import requests
from django.shortcuts import render
import rosreestr2coord as r2c
import osmapi as osm
from .utils import flatten, lon_lat_to_dict, get_node_id, divide_coords
from .config import OSM_BASE_URL, USER, PASSWORD, MAP_URL

from area_fixate.forms import GetMapAreaForm


def get_by_cadastral(request):
    html_map = None
    coord_dict = {}
    nodes = []
    data = {}
    if request.method == 'POST':
        cadastral_form = GetMapAreaForm(request.POST)
        if cadastral_form.is_valid():
            area = r2c.Area(str(cadastral_form.cleaned_data['cadastral_number']))
            lat_and_lon = flatten(area.get_coord(), 2)
            formatted_coordinates = lon_lat_to_dict(lat_and_lon)
            coords = copy.deepcopy(lat_and_lon)
            api = osm.OsmApi(USER, PASSWORD, api=OSM_BASE_URL)
            api.ChangesetCreate({u"comment": str(cadastral_form.cleaned_data['cadastral_number'])})
            for coord in formatted_coordinates:
                # nodes.append(api.NodeCreate(coord))
                api.ChangesetUpload({
                    u"type": u'node',
                    u"action": u"create",
                    u"data": {api.NodeCreate(coord)}
                })
            # node_ids = get_node_id(nodes)

            # data.update(api.WayCreate({
            #     u"nd": node_ids,
            #     u"tag": {}
            # }))
            # print(data)
            divided = divide_coords(coords)
            coord_dict['min_lon'] = min(divided[0])
            coord_dict['min_lat'] = min(divided[1])
            coord_dict['max_lon'] = max(divided[0])
            coord_dict['max_lat'] = max(divided[1])
            # api.ChangesetUpload({
            #     u"type": u'way',
            #     u"action": u"create",
            #     u"data": {*data}
            # })
            # api.ChangesetClose()
            html_map = MAP_URL + '{}%2C{}%2C{}%2C{}&amp;layer=mapnik'.format(coord_dict['min_lon'],
                                                                             coord_dict['min_lat'],
                                                                             coord_dict['max_lon'],
                                                                             coord_dict['min_lat'])
    else:
        cadastral_form = GetMapAreaForm()
    return render(request, 'area_fixate/index.html',
                  {'form': cadastral_form, 'url_name': get_by_cadastral, 'map': html_map})
