"""
Creates custom DjangoProject object using custom template
and deploys to live website.

"""
# Relevant library imports
from django_project_tools import DjangoProject
from django_deployment_tools import DjangoWebsite
import system_tools
import os, time, json

with open('/etc/django_builder_private_data.json') as private_config:
    config_file = json.load(private_config)

# Start the timer
start_time = time.time()

django_project_kwargs = {
    'project_name': 'Band Website',
    'client_or_personal': 'p',
    'project_type': '1',
    #'default_template': False,
    #'format_html': True
    'template_attrs': {
        'plain_html_template': config_file['WEB_DEV_DIR'] + '/Experiments/BandWebsiteOblique-1/html/BandWebsiteOblique-1.html',
        #'base_html_template': system_tools.TOOLS_DIR + 'Templates/type1/html/type1_home_base.html',
        #'home_html_template': system_tools.TOOLS_DIR + 'Templates/type1/html/type1_home.html',
        'home_js_template': config_file['WEB_DEV_DIR'] + '/Experiments/BandWebsiteOblique-1/js/BandWebsiteOblique-1.js',
        'main_css_template': config_file['WEB_DEV_DIR'] + '/Experiments/BandWebsiteOblique-1/css/BandWebsiteOblique-1.css',
        'template_img_dir': config_file['WEB_DEV_DIR'] + '/Experiments/BandWebsiteOblique-1/img/',
        'template_video_dir': config_file['WEB_DEV_DIR'] + '/Experiments/BandWebsiteOblique-1/video/'
    },
    'admin_creds': {
        'admin_id': config_file['DEFAULT_ADMIN_ID'],
        'admin_password': config_file['DEFAULT_ADMIN_PASS'],
        'admin_email': config_file['DEFAULT_ADMIN_EMAIL']
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

