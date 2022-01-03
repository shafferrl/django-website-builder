"""
Tools for interacting with project resources based
on the internet.

"""
# Relevant library imports
import os

# General web variables and functions

email_addr = 'emailconfirmautomation@yahoo.com'
email_login_url = 'https://login.yahoo.com/?.src=ym&.lang=en-US&.intl=us&.done=https%3A%2F%2Fmail.yahoo.com%2Fd'
email_username = email_addr.split('@')[0]

linode_login_url = 'https://login.linode.com/login'


# Logs into email account.  Takes Selenium webdriver object as parameter.
def email_login(selenium_webdriver):
    # Confirm Linode account via email
    print('Retrieving email login page...')
    selenium_webdriver.get(email_login_url)

    # Try to locate username input and if can't be found assume already logged in
    while True:
        try:
            selenium_webdriver.find_element_by_xpath('//*[@data-test_id="mail-left-rail"]')
            break
        except:
            pass
        try:
            # Input and submit email username
            email_user_input = selenium_webdriver.find_element_by_id('login-username')
            email_user_input.clear()
            email_user_input.send_keys(email_username)
            print('Submitting email username...')
            email_user_input.submit()
            
            # Input and submit email password
            email_password_input = selenium_webdriver.find_element_by_id('login-passwd')
            email_password_input.send_keys(os.environ.get('AUTOEMAIL_PASS'))
            email_login_btn = selenium_webdriver.find_element_by_id('login-signin')
            print('Submitting email password...')
            email_login_btn.click()
            break
        except:
            continue


# Clears email inbox once already logged in.  Takes Selenium webdriver object as parameter.
def email_clear_inbox(selenium_webdriver):
    # Find "select all" button / checkbox and select
    select_all_btn = selenium_webdriver.find_element_by_xpath('//*[@data-test-id="checkbox"]')
    select_all_btn.click()

    # Find "delete" button and click
    delete_btn = selenium_webdriver.find_element_by_xpath('//*[@data-test-id="toolbar-delete"]')
    delete_btn.click()


# Logs out of email account.  Takes Selenium webdriver object as parameter.
def email_logout(selenium_webdriver):
    # Click on account icon
    user_icon = selenium_webdriver.find_element_by_id('ybarAccountMenu')
    clickable_user_icon = user_icon.find_element_by_xpath('..')
    clickable_user_icon.click()
    
    # Find logout button
    account_pane = selenium_webdriver.find_element_by_id('ybarAccountMenuBody')
    logout_btn = account_pane.find_elements_by_tag_name('a')[4]
    print('Logging out of email account')
    logout_btn.click()

    

