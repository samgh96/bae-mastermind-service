from __future__ import unicode_literals

UNITS = [{
    'name': 'Api call',
    'description': 'The final price is calculated based on the number of calls made to the API'
}]

# The keystone credentials are provided as settings rather than in the asset meta data
# as the IDM is supposed to be unique (the same as the BAE one)
KEYSTONE_USER = 'idm'
KEYSTONE_PASSWORD = 'idm'
KEYSTONE_HOST = 'http://172.17.0.1:5000'
