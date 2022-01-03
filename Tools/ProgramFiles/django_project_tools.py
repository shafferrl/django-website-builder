"""
Tools for creating, saving, and testing Django website projects 
using web page templates.

"""
# Relevant library imports
import system_tools
from client_tools import Client
    

# Class containing methods to create, save, and test a Django website project
class DjangoProject:
    project_name = ''
    project_dir_prefix = ''
    client_or_personal = ''
    supported_types = [
        'Simple Business / Personal CV with Basic Info 1',
    ]
    # Future Templates
    '''
        'Simple Business / Personal CV with Basic Info 2',
        'Personal Portfolio 1',
        'Simple Business / Personal Blog 1',
        'Advanced Business / Personal w/ Contact Form & Addt\'l Pages',
        'Business / Personal Page w/ \'Staff\' Blog & Addt\'l Pages',
        'E-Commerce Site',
    '''
    
    project_type = ''
    abort = False

    
    def __init__(self, custom_handle=False, **kwargs):
        # Set project name and convert to unique snake-cased project handle for naming files and folders
        if not self.abort:
            if 'project_name' in kwargs:
                self.project_name = kwargs['project_name']
                if custom_handle:
                    if 'project_handle' in kwargs:
                        self.get_dir_prefix(kwargs['project_handle'], no_input=True, custom_handle=True)
                    else:
                        self.get_dir_prefix(custom_handle=True)
                else:
                    self.get_dir_prefix(no_input=True)
            else:
                self.get_name()
                self.get_dir_prefix()

        # Determine whether a project is for personal use, for a client, or for testing
        if not self.abort:
            if 'client_or_personal' in kwargs:
                self.client_or_personal = kwargs['client_or_personal']
                if kwargs['client_or_personal'] == 'p':
                    self.client = Client(set_default=True)
                    self.project_home_dir = system_tools.PROJECTS_DIR + 'Personal/'
                elif kwargs['client_or_personal'] == 'c':
                    self.project_home_dir = system_tools.PROJECTS_DIR + 'Clients/'
                elif kwargs['client_or_personal'] == 't':
                    self.project_home_dir = system_tools.PROJECTS_DIR + 'TestSites/'
            else:
                self.get_project_context()
        
        # Determine the style or category of website the project will be
        if not self.abort:
            if 'project_type' in kwargs:
                self.get_project_type(kwargs['project_type'])
            else:
                self.get_project_type()
        
        # Determine whether to use default or custom web page template for project
        if not self.abort:
            if 'default_template' in kwargs:
                if kwargs['default_template']:
                    self.get_template(default_template=True)
                else:
                    if 'template_attrs' in kwargs:
                        self.get_template(kwargs['template_attrs'])
                    else:
                        self.get_template(bypass_default=True)
            else:
                if 'template_attrs' in kwargs:
                    self.get_template(kwargs['template_attrs'])
                else:
                    self.get_template()
        
        # Set the credentials for the website project's admin / superuser
        if not self.abort:
            if 'admin_creds' in kwargs:
                self.admin_id = kwargs['admin_creds']['admin_id']
                self.admin_password = kwargs['admin_creds']['admin_password']
                self.admin_email = kwargs['admin_creds']['admin_email']
            else:
                self.get_admin_info()

        if self.abort:
            print('\nProject aborted.')


    # Obtain the website's name to appear in the header / intro
    def get_name(self):
        while True:
            prompt = '\nEnter the name of the website as it would appear on the page\'s header '\
                    'with appropriate spacing, punctuation, and capitalization:\n'
            self.project_name =  input(prompt)

            if self.project_name.strip() == '':
                print('\nThe project\'s name must contain non-whitespace characters.\n')
                continue
            else:
                print('\nThe website\'s name will appear as: ' + '"' + self.project_name + '"')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue

    # Creates project directory handle (prefix) from project name with file system-appropriate characters and without spaces
    def create_dir_prefix(self, project_name):
        import string, re
        self.proj_dir_prefix = '_'.join(re.sub('[' + string.punctuation + ']', '', project_name).lower().split(' '))


    # Create / obtain a unique project handle, which will be used for naming directories and as a primary key in the project database
    def get_dir_prefix(self, *args, no_input=False, custom_handle=False):
        import string, os, re

        if not custom_handle:
            self.proj_dir_prefix = system_tools.create_dir_prefix(self.project_name)
        else:
            self.proj_dir_prefix = ''
        handle_exists = False
        
        # Make sure the directory handle / prefix is acceptable and that it is valid
        while True:
            if not no_input:
                is_confirmed_prefix = system_tools.confirm_yes_no()
            else:
                is_confirmed_prefix = True
            if not handle_exists and is_confirmed_prefix and not custom_handle:
                try:
                    os.mkdir(system_tools.PROJECTS_DIR + 'Utilities/BashScripts/' + self.proj_dir_prefix)
                    self.BASH_SCRIPT_DIR = system_tools.PROJECTS_DIR + 'Utilities/BashScripts/' + self.proj_dir_prefix + '/'
                    print('\nThe files for this project will have the following prefix:\n"' + self.proj_dir_prefix + '"')
                    handle_exists = False
                except FileExistsError:
                    print('\nThis handle already exists.  Please choose a different one.')
                    handle_exists = True
                    if no_input:
                        print('\nA project with this handle already exists.  Creating incremented handle...')
                    continue
                print('"' + self.proj_dir_prefix + '"' + ' prefix/handle confirmed.')
                break
            else:
                while True:
                    if not args and not no_input:
                        self.proj_dir_prefix = input('Enter custom file prefix: ')
                    elif not args and no_input:
                        highest_match_dir = max([direc for direc in os.listdir(system_tools.BASH_UTILS_DIR) if direc == self.proj_dir_prefix or direc.startswith(self.proj_dir_prefix) and re.search('NUM\d{3}$', direc)])
                        if re.search('NUM\d{3}$', highest_match_dir):
                            new_num = int(highest_match_dir[-3:]) + 1
                            if new_num >= 100:
                                self.proj_dir_prefix = highest_match_dir[:-3] + str(new_num)
                            elif new_num >= 10:
                                self.proj_dir_prefix = highest_match_dir[:-3] + '0' + str(new_num)
                            else:
                                self.proj_dir_prefix = highest_match_dir[:-3] + '00' + str(new_num)
                            handle_exists = False
                            break
                        else:
                            self.proj_dir_prefix += '_NUM002'
                            handle_exists = False
                            break
                    else:
                        self.proj_dir_prefix = args[0]
                    if not system_tools.is_valid_handle(self.proj_dir_prefix):
                        if no_input:
                            raise SyntaxError('Project handle may contain letters, digits, and/or underscore only.')
                        continue
                    else:
                        handle_exists = False
                        custom_handle = False
                        break


    # Determine whether the project is a personal or client project to file appropriately and get payment info for hosting services
    def get_project_context(self):
        while True:
            self.client_or_personal = input('\nIs this project for a client or a personal project?\n'\
                                       'Enter "c" for client, "p" for personal, or "t" for test site:').lower()
            if self.client_or_personal == 'c' or self.client_or_personal == 'p' or self.client_or_personal == 't':
                break
            else:
                print('\nInvalid input.  Please try again.')
                continue

        if self.client_or_personal == 'c':
            self.project_home_dir = system_tools.PROJECTS_DIR + 'Clients/'
            while True:
                enter_client_info = input('\nIs there relevant client info to enter at this time?\n'\
                                       'This can be skipped for now but will be needed before\n'\
                                       'a project can become a website.  Enter "y" or "n": ')
                if enter_client_info.lower() == 'y':
                    self.client = Client()
                    break
                elif enter_client_info.lower() == 'n':
                    self.client = None
                    break
                else:
                    print('\nThe input was invalid.  Please try again.')
                    continue
        elif self.client_or_personal == 'p':
            self.project_home_dir = system_tools.PROJECTS_DIR + 'Personal/'
            while True:
                enter_personal_info = input('\nEnter personal information for payment at this time?\n'\
                                            'Can be skipped now but will be needed for deployment. ("y" or "n): ')
                if enter_personal_info.lower() == 'y':
                    self.client = Client(set_default=True)
                    break
                elif enter_personal_info.lower() == 'n':
                    self.client = None
                    break
                else:
                    print('\nThe input was invalid.  Please try again.')
                    continue
        elif self.client_or_personal == 't':
            self.project_home_dir = system_tools.PROJECTS_DIR + 'TestSites/'
        

    # Create / obtain the style of website, which will determine the structure of the backend program files
    def get_project_type(self, *args):
        if args:
            self.project_type = args[0]
        while True and not args:
            types_str = ''
            for type_index in range(len(self.supported_types)):
                types_str += '\n' + str(type_index + 1) + ') ' + self.supported_types[type_index]

            self.project_type = input('\nWhat kind of project is this? (enter number)' + types_str + '\n')
            if self.project_type < '1' or self.project_type > str(len(self.supported_types)):
                print('\nYour input was invalid.\nPlease enter a number shown to the left of the type you want.')
                continue
            else:
                print('\nThe type of project you\'re starting is:\n' + self.project_type + ') ' + self.supported_types[int(self.project_type) - 1])
                if system_tools.confirm_yes_no():
                    break
                else: continue

        if self.project_type == '1':
            self.app1_name = 'main'


    # Create Django-style html templates from typically structured html template files
    def create_django_html(self, django_template_type, html_template, project_type):
        import re
        template_dir = '/'.join(html_template.split('/')[:-1]) + '/'

        if project_type == '1':
            
            # Replace html external references (href, src attributes) with Django-formatted ones
            def django_refs(html_string, *regexes):
                for regex in regexes:
                    if re.findall(regex, html_string):
                        for found_match in re.findall(regex, html_string):
                            try:
                                if not found_match.startswith('{%'):
                                    html_string = html_string.replace(found_match, '{% static \'' + self.app1_name + '/' + system_tools.media_types_by_ext[found_match.split('.')[-1]] + '/' + found_match.split('/')[-1] + '\' %}')
                            except KeyError:
                                continue
                return html_string

            # Render "base" django html template
            if django_template_type == 'base':
                with open(template_dir + 'type1_home_base.html', 'w') as base_html_file:
                    base_html_file.write('{% load static %}\n')
                    with open(html_template) as html_template_file:
                        for line in html_template_file:
                            if '</head>' not in line:
                                # Assumes one "main" css file (main.css) in the header of type 1 websites
                                if re.search('<link.*?href=[\'"](.+?\.css)[\'"].*?>', line):
                                    for match_group in re.findall('<link.*?href=[\'"](.+?\.css)[\'"].*?>', line):
                                        if not match_group.startswith('{%'):
                                            line = line.replace(match_group, '{% static \'' + self.app1_name + '/' + system_tools.media_types_by_ext[match_group.split('.')[-1]] + '/type1_main.css\' %}')
                                line = django_refs(line, '<link.*?href=[\'"](.+?)[\'"].*?>', '<script.*?src=[\'"](.+?)[\'"].*?>')
                                base_html_file.write(line)
                            else:
                                line = django_refs(line.split('</head>')[0], '<link.*?href=[\'"](.+?)[\'"].*?>', '<script.*?src=[\'"](.+?)[\'"].*?>')
                                base_html_file.write(line)
                                base_html_file.write('{% if title %}\n'\
                                                     '<title>\n    pr0j3ct_n4m3 -- {{ title }}\n</title>\n'\
                                                     '{% else %}\n'\
                                                     '<!-- 20 characters max -->\n<title>\n    pr0j3ct_n4m3\n</title>\n'\
                                                     '{% endif %}\n'\
                                                     '</head>\n')
                                break
                    base_html_file.write('{% block content %}\n{% endblock content %}\n</html>')
                return template_dir + 'type1_home_base.html'
            
            # Render "home" django html template
            elif django_template_type == 'home':
                with open(template_dir + 'type1_home.html', 'w') as home_html_file:
                    home_html_file.write('{% extends "' + self.app1_name + '/base.html" %}\n'\
                                         '{% load static %}\n'\
                                         '{% block content %}\n')
                    with open(html_template) as html_template_file:
                        is_body = False
                        for line in html_template_file:
                            if re.search('<body.*?>', line):
                                if '</body>' not in line:
                                    is_body = True
                                    line = django_refs(line, '<img.*?src=[\'"](.+?)[\'"].*?>', '<video.*?src=[\'"](.+?)[\'"].*?>', '<source.*?src=[\'"](.+?)[\'"].*?>', '<script.*?src=[\'"](.+?)[\'"].*?>')
                                    home_html_file.write(re.search('<body.*?>', line).group() + line.split(re.search('<body.*?>', line).group())[1])
                                else:
                                    line = django_refs(line, '<img.*?src=[\'"](.+?)[\'"].*?>', '<video.*?src=[\'"](.+?)[\'"].*?>', '<source.*?src=[\'"](.+?)[\'"].*?>', '<script.*?src=[\'"](.+?)[\'"].*?>')
                                    home_html_file.write(re.search('<body.*?>', line).group() + line.split(re.search('<body.*?>', line).group())[1].split('</body>')[0] + '</body>\n')
                                    break
                            else:
                                if is_body:
                                    if '</body>' not in line:
                                        # Assumes one script tag for type1 website
                                        if re.search('<script.*?src=[\'"](.+?)[\'"].*?>', line):
                                            for match_group in re.findall('<script.*?src=[\'"](.+?)[\'"].*?>', line):
                                                if not match_group.startswith('{%'):
                                                    line = line.replace(match_group, '{% static \'' + self.app1_name + '/' + system_tools.media_types_by_ext[match_group.split('.')[-1]] + '/' + match_group.split('/')[-1] + '\' %}')
                                        line = django_refs(line, '<img.*?src=[\'"](.+?)[\'"].*?>', '<video.*?src=[\'"](.+?)[\'"].*?>', '<source.*?src=[\'"](.+?)[\'"].*?>', '<script.*?src=[\'"](.+?)[\'"].*?>')
                                        home_html_file.write(line)
                                    else:
                                        # Assumes one script tag for type1 website
                                        if re.search('<script.*?src=[\'"](.+?)[\'"].*?>', line):
                                            for match_group in re.findall('<script.*?src=[\'"](.+?)[\'"].*?>', line):
                                                if not match_group.startswith('{%'):
                                                    line = line.replace(match_group, '{% static \'' + self.app1_name + '/' + system_tools.media_types_by_ext[match_group.split('.')[-1]] + '/' + match_group.split('/')[-1] + '\' %}')
                                        line = django_refs(line.split('</body>')[0], '<img.*?src=[\'"](.+?)[\'"].*?>', '<video.*?src=[\'"](.+?)[\'"].*?>', '<source.*?src=[\'"](.+?)[\'"].*?>', '<script.*?src=[\'"](.+?)[\'"].*?>')
                                        home_html_file.write(line + '</body>\n')
                                        is_body = False
                                        break
                    home_html_file.write('{% endblock content %}')
                return template_dir + 'type1_home.html'

            # Render django-formatted links in css file
            elif django_template_type == 'css':
                with open(template_dir + 'type1_main.css', 'w') as main_css_file:
                    with open(html_template) as css_template_file:
                        for line in css_template_file:
                            if re.findall('url\([\'"]{0,1}(.*?/.+?\..+?)[\'"]{0,1}\)', line):
                                for match_group in re.findall('url\([\'"]{0,1}(.*?/.+?\..+?)[\'"]{0,1}\)', line):
                                    line = line.replace(match_group, '../' + system_tools.media_types_by_ext[match_group.split('.')[-1]] + '/' + match_group.split('/')[-1])
                            main_css_file.write(line)
                return template_dir + 'type1_main.css'

            # If improper Django template type is requested
            else:
                raise NameError('"' + django_template_type + '" is not a valid Django template type.')


    # Ask user whether a custom template is to be used or if just to go with default
    def get_template(self, *args, default_template=False, bypass_default=False):
        self.template_video_dir = None
        if self.project_type == '1':
            if args:
                if not 'plain_html_template' in args[0]:
                    self.base_html_template = args[0]['base_html_template']
                    self.home_html_template = args[0]['home_html_template']
                    self.main_css_template = args[0]['main_css_template']
                else:
                    self.base_html_template = self.create_django_html('base', args[0]['plain_html_template'], self.project_type)
                    self.home_html_template = self.create_django_html('home', args[0]['plain_html_template'], self.project_type)
                    self.main_css_template = self.create_django_html('css', args[0]['main_css_template'], self.project_type)
                self.home_js_template = args[0]['home_js_template']
                self.template_img_dir = args[0]['template_img_dir']
                if 'template_video_dir' in args[0]:
                    self.template_video_dir = args[0]['template_video_dir']
            while True and not args:
                if not default_template and not bypass_default:
                    is_custom_template = input('\nWould you like to use a custom template? (y/n): ')
                elif not default_template and bypass_default:
                    is_custom_template = 'y'
                else:
                    is_custom_template = 'n'
                if is_custom_template.lower() == 'n':
                    print('\nUsing default template.')
                    self.base_html_template = system_tools.TOOLS_DIR + 'Templates/type1/html/template1/type1_template1_home_base.html'
                    self.home_html_template = system_tools.TOOLS_DIR + 'Templates/type1/html/template1/type1_template1_home.html'
                    self.home_js_template = system_tools.TOOLS_DIR + 'Templates/type1/js/template1-a/type1_template1-a_home.js'
                    self.main_css_template = system_tools.TOOLS_DIR + 'Templates/type1/css/template1-a/type1_template1-a_main.css'
                    self.template_img_dir = system_tools.TOOLS_DIR + 'Templates/type1/img/template1-a/'
                    break
                elif is_custom_template.lower() == 'y':
                    while True:
                        is_django_template = input('\nIs the html in Django format? (y/n)')
                        if is_django_template.lower() == 'y':
                            self.base_html_template = system_tools.verify_file_path('html', 'the HTML "base" template')
                            self.home_html_template = system_tools.verify_file_path('html', 'the HTML "home" template')
                            break
                        elif is_django_template.lower() == 'n':
                            combined_html_template = system_tools.verify_file_path('html', 'the HTML template')
                            self.base_html_template = self.create_django_html('base', combined_html_template, self.project_type)
                            self.home_html_template = self.create_django_html('home', combined_html_template, self.project_type)
                            break
                        else:
                            print('\nThe input entered was not valid.  Please try again.')
                            continue
                    self.home_js_template = system_tools.verify_file_path('js', 'the "home" JavaScript template')
                    self.main_css_template = system_tools.verify_file_path('css', 'the "main" CSS template')
                    self.template_img_dir = system_tools.verify_file_path('', 'the template image directory')
                    while True:
                        is_video_dir = input('\nAre there any video files with this template? (y/n):')
                        if is_video_dir.lower() == 'y':
                            self.template_video_dir = system_tools.verify_file_path('', 'the template video directory')
                            break
                        elif is_video_dir.lower() == 'n':
                            break
                        else:
                            print('\nThe input entered was invalid.  Please try again.')
                            continue
                    break
                else:
                    print('\nInvalid input.  Please try again.')
                    continue

    #
    def get_admin_info(self):

        # To be implemented later
        """
        while True:
            self.admin_id = input('\nPlease enter your desired admin username:\n')
            if not system_tools.is_valid_handle(self.admin_id):
                continue
            else:
                print('Your admin account username is:\n' + self.admin_id)
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue"""
        
        self.admin_id = 'admin'
        self.admin_password = 'insecurepassword'
        self.admin_email = 'email@address.com'
        print('\nThe current admin id is: "' + self.admin_id + '"')
        print('The temporary admin password is: "' + self.admin_password + '"')
        print('The placeholder admin email is: ' + self.admin_email)
        print('Change these via the form(s) on the /admin page as soon as possible.')

    # Create a Django project of any available type         
    def create_project(self):
        import subprocess, re, os

        while True and not self.abort:
            cmds_1 = [
                system_tools.PYTHON_PATH + ' -m venv "' + ' '.join([re.escape(segment) for segment in self.project_home_dir.split()]) + 'VirtualEnvs/' + self.proj_dir_prefix + '_venv"',
                '"' + self.project_home_dir + 'VirtualEnvs/' + self.proj_dir_prefix + '_venv/bin/python" -m pip install django'
            ]

            # Create bash script from which commands will be run and which will serve as a log of the commands entered
            with open(self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_1.sh', 'w') as bash_local_1:
                for cmd in cmds_1:
                    bash_local_1.write(cmd + '\n')

            # Give Bash script appropriate permissions
            subprocess.run('chmod 700 "' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_1.sh"', shell=True)
                           
            # Generate project folders for website.
            print('\nCreating project virtual environment...')
            subprocess.run('"' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_1.sh"', shell=True)

            # Give virtual environment activation file necessary permissions
            subprocess.run('chmod 700 "' + self.project_home_dir + 'VirtualEnvs/' + self.proj_dir_prefix + '_venv/bin/activate"', shell=True)

            if 'django-admin' not in os.listdir(self.project_home_dir + 'VirtualEnvs/' + self.proj_dir_prefix + '_venv/bin/'):
                print('\nUnable to download Django via pip.')
                print('Try again with internet connection.')
                self.abort = True
                break

            cmds_2 = [
                'cd ' + '"' + self.project_home_dir + 'ProjectFolders"',
                '"' + self.project_home_dir + 'VirtualEnvs/' + self.proj_dir_prefix + '_venv/bin/django-admin" startproject ' + self.proj_dir_prefix + '_project',
            ]

            # Create bash script from which commands will be run and which will serve as a log of the commands entered
            with open(self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_2.sh', 'w') as bash_local_2:
                for cmd in cmds_2:
                    bash_local_2.write(cmd + '\n')

            # Give Bash script appropriate permissions
            subprocess.run('chmod 700 "' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_2.sh"', shell=True)
            
            print('\nCreating project files and directories...')
            subprocess.run('"' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_2.sh"', shell=True)
            
            self.PYTHON_PATH = self.project_home_dir + 'VirtualEnvs/' + self.proj_dir_prefix + '_venv/bin/python'
            self.PROJECT_ROOT_DIR = self.project_home_dir + 'ProjectFolders/' + self.proj_dir_prefix + '_project/'

            if self.project_type == '1':
                self.create_simple()

            break

    # Create a simple informational website
    def create_simple(self):
        import re, os, subprocess

                        
        # Bash comands to create app 1 files and directories
        cmds_3 = [
            'cd "' + self.PROJECT_ROOT_DIR + '"',
            '"' + self.PYTHON_PATH + '"' + ' manage.py startapp ' + self.app1_name,
            'rm ' + '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/tests.py"',
            'rm ' + '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/admin.py"',
            'rm ' + '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/models.py"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/templates"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/templates/' + self.app1_name + '"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/static"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/'  + self.app1_name + '"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/'  + self.app1_name + '/img"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/'  + self.app1_name + '/css"',
            'mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/'  + self.app1_name + '/js"',
            '"' + self.PYTHON_PATH + '"' + ' manage.py makemigrations',
            '"' + self.PYTHON_PATH + '"' + ' manage.py migrate',
            'echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'email@address.com\', \'insecurepassword\')" | "' + self.PYTHON_PATH + '" manage.py shell',
            #'chmod 700 ' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_create_su.sh"',
            #'"' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_create_su.sh"',
        ]

        # Add command to list if the template has videos
        if self.template_video_dir:
            cmds_3.append('mkdir "' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/' + self.app1_name + '/video"')
            

        with open(self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_3.sh', 'w') as bash_local_3:
            for cmd in cmds_3:
                if cmd.startswith('rm '):
                    if self.project_type == '1':
                        bash_local_3.write(cmd + '\n')
                else:
                    bash_local_3.write(cmd + '\n')


        # Create Bash script to create a superuser and enter relevant information
        with open(system_tools.TOOLS_DIR + 'Templates/common/bash/createsuperuser.sh') as create_su_template:
            with open(self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_create_su.sh', 'w') as create_su_target:
                for line in create_su_template:
                    if 'python' in line:
                        create_su_target.write(line.replace('python', '"' + self.PYTHON_PATH + '"'))
                    else:
                        create_su_target.write(line)

        # Give Bash script permissions necessary to run
        subprocess.run('chmod 700 "' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_3.sh"', shell=True)
        print('Creating project type (' + self.project_type + ') files and directories...')
        cmd_run_3 = subprocess.run('"' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_3.sh"', shell=True, capture_output=True)
        print(cmd_run_3.stdout.decode())


        # Bash commands to copy template files
        # Use list comprehension to populate list with copy commands for image files
        cmds_4 = [
            'cp ' + '"' + self.template_img_dir + template_img + '" '\
                '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/' + self.app1_name + '/img/' + template_img + '"'
            for template_img in os.listdir(self.template_img_dir)
        ]

        # If there are any video files, copy in same manner as image files
        if self.template_video_dir:
            cmds_4 += [
                'cp ' + '"' + self.template_video_dir + template_video + '" '\
                '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/' + self.app1_name + '/video/' + template_video + '"'
                for template_video in os.listdir(self.template_video_dir)
            ]
        
        cmds_4 += [
            'cp ' + '"' + self.main_css_template + '" '\
                '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/' + self.app1_name + '/css/' + self.main_css_template.split('/')[-1] + '"',
            'cp ' + '"' + self.home_js_template + '" '\
                '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/static/' + self.app1_name + '/js/' + self.home_js_template.split('/')[-1] + '"',
            'cp ' + '"' + system_tools.TOOLS_DIR + 'Templates/type1/python/type1_urls.py" '\
                '"' + self.PROJECT_ROOT_DIR + self.proj_dir_prefix + '_project/urls.py"',
            'cp ' + '"' + system_tools.TOOLS_DIR + 'Templates/type1/python/type1_app1_urls.py" '\
                '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/urls.py"',
            'cp ' + '"' + system_tools.TOOLS_DIR + 'Templates/type1/python/type1_app1_views.py" '\
                '"' + self.PROJECT_ROOT_DIR + self.app1_name + '/views.py"',
        ]
        
        with open(self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_4.sh', 'w') as bash_local_4:
            for cmd in cmds_4:
                bash_local_4.write(cmd + '\n')
                
        # Give Bash script appropriate permissions
        subprocess.run('chmod 700 "' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_4.sh"', shell=True)
        
        print('Copying type (' + self.project_type + ') template files...')
        subprocess.run('"' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_4.sh"', shell=True)

        
        base_html_template_name = 'type1_home_base.html'
        home_html_template_name = 'type1_home.html'

        # Copy and modify html base template
        with open(self.base_html_template) as base_html_template:
            with open(self.PROJECT_ROOT_DIR + self.app1_name + '/templates/' + self.app1_name + '/base.html', 'w') as base_html:
                for line in base_html_template:
                    if 'pr0j3ct_n4m3' in line:
                        line = line.replace('pr0j3ct_n4m3', self.project_name)
                    if re.search('\{%\s*static\s+\'main/css/.+?\.css\'\s*%\}', line):
                        line = re.sub('\{%\s*static\s+\'main/css/.+?\.css\'\s*%\}', '{% static \'' + self.app1_name + '/css/' + self.main_css_template.split('/')[-1] + '\' %}', line)
                    base_html.write(line)

        # Copy and modify html home page template
        with open(self.home_html_template) as home_html_template:
            with open(self.PROJECT_ROOT_DIR + self.app1_name + '/templates/' + self.app1_name + '/home.html', 'w') as home_html:
                for line in home_html_template:
                    if 'pr0j3ct_n4m3' in line:
                        line = line.replace('pr0j3ct_n4m3', self.project_name)
                    if re.search('\{%\s*static\s+\'main/js/.+?\.js\'\s*%\}', line):
                        line = re.sub('\{%\s*static\s+\'main/js/.+?\.js\'\s*%\}', '{% static \'' + self.app1_name + '/js/' + self.home_js_template.split('/')[-1] + '\' %}', line)
                    home_html.write(line)

        # Modify settings.py module for this project
        with open(self.PROJECT_ROOT_DIR + self.proj_dir_prefix + '_project/settings.py') as settings_file:
            settings_updated = ''
            for line in settings_file:
                if 'django.contrib.admin' in line:
                    new_line = line.replace('django.contrib.admin', self.app1_name + '.apps.' + self.app1_name.capitalize() + 'Config')
                    settings_updated += new_line
                    settings_updated += line
                elif 'STATIC_URL =' in line:
                    settings_updated += 'STATIC_ROOT = os.path.join(BASE_DIR, \'static\')\n'
                    settings_updated += line
                else:
                    settings_updated += line
        os.remove(self.PROJECT_ROOT_DIR + self.proj_dir_prefix + '_project/settings.py')
        with open(self.PROJECT_ROOT_DIR + self.proj_dir_prefix + '_project/settings.py', 'w') as updated_settings_file:
            updated_settings_file.write(settings_updated)

    # Save project to database
    def save_project(self):
        import sqlite3, pickle

        # Allow sqlite3 to convert to and from DjangoProject data type
        sqlite3.register_converter('DJANGO_PROJECT', pickle.loads)
        sqlite3.register_adapter(DjangoProject, pickle.dumps)

        # Write SQL statements to variables for more readable code
        sql_create_table = 'CREATE TABLE IF NOT EXISTS ' + system_tools.projects_table + '(project_id INTEGER NOT NULL PRIMARY KEY, project_handle STRING, project_object DJANGO_PROJECT)'
        sql_insert_project = 'INSERT INTO ' + system_tools.projects_table + ' VALUES ((SELECT MAX(project_id) + 1 FROM ' + system_tools.projects_table + '), :handle, :project)'
        sql_update_project = 'UPDATE ' + system_tools.projects_table + ' SET project_object = :project WHERE project_id = (SELECT project_id FROM ' + system_tools.projects_table + ' WHERE project_handle = "' + self.proj_dir_prefix + '")'
        sql_select_existing = 'SELECT * FROM ' + system_tools.projects_table + ' WHERE project_handle = "' + self.proj_dir_prefix + '"'

        project_dict = {'handle': self.proj_dir_prefix, 'project': self}

        # Connect to database and create cursor
        conn = sqlite3.connect(system_tools.projects_database, detect_types=sqlite3.PARSE_DECLTYPES)
        curs = conn.cursor()
        curs.execute(sql_create_table)

        # If project already exists in database, update.  If not, insert new
        try:
            if curs.execute(sql_select_existing).fetchone():
                curs.execute(sql_update_project, project_dict)
            else:
                curs.execute(sql_insert_project, project_dict)
        except sqlite3.OperationalError:
            curs.execute(sql_create_table)
            curs.execute(sql_insert_project, project_dict)

        # Save and close database
        conn.commit()
        conn.close()
        
    # Run a local server and open website
    def run_localhost(self):
        import subprocess, time
        from selenium import webdriver

        # Create .vbs script that runs a local server
        with open(system_tools.TOOLS_DIR + 'Templates/common/bash/runserver.sh') as runserver_template:
            with open(self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_runserver.sh', 'w') as runserver_target:
                for line in runserver_template:
                    if 'python' in line:
                        line = line.replace('python', '"' + self.PYTHON_PATH + '"')
                    if 'manage.py' in line:
                        line = line.replace('manage.py', '"' + self.PROJECT_ROOT_DIR + 'manage.py"')
                    runserver_target.write(line)

        # Give bash script necessary permissions
        subprocess.run('chmod 700 ' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_runserver.sh', shell=True)

        # Run bash script in separate terminal
        test_cmd = 'gnome-terminal -e "bash -c ' + self.BASH_SCRIPT_DIR + self.proj_dir_prefix + '_runserver.sh;bash"'
        subprocess.run(test_cmd, shell=True)
        
        print('Starting local server...')
        # Local server sometimes takes a few seconds to boot. Sleep to keep program from tripping up.
        time.sleep(4)
        
        test_url = 'http://localhost:8000/'
        self.test_driver = webdriver.Firefox()
        self.test_driver.implicitly_wait(1)
        self.test_driver.get(test_url)

    #Close the local server
    def close_localhost(self):
        self.test_driver.quit()
        print('Localhost closed')
            
