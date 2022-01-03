from django_deployment_tools import DjangoWebsite
import os

# Instantiate DjangoWebsite object
django_website = DjangoWebsite()

# Change Linode account information to standard account
django_website.linode_acct_username = os.environ.get('LINODE_PRIMARY_USER')
django_website.linode_acct_password = os.environ.get('LINODE_PRIMARY_PASS')
django_website.linode_api_token = os.environ.get('WEBSITE_API_ACCESS_TOKEN') # Value incorrect for anonymity

# Generate SSH RSA key pair
django_website.ssh_keygen()

# Generate package requirements file
django_website.create_package_reqs()

# Create files to configure server and configure server
django_website.configure_server_type1()
