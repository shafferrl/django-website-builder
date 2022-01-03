from django_project_tools import DjangoProject
from django_deployment_tools import DjangoWebsite
import system_tools
import os, time, json

with open('/etc/django_builder_private_data') as private_config:
    config_file = json.load(private_config)

start_time = time.time()

django_project_kwargs = {
    'project_name': 'Band Website',
    'client_or_personal': 'p',
    'project_type': '1',
    'default_template': True,
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

# Launch website on localhost in browser
django_project.run_localhost()

duration = (time.time() - start_time)
print('Total time: ', int(duration // 60), 'min, ', int(duration % 60), ' sec')

