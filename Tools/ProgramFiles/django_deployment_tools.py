"""
Tools for deploying a DjangoProject object to a live website.

"""
# Relevant library imports
from django_project_tools import DjangoProject
from client_tools import Client
import system_tools
import web_tools


# Class containing methods to create, save, and deploy a website from a DjangoProject object
class DjangoWebsite:
    
    # Constructor prompts user for project handle and retrieves associated project from database
    def __init__(self, *args, load_website=True, **kwargs):
        linode_api_keys = []
        
        import os, sqlite3, pickle

        # Initialize variables whose existence will be compared against
        self.project = None
        django_project_handle = ''

        # Load website object from database if handle is passed into constructor
        if args:
            if args[0] + '_project' in system_tools.proj_list():
                django_project_handle = args[0]
                # Check if constructor keyword allows for loading website object or just project object
                if load_website:
                    try:
                        existing_site = self.load_website(django_project_handle)
                        self.__dict__ = existing_site.__dict__.copy()
                        print('"' + self.project.proj_dir_prefix + '" website object has been loaded from database.')
                    except:
                        self.project = self.load_project(django_project_handle)
                        print('\nNo website with that handle exists in the database.\n'\
                              '"' + self.project.proj_dir_prefix + '" project object only has been loaded from database.')
                else:
                    self.project = self.load_project(django_project_handle)
                    print('"' + self.project.proj_dir_prefix + '" project object has been loaded from database.')
            else:
                print('\n"' + args[0] + '" is not a valid project handle.')
            
        # Take project handle as input to load DjangoProject object into DjangoWebsite object
        while True and not django_project_handle:
            django_project_handle = input('\nEnter the handle of a project to load: ')
            if django_project_handle + '_project' not in system_tools.proj_list():
                print('\nThe project handle entered is not valid.\nPlease retry.')
                django_project_handle = ''
                continue
            else:
                print('\nThe handle entered is: ' + django_project_handle)
                if system_tools.confirm_yes_no():
                    try:
                        existing_site = self.load_website(django_project_handle)
                        print(existing_site)
                        while True:
                            load_existing = input('\nA website with this handle exists in the database.\n'\
                                                  'Would you like to load the existing website? (y/n)')
                            if load_existing.lower() == 'y':
                                self.__dict__ = existing_site.__dict__.copy()
                                print('\n"' + self.project.proj_dir_prefix + '" has been loaded from database.')
                                break
                            elif load_existing.lower() == 'n':
                                break
                            else:
                                print('\nInvalid input.  Please try again.')
                                continue
                    except:
                        pass
                else:
                    continue

        # Don't load project from database if it was already copied from a DjangoWebsite object from the database
        if not self.project:
            # Load the desired project from the database and save as DjangoWebsite object attribute
            sqlite3.register_converter('DJANGO_PROJECT', pickle.loads)

            # Probably not necessary, but safeguard against SQL injection in case this code ever gets copied into website form backend
            handle_dict = {'handle': django_project_handle}

            # Connect to database and create cursor
            conn = sqlite3.connect(system_tools.projects_database, detect_types=sqlite3.PARSE_DECLTYPES)
            curs = conn.cursor()

            # Fetch the DjangoProject object from the database
            curs.execute('SELECT project_object FROM django_projects WHERE project_handle = :handle', handle_dict)
            self.project = curs.fetchone()[0]
            conn.close()
            
            try:
                self.payment_info = self.project.payment_info
            except:
                if self.project.client_or_personal == 'p':
                    self.project.client = Client(set_default=True)
                else:
                    self.project.client = Client()
                self.payment_info = self.project.client.client_info['payment_info']


    def load_project(self, project_handle):
        import sqlite3, pickle

        # Retrieve BLOB data as reconstructed DjangoProject object
        sqlite3.register_converter('DJANGO_PROJECT', pickle.loads)

        # SQL statement for retrieving DjangoProject object from database
        sql_select_project = 'SELECT project_object FROM ' + system_tools.projects_table + ' WHERE project_handle = "' + project_handle + '"'

        # Connect to database and create cursor
        conn = sqlite3.connect(system_tools.projects_database, detect_types=sqlite3.PARSE_DECLTYPES)
        curs = conn.cursor()

        # Attempt to retrieve DjangoProject object with given handle
        try:
            curs.execute(sql_select_project)
            project_obj = curs.fetchone()[0]
            return project_obj
        except:
            print('\nNo project object exists in database under given handle.')
            raise sqlite3.OperationalError


    def load_website(self, web_proj_handle):
        import sqlite3, pickle

        # Retrieve BLOB data as reconstructed DjangoWebsite object
        sqlite3.register_converter('DJANGO_WEBSITE', pickle.loads)
    
        # SQL statement for retrieving DjangoWebsite object from database
        sql_select_website = 'SELECT website_object FROM ' + system_tools.website_table + ' WHERE project_handle = "' + web_proj_handle + '"'

        # Connect to database and create cursor
        conn = sqlite3.connect(system_tools.projects_database, detect_types=sqlite3.PARSE_DECLTYPES)
        curs = conn.cursor()

        # Attempt to retrieve DjangoWebsite object with given handle
        try:
            curs.execute(sql_select_website)
            website_obj = curs.fetchone()[0]
            return website_obj
        except:
            print('\nNo website object exists in database under given handle.')
            raise sqlite3.OperationalError

    
    def save_website(self):
        import sqlite3, pickle
        
        # Allow sqlite3 to convert to and from DjangoWebsite data type
        sqlite3.register_converter('DJANGO_WEBSITE', pickle.loads)
        sqlite3.register_adapter(DjangoWebsite, pickle.dumps)

        # Write SQL statements to variables for more readable code
        sql_create_table = 'CREATE TABLE IF NOT EXISTS ' + system_tools.website_table + '(website_id INTEGER NOT NULL PRIMARY KEY, project_handle STRING, website_object DJANGO_WEBSITE)'
        sql_insert_website = 'INSERT INTO ' + system_tools.website_table + ' VALUES ((SELECT MAX(website_id) + 1 FROM ' + system_tools.website_table + '), :handle, :website)'
        sql_update_website = 'UPDATE ' + system_tools.website_table + ' SET website_object = :website WHERE website_id = (SELECT website_id FROM ' + system_tools.website_table + ' WHERE project_handle = "' + self.project.proj_dir_prefix + '")'
        sql_select_existing = 'SELECT * FROM ' + system_tools.website_table + ' WHERE project_handle = "' + self.project.proj_dir_prefix + '"'

        website_dict = {'handle': self.project.proj_dir_prefix, 'website': self}
        
        # Connect to database and create cursor
        conn = sqlite3.connect(system_tools.projects_database, detect_types=sqlite3.PARSE_DECLTYPES)
        curs = conn.cursor()

        # If project already exists in database, update.  If not, insert new
        try:
            if curs.execute(sql_select_existing).fetchone():
                curs.execute(sql_update_website, website_dict)
            else:
                curs.execute(sql_insert_website, website_dict)
        except sqlite3.OperationalError:
            curs.execute(sql_create_table)
            curs.execute(sql_insert_website, website_dict)

        # Save and close database
        conn.commit()
        conn.close()

        
    # Generate an ssh RSA key pair that is unique to each website
    def ssh_keygen(self):
        import subprocess, os
        
        if self.project.proj_dir_prefix + '_id_rsa' not in os.listdir(system_tools.SSH_DIR):
            print('Generating RSA key pair for passwordless SSH login')
            ssh_keygen_cmd = 'ssh-keygen -b 4096 -N "" -f ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa' 
            subprocess.run(ssh_keygen_cmd, shell=True)
        else:
            print('Not generating SSH key.  SSH key already exists for this project...')


    # Creates a file with the package installation requirements for the server
    def create_package_reqs(self):
        import subprocess, os
        
        print('Creating package requirements file...')
        
        self.REQUIREMENTS_DIR = system_tools.PROJECTS_DIR + 'Utilities/PackageRequirements/' + self.project.proj_dir_prefix + '/'
        try:
            os.mkdir(self.REQUIREMENTS_DIR)
        except FileExistsError:
            pass
        
        freeze_cmd = '"' + self.project.PYTHON_PATH + '" -m pip freeze > ' + '"' + self.REQUIREMENTS_DIR + self.project.proj_dir_prefix + '_requirements.txt"'
        subprocess.run(freeze_cmd, shell=True)

    def create_linode_acct(self):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.firefox.options import Options
        import time, os

        def get_confirm_email():
            nonlocal email_confirmed

            email_confirmed = False
            
            email_tuple = tuple(driver.find_elements_by_xpath('//*[@data-test-id="message-list-item"]'))
            
            # Search for the correct verification email by "from" and "subject" fields as well as timestamp
            time.sleep(1)
            for email_item in email_tuple:
                email_text = email_item.text
                
                if 'support@linode.com' and 'Linode - Please confirm your email' in email_text:
                    email_time = email_text.split()[-2]
                    
                    if ':' in email_time:
                        email_minutes = int(email_time.split(':')[-1])
                        email_hours = int(email_time.split(':')[0])
                        
                        if request_hours >= email_hours and request_minutes >= email_minutes:
                            email_confirmed = True
                            print('Retrieving confirmation email...')
                            email_item.click()
                            break
                        
                        else:
                            continue

        # Create attributes necessary for creating linode account
        self.linode_acct_username = system_tools.handle_datestamp(self.project.proj_dir_prefix)
        self.linode_acct_password = self.linode_acct_username + '_01'
        # Savenew attributes to database
        self.save_website()

        # Set up web driver and settings
        options = Options()
        #options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(1)

        # Retrieve Linode account sign-up page
        create_acct_url = 'https://login.linode.com/signup'
        print('Retrieving account sign-up page...')
        driver.get(create_acct_url)

        # Locate form input elements and enter user information
        print('Entering user information...')
        username_input = driver.find_element_by_id('username')
        email_input = driver.find_element_by_id('email')
        password_input = driver.find_element_by_id('password')
        
        username_input.send_keys(self.linode_acct_username)
        email_input.send_keys(web_tools.email_addr)
        password_input.send_keys('insecurepassword_001')
        print('Submitting user information...')
        password_input.submit()

        # Record the time that the account creation request was made to verify correct email by timestamp
        request_time = ''.join(time.ctime().__str__()[11:19].split(':')[:2])
        request_hours = int(request_time[:2])
        request_minutes = int(request_time[-2:])

        # Allow request time to go through before leaving page
        time.sleep(5)

        web_tools.email_login(driver)

        # Wait for inbox to load and locate all emails in inbox
        time.sleep(3)

        email_confirmed = False
        get_confirm_email()

        # If the correct email was found, navigate to second account creation page, entering and submitting payment information
        if email_confirmed:
            time.sleep(1)
            confirm_button = driver.find_element_by_partial_link_text('Confirm')
            confirm_link = confirm_button.get_attribute('href')

            # Sometimes "select" element for U.S. State doesn't properly load after selecting dropdown option for "US", so retry until successful
            while True:
                print('Retrieving Linode user payment info page...')
                driver.get(confirm_link)
                time.sleep(3)

                # Attempt to complete and submit form and break loop if successful
                try:
                    first_name_input = driver.find_element_by_id('first_name')
                    first_name_input.send_keys(self.payment_info['first_name'])
                    
                    last_name_input = driver.find_element_by_id('last_name')
                    last_name_input.send_keys(self.payment_info['last_name'])
                    
                    address_input = driver.find_element_by_id('address_1')
                    address_input.send_keys(self.payment_info['address_1'])
                    
                    # If client has suite number or similar in billing address
                    if self.payment_info['address_2']:   #suite, etc...
                        address_2_input = driver.find_element_by_id('address_2')
                        address_2_input.send_keys(self.billing_address_2)
                    
                    time.sleep(1)
                    country_input = driver.find_element_by_xpath('//select[@id="country"]/option[@value="'+self.payment_info['country']+'"]')
                    country_input.click()
                    
                    time.sleep(1)
                    state_input = driver.find_element_by_xpath('//select[@id="state"]/option[@value="'+self.payment_info['state']+'"]')
                    state_input.click()
                    
                    city_input = driver.find_element_by_id('city')
                    city_input.send_keys(self.payment_info['city'])

                    zip_input = driver.find_element_by_id('zip')
                    zip_input.send_keys(self.payment_info['card_zip'])
                    
                    cc_no_input = driver.find_element_by_id('cc_number')
                    cc_no_input.send_keys(self.payment_info['card_no'])

                    cc_exp_input = driver.find_element_by_id('cc_expiration')
                    cc_exp_input.send_keys(self.payment_info['card_expiry'])

                    cc_cvv_input = driver.find_element_by_id('cvv')
                    cc_cvv_input.send_keys(self.payment_info['card_cvv'])
                                           
                    accept_service = driver.find_element_by_class_name('checkbox-label')
                    accept_service.click()

                    create_acct_btn = driver.find_element_by_id('submit')
                    #create_acct_btn.click()
                    break

                # Notify user upon failure and retry page retrieval and form submittal
                except:
                    print('Linode payment info form submittal failed.  Trying again...')
                    continue

        time.sleep(1)

        # Log back into email and delete confirmation email since it is no longer needed
        web_tools.email_login(self, driver)

        time.sleep(1)

        get_confirm_email()

        if email_confirmed:
            delete_email_btn = driver.find_element_by_xpath('//*[@data-test-id="toolbar-delete"]')
            print('Deleting confirmation email')
            delete_email_btn.click()
        
        web_tools.email_logout(self, driver)

        driver.quit()

    def create_linode_api_token(self):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.firefox.options import Options
        import time, os

        # Set up web driver and settings
        options = Options()
        #options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(1)

        driver.get(web_tools.linode_login_url)
        
        username_input = driver.find_element_by_id('username')
        username_input.send_keys(self.linode_acct_username)
        
        password_input = driver.find_element_by_id('password')
        password_input.send_keys(self.linode_acct_password)
        
        submit_btn = driver.find_element_by_name('submit')
        submit_btn.click()

        access_token_url = 'https://cloud.linode.com/profile/tokens'
        driver.get(access_token_url)

        # Loop until page loads with relevant button
        while True:
            try:
                add_api_token_btn = driver.find_element_by_xpath('//*[@title="Add a Personal Access Token"]')
                add_api_token_btn.click()
                break
            except:
                time.sleep(1)
                continue
        
        token_label_input = driver.find_element_by_id('label')
        token_label_input.send_keys(self.linode_acct_username + '_key')
            
        select_rw_all = driver.find_element_by_xpath('//*[@aria-label="Select read/write for all"]')
        select_rw_all.click()

        all_btns = driver.find_elements_by_tag_name('button')
        for button in all_btns:
            if 'Create Token' in button.text:
                create_token_btn = button
                break

        create_token_btn.click()

        self.linode_api_token = ''

        # Loop until page loads element with API token and button
        while not self.linode_api_token:
            try:
                time.sleep(1)
                self.linode_api_token = driver.find_element_by_class_name('noticeText').text
                api_token_ok_btn = driver.find_element_by_class_name('MuiButton-containedSecondary')
                api_token_ok_btn.click()
                break
            except:
                continue

        # Logout of account when finished
        logout_url = 'https://cloud.linode.com/logout'
        driver.get(logout_url)

        driver.quit()

        # Save new attribute to database
        self.save_website()


    def create_linode_nanode(self):
        import subprocess, json
        
        # Define attributes that will be needed to generate a linode instance
        self.linode_attrs = {
            'region': 'us-west',
            'type': 'g6-nanode-1',
            'image': 'linode/ubuntu19.10',
        }

        with open(system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa.pub') as ssh_pub_key:
            linode_authorized_keys = ssh_pub_key.read().strip()

        create_nanode_cmd = 'curl -H "Content-Type: application/json" '\
                    '-H "Authorization: Bearer '+self.linode_api_token+'" '\
                    '-X POST -d "{'\
                    '   \\"image\\": \\"'+self.linode_attrs['image']+'\\", '\
                    '   \\"type\\": \\"'+self.linode_attrs['type']+'\\", '\
                    '   \\"region\\": \\"'+self.linode_attrs['region']+'\\", '\
                    '   \\"root_pass\\": \\"'+self.linode_acct_password+'\\", '\
                    '  \\"authorized_keys\\": ['\
                    '       \\"' + linode_authorized_keys + '\\"'\
                    '   ]'\
                    '}" '\
                    'https://api.linode.com/v4/linode/instances'

        create_nanode = subprocess.run(create_nanode_cmd, shell=True, capture_output=True)
        self.linode_attrs = json.loads(create_nanode.stdout)

        # Save new attributes to database
        self.save_website()


    # Gets the current attributes (status) of linode instance
    def get_linode_status(self):
        import subprocess, json
        
        get_status_cmd = 'curl -H "Authorization: Bearer '+self.linode_api_token+'" '\
                        'https://api.linode.com/v4/linode/instances/'+str(self.linode_attrs['id'])
      
        get_status = subprocess.run(get_status_cmd, shell=True, capture_output=True)
        self.linode_attrs['status'] = json.loads(get_status.stdout)['status']


    # Install necessary files and configure server for website
    def configure_server_type1(self):
        import subprocess, time, sys, os
        """
        # Copy sshd_config-transfer script from templates to project and change IP address appropriately
        print('Creating Visual Basic script to bypass first server login...')
        with open(system_tools.TOOLS_DIR + 'Templates/type1/vbs/type1_scp_sshd_startup.vbs') as type1_scp_sshd_startup:
            with open(self.project.VBS_FILE_DIR + 'scp_sshd_startup.vbs', 'w') as send_sshd_startup:
                for line in type1_scp_sshd_startup:
                    if '255.255.255.255' in line:
                        send_sshd_startup.write(line.replace('255.255.255.255', self.linode_attrs['ipv4'][0]))
                    elif 'p4ssw0rd' in line:
                        send_sshd_startup.write(line.replace('p4ssw0rd', self.linode_acct_password))
                    else:
                        send_sshd_startup.write(line)
        """
        # Make project-specific bash script folder in general projects' utilities folder
        try:
            os.mkdir(system_tools.PROJECTS_DIR + 'Utilities/BashScripts/' + self.project.proj_dir_prefix)
        except FileExistsError:
            pass
        self.BASH_SCRIPT_DIR = system_tools.PROJECTS_DIR + 'Utilities/BashScripts/' + self.project.proj_dir_prefix + '/'

        # Copy stack script from templates to project and change values as appropriate
        print('Creating Bash stack script...')
        with open(system_tools.TOOLS_DIR + 'Templates/type1/bash/type1_stack_script.sh') as type1_stack_script:
            with open(self.BASH_SCRIPT_DIR + self.project.proj_dir_prefix + '_stack_script.sh', 'w') as project_stack_script:
                for line in type1_stack_script:
                    if 'proj_dir_prefix' in line:
                        if 'proj_dir_prefix_project' in line:
                            project_stack_script.write(line.replace('proj_dir_prefix', self.project.proj_dir_prefix))
                        else:
                            if '.conf' in line:
                                project_stack_script.write(line.replace('proj_dir_prefix', self.project.proj_dir_prefix))
                            else:
                                project_stack_script.write(line.replace('proj_dir_prefix', self.project.proj_dir_prefix.replace('_','-')))
                    else:
                        project_stack_script.write(line)
                        
        # Make project-specific bash script folder in general projects' utilities folder
        try:
            os.mkdir(system_tools.PROJECTS_DIR + 'Utilities/LinuxConfigFiles/' + self.project.proj_dir_prefix)
        except FileExistsError:
            pass
        self.LINUX_CONFIG_DIR = system_tools.PROJECTS_DIR + 'Utilities/LinuxConfigFiles/' + self.project.proj_dir_prefix + '/'
         
        # Copy "hosts" file (/etc/hosts) from templates and change values as appropriate for server
        print('Creating Linux hosts file...')
        with open(system_tools.TOOLS_DIR + 'Templates/type1/linux/hosts') as type1_hosts:
            with open(self.LINUX_CONFIG_DIR + self.project.proj_dir_prefix + '_hosts', 'w') as project_hosts:
                for line in type1_hosts:
                    if '255.255.255.255' in line:
                        project_hosts.write(line.replace('255.255.255.255', self.linode_attrs['ipv4'][0]).replace('h05tn4m3', self.project.proj_dir_prefix.replace('_', '-')))
                    else:
                        project_hosts.write(line)

        # Copy basic Apache http configuration file from templates to project folder and change values as necessary
        print('Creating Apache configuration file...')
        with open(system_tools.TOOLS_DIR + 'Templates/type1/linux/type1_django_website_http.conf') as type1_http_conf:
            with open(self.LINUX_CONFIG_DIR + self.project.proj_dir_prefix + '_http.conf', 'w') as project_http_conf:
                for line in type1_http_conf:
                    if 'pr0j3ct_n4m3' in line:
                        project_http_conf.write(line.replace('pr0j3ct_n4m3', self.project.proj_dir_prefix + '_project'))
                    else:
                        project_http_conf.write(line)

        # Make folder if not yet created for project's remote settings.py file
        try:
            os.mkdir(system_tools.PROJECTS_DIR + 'Utilities/PythonTemplates/' + self.project.proj_dir_prefix + '/')
        except FileExistsError:
            pass
        
        # Copy project settings.py file and change values necessary to run website on server
        print('Creating server-specific Django settings file...')
        with open(self.project.PROJECT_ROOT_DIR + '/' + self.project.proj_dir_prefix + '_project/' + 'settings.py') as settings_py_local:
            with open(system_tools.PROJECTS_DIR + 'Utilities/PythonTemplates/' + self.project.proj_dir_prefix + '/settings.py', 'w') as settings_py_remote:
                for line in settings_py_local:
                    if 'import os' in line:
                        settings_py_remote.write(line.replace('os', 'os, json'))
                        settings_py_remote.write('\n\nwith open(\'/etc/config.json\') as config_file:\n'\
                                                 '    config = json.load(config_file)\n')
                    elif 'SECRET_KEY' in line:
                        print('Creating Django settings config file from template...')
                        with open(system_tools.TOOLS_DIR + 'Templates/type1/linux/type1_config.json') as type1_config_json:
                            with open(system_tools.PROJECTS_DIR + 'Utilities/LinuxConfigFiles/' + self.project.proj_dir_prefix + '/' + self.project.proj_dir_prefix + '_config.json', 'w') as project_config_json:
                                for json_line in type1_config_json:
                                    if 'SECRET_KEY' in json_line:
                                        project_config_json.write(json_line.replace('""', '"' + line.split('\'')[1] + '"'))
                                    else:
                                        project_config_json.write(json_line)
                        settings_py_remote.write('SECRET_KEY = config[\'SECRET_KEY\']\n')
                    elif 'DEBUG = True' in line:
                        settings_py_remote.write('DEBUG = False\n')
                    elif 'ALLOWED_HOSTS' in line:
                        settings_py_remote.write('ALLOWED_HOSTS = [\'' + self.linode_attrs['ipv4'][0] + '\']\n')
                    else:
                        settings_py_remote.write(line)
        
        # Pause program if server isn't yet ready
        time.sleep(2)
        wait_count = 0
        while self.linode_attrs['status'] != 'running':
            if wait_count == 0:
                print('Waiting for server to boot up...')
            elif wait_count == 7:       # ~1 minute
                print('Server is taking unusually long to boot.  Consider interrupting execution.')
            time.sleep(9)
            self.get_linode_status()
            wait_count += 1

        # Save updated status to database
        self.save_website()

        # Give streams time to clear to avoid hang-ups
        time.sleep(22)

        # Relevant commands for getting server ready and booted
        server_config_cmds = [
            'ssh-keygen -f ' + system_tools.SSH_DIR + 'known_hosts -R "' + self.linode_attrs['ipv4'][0] + '"',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa -o "StrictHostKeyChecking no" ' + system_tools.TOOLS_DIR + 'Templates/type1/linux/type1_sshd_config_startup root@' + self.linode_attrs['ipv4'][0] + ':/etc/ssh/sshd_config',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa "' + system_tools.PROJECTS_DIR + 'Utilities/PythonTemplates/' + self.project.proj_dir_prefix + '/settings.py" root@' + self.linode_attrs['ipv4'][0] + ':~/settings.py',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa "' + self.REQUIREMENTS_DIR + self.project.proj_dir_prefix + '_requirements.txt" root@' + self.linode_attrs['ipv4'][0] + ':~/type1_requirements.txt',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa "' + self.LINUX_CONFIG_DIR + self.project.proj_dir_prefix + '_hosts" root@' + self.linode_attrs['ipv4'][0] + ':~/hosts',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa "' + self.LINUX_CONFIG_DIR + self.project.proj_dir_prefix + '_config.json" root@' + self.linode_attrs['ipv4'][0] + ':/etc/config.json',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa "' + self.LINUX_CONFIG_DIR + self.project.proj_dir_prefix + '_http.conf" root@' + self.linode_attrs['ipv4'][0] + ':~',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa "' + self.BASH_SCRIPT_DIR + self.project.proj_dir_prefix + '_stack_script.sh" root@' + self.linode_attrs['ipv4'][0] + ':~',
            'scp -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa -r "' + self.project.PROJECT_ROOT_DIR[:-1] + '" root@' + self.linode_attrs['ipv4'][0] + ':~',
            'ssh -i ' + system_tools.SSH_DIR + self.project.proj_dir_prefix + '_id_rsa root@' + self.linode_attrs['ipv4'][0] + ' "chmod 700 ' + self.project.proj_dir_prefix + '_stack_script.sh; source ' + self.project.proj_dir_prefix + '_stack_script.sh"',
        ]

        # Run each config command in list
        for config_cmd in server_config_cmds:
            sys.stdin.flush()
            if 'settings.py' in config_cmd:
                print('Copying Django settings file to server...')
            elif 'StrictHostKeyChecking no' in config_cmd:
                print('Copying sshd_config file to server...')
            elif 'known_hosts -R' in config_cmd:
                print('Adding ' + self.linode_attrs['ipv4'][0] + ' to known_hosts...')
            elif 'hosts" root@' in config_cmd:
                print('Copying modified "hosts" file to server...')
            elif '_config.json' in config_cmd:
                print('Copying Django settings configuration file to server...')
            elif '_http.conf' in config_cmd:
                print('Copying modified Apache configuration file to server...')
            elif '_stack_script.sh" root' in config_cmd:
                print('Copying Bash stack script to server...')
            elif self.project.PROJECT_ROOT_DIR[:-1] + '" root@' in config_cmd:
                print('Copying ' + self.project.proj_dir_prefix + '_project directory to server...')
            elif 'ssh -i' in config_cmd:
                print('Running server stack script (might take awhile)...')
            proc_obj = subprocess.run(config_cmd, shell=True, capture_output=True)
            if proc_obj.stdout:
                print(proc_obj.stdout.decode())
            if proc_obj.stderr:
                print(proc_obj.stderr.decode())
            sys.stdout.flush()
        
        
    # Deletes the linode instance associated with the DjangoWebsite object
    def delete_linode(self):
        import subprocess, json

        try:
            delete_linode_cmd = 'curl -H "Authorization: Bearer '+self.linode_api_token+'" '\
                                '-X DELETE '\
                                'https://api.linode.com/v4/linode/instances/'+str(self.linode_attrs['id'])
            delete_linode = subprocess.run(delete_linode_cmd, shell=True, capture_output=True)
            self.linode_attrs = json.loads(delete_linode.stdout)
        except KeyError:
            print('There was no Linode associated with object when deletion was attempted.')

        # Just delete all Linode attributes and leave empty dictionary if non-existent linode deletion is attempted
        try:
            if self.linode_attrs['errors']:
                for error in self.linode_attrs['errors']:
                    if error['reason'] == 'Not found':
                        print('Attempted to delete a non-existent Linode instance.\n'\
                              'Linode attributes (linode_attrs) will be saved as empty.')
                        self.linode_attrs = {}
        except KeyError:
            pass

        # Save updated (deleted) attributes to website in database
        self.save_website()
        
        
        

        
        
        
