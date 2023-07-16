import datetime as dt
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.core.serializers import serialize
import folium
import ee
import jsonify
import json
from earthengine.products import EE_PRODUCTS
from .forms import SatelliteDataForm
from earthengine.methods import get_image_collection_asset,image_to_map_id
from django.shortcuts import render
import geemap



def home_view(request):
    '''
    To prevent confusion of urls, here is a `home page` that will be loaded at the root
    '''
    return render(request, 'gee/index.html')


def map_view(request):
    '''
    This will be the mapview
    '''
    satellite_data_form = SatelliteDataForm()

    latest_date = dt.datetime.today().strftime('%Y-%m-%d')
    context =   {
    'satellite_data_form':satellite_data_form,
    'ee_products':EE_PRODUCTS,
    'latest_date':latest_date,
    }
    return render(request, 'gee/map.html', context)

def get_image_collection(request):
    """
    Controller to handle image collection requests.
    """
    response_data = {'success': False}

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    else:
        platform = request.POST.get('platforms')
        sensor = request.POST.get('sensors')
        product = request.POST.get('products')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reducer = request.POST.get('reducer')

        url = get_image_collection_asset(
            platform=platform,
            sensor=sensor,
            product=product,
            date_from=start_date,
            date_to=end_date,
            reducer=reducer
        )

        print(platform, sensor, product, start_date, end_date, reducer)
        response_data.update({
            'success': True,
            'url': url,
            'products':product
        })
        #the_response_data = json.dumps(response_data)
        #print(the_response_data)
        return JsonResponse(response_data)

def mapfunction(img):
    return img.normalizedDifference(['B8','B4']);

def test1(request):
    # countries_shp = 'ahwaz.shp'
    # print(f"type(countries)={type(countries)}")
    # Map.addLayer(countries, {}, 'Countries')    
    ee_collection = ee.ImageCollection('COPERNICUS/S2_SR')
    # table = geemap.shp_to_ee(countries_shp)
    table = ee.FeatureCollection('projects/ee-farokhian/assets/ahwaz')
    print(f"type(table)={type(table)}")
    print(f"table.geometry().getInfo()={table.geometry().getInfo()}")

    e1 = ee_collection.filterBounds(table)
    e2 = e1.filterDate('2023-02-01','2023-03-01')
    e3 = e2.filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',30))
    e4 = e3.map(mapfunction).max().clip(table).rename('may')
    # print(f"e4.geometry.getInfo()={e4.geometry().getInfo()}")
    vis_params = {
                    'min': 0.0,
                    'max': 1.0
                    # 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
                }
    # print(f"ee_collection={ee_collection}")
    
    url = image_to_map_id(e4, vis_params)
    response_data = {
        'success': True,
        'url': url,
    }
    print(f"URL={url}")
    return render(request,'test1.html',{'map_url':url})
    return JsonResponse(response_data)