import os
import requests
import json
import xmltodict

API_ACCESS_KEY = os.getenv('3SCALE_API_ACCESS_KEY',
                'c297628a2f3596c288bda279785d3811544105ce0c31c29812d601e0eb607965')
API_URL = 'https://fabric8-analytics-test-admin.3scale.net'

def call_service(endpoint, data=None, method='post'):
    """ Posts data to 3scale's API and returns the response. Also,
    log any exceptions thrown"""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    service_url = "{}/{}/{}".format(API_URL, '/admin/api', endpoint)
    try:
        if method == 'post':
            response = requests.post(service_url, data=data, headers=headers)
        elif method == 'get':
            service_url = '{}?access_token={}'.format(service_url, API_ACCESS_KEY)
            if data is not None:
                service_url = '{}&{}'.format(service_url, data)
            response = requests.get(service_url, headers=headers)
        else:
            print ('unsupported service call {}'.format(method))
            return None
        #if response.status_code == 200:
        #    print (response.text)
    except requests.exceptions.Timeout as e:
        print ("Timeout Exception found %r" % e)
    except requests.exceptions.InvalidURL as e:
        print ("Invalid URL Exception found %r" % e)
    except requests.exceptions.TooManyRedirects as e:
        print ("Too Many Redirects Exception found %r" % e)
    except requests.exceptions.RequestException as e:
        print ("Exception found %r" % e)
    except Exception as e:
        print (e)
    
    return xmltodict.parse(response.text)
