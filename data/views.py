import json
import subprocess
from time import sleep

import requests
from django.shortcuts import render
from django.http.response import HttpResponse


def experiment(request):
    return HttpResponse('OK')

def traceroute(request, domain):
    print('domain', domain)
    # Get trace-route information from the system
    trace_results = subprocess.check_output(['traceroute', '-n', '-m', '100', domain])
    trace_results = bytes.decode(trace_results)
    lines = trace_results.strip().split('\n')

    # Collect all the IP addresses from the command output
    ip_addr_array = []
    for line in lines:
        items = line.split('  ')
        if len(items) > 1:
            ip_address = items[1]
            ip_addr_array.append(ip_address)
    
    geo_locations = []
    
    # experiment with ip-api.com
    for ip_address in ip_addr_array:
        response = requests.get('http://ip-api.com/json/{}'.format(ip_address))
        if response.status_code == 200:
            json_text = response.text
            json_obj = json.JSONDecoder().decode(json_text)
     
            if json_obj['status'] == 'success':
                geo_location = {
                    'lng': json_obj['lon'],
                    'lat': json_obj['lat'],
                }
             
                geo_locations.append(geo_location)
             
            # wait to be safe
            sleep(0.41)
             
        else:
            print('something went wrong')
    
    built_context = {
        'geo_locations': geo_locations
    }
    
    return render(request, template_name='traceroute/index.html', context=built_context)