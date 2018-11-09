from shade import *
from pprint import pprint
simple_logging(debug=True)
conn = openstack_cloud(cloud='openstack')

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
