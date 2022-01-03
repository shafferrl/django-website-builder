"""
Uses the DjangoProject class to instantiate a new project
and save to the projects database.

"""

# Relevant library imports
import django_project_tools, json

with open('/etc/django_builder_private_data') as private_config:
    config_file = json.load(private_config)


# Keyword arguments used to instantiate a new DjangoProject object
django_project_kwargs = {
    'project_name': 'Website Project',
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
django_project = django_project_tools.DjangoProject(**django_project_kwargs)

    # Run create_project method on new DjangoProject object, which will create project files, etc...
django_project.create_project()

# Save project to database
django_project.save_project()

# Launch a browser window with the filled-in template
#if not django_project.abort:
#    django_project.run_localhost()
