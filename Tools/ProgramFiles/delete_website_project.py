import system_tools
from django_project_tools import DjangoProject
from django_deployment_tools import DjangoWebsite
import sqlite3, os

def delete_website_project(keep_input=False, *args, **kwargs):
    to_delete = []
    # requires at least one project but will accept more projects as arguments if given
    if args:
        to_delete.append(args)
    else:
        while True:
            to_delete.append(input('\nEnter the handles of the projects to delete,\n'\
                                   'separated by a comma if multiple entries: ').split(','))
            to_delete = [to_delete[itm_indx].strip() for itm_indx in range(len(to_delete))]

    for del_item in to_delete:
        if not keep_input:
            
        else:
            pass
