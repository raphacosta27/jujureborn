from shade import *
from pprint import pprint
simple_logging(debug=True)
conn = openstack_cloud(cloud='openstack')
images = conn.list_images()

for image in images:
    print(image, '\n')

flavors = conn.list_flavors()
for flavor in flavors:
    print(flavor)

image_id = '06314e6d-ae1a-49e0-9de4-a7458acb5819'
image = conn.get_image(image_id)
print(image)

flavor_id = '15de0f48-734c-42f4-8bdf-c4eeb8ae2228'
flavor = conn.get_flavor(flavor_id)

print('--------- networks ---------')
networks = conn.list_networks()
network_id = '21b26d41-3312-478f-9b77-8ff2ca72cbaa'
print(networks)
for n in networks:
    print(n)
    print('\n')

print('------------ create server -------------')
instance_name = 'testing'
testing_instance = conn.create_server(wait=True, auto_ip=True,
    name=instance_name,
    image=image_id,
    flavor=flavor_id,
    network=network_id
    )
print(testing_instance)

print('--------- existing instances ---------')
instances = conn.list_servers()
for instance in instances:
    print(instance)


# Keys
print('Checking for existing SSH keypair...')
keypair_name = 'pubkey'
pub_key_file = '/home/cloud/.ssh/id_rsa.pub'

if conn.search_keypairs(keypair_name):
    print('Keypair already exists. Skipping import.')
else:
    print('Adding keypair...')
    conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())

for keypair in conn.list_keypairs():
    print(keypair)


# Network

print('Checking for existing security groups...')
sec_group_name = 'all-in-one'
if conn.search_security_groups(sec_group_name):
    print('Security group already exists. Skipping creation.')
else:
    print('Creating security group.')
    conn.create_security_group(sec_group_name, 'network access for all-in-one application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

conn.search_security_groups(sec_group_name)

# Userdata

ex_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''

instance_name = 'all-in-one'
testing_instance = conn.create_server(wait=True, auto_ip=False,
    name=instance_name,
    image=image_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[sec_group_name],
    userdata=ex_userdata,
    network=network_id
)

f_ip = conn.available_floating_ip()
print('The Fractals app will be deployed to http://%s' % f_ip['floating_ip_address'] )
conn.add_ip_list(testing_instance, [f_ip['floating_ip_address']])

