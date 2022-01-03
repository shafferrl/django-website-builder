"""
Creates a new DjangoProject object and deploys it to 
a live website using Linode's API.

"""
# Relevant library imports
from django_project_tools import DjangoProject
from django_deployment_tools import DjangoWebsite
import system_tools
import os, time


# Start the timer
start_time = time.time()

# Keyword arguments for instantiating a new DjangoProject object
django_project_kwargs = {
    'project_name': 'Test Website',
    'client_or_personal': 'p',
    'project_type': '1',
    'default_template': True,
    #'template_attrs': {
    #    'base_html_template': system_tools.TOOLS_DIR + 'Templates/type1/html/type1_home_base.html',
    #    'home_html_template': system_tools.TOOLS_DIR + 'Templates/type1/html/type1_home.html',
    #    'home_js_template': system_tools.TOOLS_DIR + 'Templates/type1/js/type1_home.js',
    #    'main_css_template': system_tools.TOOLS_DIR + 'Templates/type1/css/type1_main.css',
    #    'template_img_dir': system_tools.TOOLS_DIR + 'Templates/type1/img/',
    #},
    'admin_creds': {
        'admin_id': 'admin',
        'admin_password': 'insecurepassword',
        'admin_email': 'test@email.com'
    }
}

# Create DjangoProject instance, which will prompt for pertinent info
django_project = DjangoProject(**django_project_kwargs)

# Run create_project method on new DjangoProject object, which will create project files, etc...
django_project.create_project()

# Save project to database
django_project.save_project()

# Instantiate DjangoWebsite object
django_website = DjangoWebsite(django_project.proj_dir_prefix)

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

duration = (time.time() - start_time)
print('Total time: ', int(duration // 60), 'min, ', int(duration % 60), ' sec')

