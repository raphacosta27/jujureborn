from shade import *
from pprint import pprint
simple_logging(debug=True)
conn = openstack_cloud(cloud='openstack')

conn.delete_server('testing')
