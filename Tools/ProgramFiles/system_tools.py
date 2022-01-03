"""
Tools for interacting with the system on which projects
and websites are being created.

"""
# Relevant library imports
import json


# Get sensitive information
with open('/etc/django_builder_private_data.json') as config_file:
    config = json.load(config_file)

# variables / attributes
PROJECTS_DIR = config['WEB_BUILD_DIR'] + '/Projects/'
TOOLS_DIR = config['WEB_BUILD_DIR'] + '/Tools/'
BASH_UTILS_DIR = PROJECTS_DIR + 'Utilities/BashScripts/'
PYTHON_PATH = '/usr/bin/python3.7'
SSH_DIR = config['HOME_DIR'] + '/.ssh/'

projects_database = PROJECTS_DIR + 'Utilities/django_projects_db.sqlite'
projects_table = 'django_projects'
website_table = 'django_websites'

months_num = {
    'Jan': '01', 'Feb': '02', 'Mar': '03',
    'Apr': '04', 'May': '05', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09',
    'Oct': '10', 'Nov': '11', 'Dec': '12'
}

# Map folder type (key) to list of file extensions (value)
media_types = {
    'img': [
        'jpg', 'jpeg', 'png', 'webp','tiff',
        'bmp', 'svg', 'gif', 'exif',
    ],
    'video': [
        'mp4', 'mov', 'm4v', 'wmv', 'avi',
        'flv', 'mpg', 'mpeg',
    ],
    'audio': [
        'aac', 'wav', 'mp3', 'wma', 'flac',
    ],
    'css': ['css'],
    'html': ['html'],
    'js': ['js']
}

# Map file extension (key) to folder type (value)
media_types_by_ext = {
    'html': 'html', 'css': 'css', 'js': 'js', 'jpg': 'img', 'jpeg': 'img', 'png': 'img', 'webp': 'img', 'tiff': 'img',
    'bmp': 'img', 'svg': 'img', 'gif': 'img', 'exif': 'img', 'mp4': 'video',
    'mov': 'video', 'm4v': 'video', 'wmv': 'video', 'avi': 'video', 'flv': 'video',
    'mpg': 'video', 'mpeg': 'video', 'aac': 'audio', 'wav': 'audio', 'mp3': 'audio',
    'wma': 'audio', 'flac': 'audio',
}


# functions / methods

# Append date to end of handle in format: _YYYYMMDD
def handle_datestamp(handle):
    import time
    
    date_addendum = '_' + time.ctime().split()[-1] + months_num[time.ctime().split()[1]] + time.ctime().split()[2] 
    datestamped_handle = handle + date_addendum
    return datestamped_handle

# Check whether handle is valid
def is_valid_handle(handle):
    import string
    forbidden_chars = ' ' + string.punctuation[:26] + string.punctuation[27:]
    if len(handle) > 30:
        print('\nThe handle must be 30 characters or less.\n\nPlease try again.')
        return False
    for char in forbidden_chars:
        if char in handle:
            print('\nThe handle you entered contains an invalid character.\n'\
                          + forbidden_chars + '  are not allowed.\n\nPlease try again.')
            return False
        else:
            continue
    return True

# Confirm yes or no
def confirm_yes_no():
    confirm = input('\nIs this correct? (y/n):').lower()
    while True:
        if confirm == 'y':
            return True
        elif confirm == 'n':
            return False
        else:
            print('\nInvalid input.  Please enter "y" or "n".\n')
            continue

# Formulate directory name prefix
def create_dir_prefix(project_name):
    import string, re
    forbidden_chars = string.punctuation[:26] + string.punctuation[27:]
    return '_'.join(re.sub('[' + forbidden_chars + ']', '', project_name).lower().split(' '))

# Verify a file path by absolute path, the extension type (i.e. .html, .js, .py) and a name reference used to get the input from the user.
def verify_file_path(extension, name_ref):
    import os
    while True:
        path_try = input('\nEnter the absolute file path to ' + name_ref + ': ')
        if os.path.exists(path_try):
            if '\\' in path_try:
                path_try = '/'.join(path_try.split('\\'))
            if os.path.isdir(path_try):
                if path_try.endswith('/'):
                    print('\nThe directory path entered is: "' + path_try + '"')
                    if confirm_yes_no():
                        return path_try
                    else:
                        continue
                else:
                    print('\nThe directory path entered is: "' + path_try + '"')
                    if confirm_yes_no():
                        return path_try + '/'
            elif os.path.isfile(path_try):
                if path_try.endswith(extension):
                    print('\nThe file path entered is: "' + path_try + '"')
                    if confirm_yes_no():
                        return path_try
                    else:
                        continue
                else:
                    print('\nThe file specified is not the correct type.\n'\
                          'The file must end with a ' + extension + ' file extension.\n'\
                          'Please try again.')
                    continue
        else:
            print('\nThe file/path specified does not exist.  Please try again.')
            continue

# Gathers list of projects to check project handle input against     
def proj_list():
    import os

    personal_list = os.listdir(PROJECTS_DIR + 'Personal/ProjectFolders')
    client_list = os.listdir(PROJECTS_DIR + 'Clients/ProjectFolders')
    
    return personal_list + client_list

def media_type(file_path):
    return media_types_by_ext[file_path.split('.')[1]]
