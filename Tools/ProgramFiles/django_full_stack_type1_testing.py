from django_deployment_tools import DjangoWebsite
import os

# Instantiate DjangoWebsite object
django_website = DjangoWebsite('introstatement_h2')

# Change Linode account information to standard account
django_website.linode_acct_username = os.environ.get('LINODE_PRIMARY_USER')
django_website.linode_acct_password = os.environ.get('LINODE_PRIMARY_PASS')
django_website.linode_api_token = os.environ.get('LINODE_API_TOKEN')

# Generate SSH RSA key pair
django_website.ssh_keygen()

# Generate package requirements file
django_website.create_package_reqs()

# Create server instance
django_website.create_linode_nanode()

# Create files to configure server and configure server
django_website.configure_server_type1()
