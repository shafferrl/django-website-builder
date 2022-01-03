"""
Tools for getting client information relevant to
building Django website project and payment.

"""
# Relevant module imports
import system_tools


# Class with methods to obtain client information and attributes for storing client info
class Client:
    client_info = {
        'client_name': '',
        'payment_info': {
            'card_no': '', 'card_expiry': '', 'card_zip': '',
            'card_cvv': '', 'name_on_card': '', 'address_1': '',
            'address_2': '', 'city': '', 'state': '', 'country': ''
        },
        'contact_info': {
            'email_address': '', 'phone_number': '',
            'address_1': '', 'address_2': '', 'city': '',
            'state': '', 'zip': ''
        }
    }
    
    def __init__(self, set_default=False, **kwargs):
        if not set_default and not kwargs:
            self.get_client_name()
            self.get_client_payment()
            self.get_client_contact()
        elif not set_default and kwargs:
            client_info = kwargs
        else:
            self.set_default_client()

    def set_default_client(self):
        import os
        
        self.client_info = {
            'client_name': os.environ.get('BILLING_FIRST_NAME') +' '+ os.environ.get('MIDDLE_NAME') +' '+ os.environ.get('BILLING_LAST_NAME'),
            'payment_info': {
                'card_no': os.environ.get('CC_01_NO'),'card_expiry': os.environ.get('CC_01_EXP_6DIGIT'),
                'card_zip': os.environ.get('CC_01_ZIP'), 'card_cvv': os.environ.get('CC_01_CVV'),
                'name_on_card': os.environ.get('BILLING_FIRST_NAME') +' '+ os.environ.get('BILLING_MI') +' '+ os.environ.get('BILLING_LAST_NAME'),
                'first_name': os.environ.get('BILLING_FIRST_NAME'), 'last_name': os.environ.get('BILLING_LAST_NAME'),
                'address_1': os.environ.get('BILLING_PO_BOX'), 'address_2': '',
                'city': os.environ.get('BILLING_CITY'), 'state': os.environ.get('BILLING_STATE_FULL'),
                'country': os.environ.get('BILLING_COUNTRY_CODE')
            },
            'contact_info': {
                'email_address': os.environ.get('EMAIL_PRIMARY'), 'phone_number': os.environ.get('PHONE_NUMBER'),
                'address_1': os.environ.get('BILLING_PO_BOX'), 'address_2': '', 'city': os.environ.get('BILLING_CITY'),
                'state': os.environ.get('BILLING_STATE_ABBR'), 'zip': os.environ.get('BILLING_ZIP')
            }
        }

    def get_client_name(self):
        
        while True:
            self.client_info['client_name'] = input('\nPlease enter the name to be\n'\
                                                    'associated with the client account: ')
            if self.client_info['client_name']:
                if self.client_info['client_name'] == 'self':
                    if not input('\nYou\'ve indicated this is a self-funded client project.\n'\
                                 'Press Enter again to confirm or enter any value to try again: '):
                        self.set_default_client()
                        break
                    else:
                        continue
                print(f'\nThe client account name is: {self.client_info["client_name"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nYou didn\'t enter anything!  Please try again.')
                continue
        
    def get_client_payment(self):

        # Prompt user for credit card number and check for valid format
        while True:
            self.client_info['payment_info']['card_no'] = input('\nPlease enter the payment card number: ')
            if self.client_info['payment_info']['card_no'].isdigit() and len(self.client_info['payment_info']['card_no']) >= 14:
                print(f'\nThe card number entered is: {self.client_info["payment_info"]["card_no"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nThe card number you entered is invalid.  Please try again.')
                continue


        # Prompt user for card expiration date and check for valid format
        while True:
            self.client_info['payment_info']['card_expiry'] = input('\nPlease enter the payment card\'s\n'\
                                                     'expiration date in the following format (MMYYYY): ')
            if self.client_info['payment_info']['card_expiry'].isdigit() and len(self.client_info['payment_info']['card_expiry']) == 6:
                print(f'\nThe expiration date entered is: {self.client_info["payment_info"]["card_expiry"][:2]}/{self.client_info["payment_info"]["card_expiry"][2:]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nThe expiration date format is invalid.  Please try again.')
                continue

        # Prompt user for card CVV and check for valid format
        while True:
            self.client_info['payment_info']['card_cvv'] = input('\nPlease enter the card\'s 3-digit CVV number (on back of card): ')
            if self.client_info['payment_info']['card_cvv'].isdigit() and len(self.client_info['payment_info']['card_cvv']) == 3:
                print(f'\nThe CVV entered is: {self.client_info["payment_info"]["card_cvv"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nThe CVV number you entered is invalid.  Please try again.')
                continue

        # Prompt user for card zip code and check for valid format
        while True:
            self.client_info['payment_info']['card_zip'] = input('\nPlease enter the card\'s billing zip code: ')
            if self.client_info['payment_info']['card_zip'].isdigit() and len(self.client_info['payment_info']['card_zip']) == 5:
                print(f'\nThe zip code entered is: {self.client_info["payment_info"]["card_zip"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nThe zip code entered is invalid.  Please try again.')
                continue

        # Prompt user for name on card and check for valid format
        while True:
            self.client_info['payment_info']['name_on_card'] = input('\nPlease enter the payer\'s name as it appears on the card: ')
            if self.client_info['payment_info']['name_on_card']:
                print(f'\nThe name entered is: {self.client_info["payment_info"]["name_on_card"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nYou didn\'t enter anything.')
                continue

        # Prompt user for first billing address line
        while True:
            self.client_info['payment_info']['address_1'] = input('\nPlease enter the first line of the\n'\
                                                   'billing address (street, P.O. box, etc...): ')
            if self.client_info['payment_info']['address_1']:
                print(f'\nThe address entered is: {self.client_info["payment_info"]["address_1"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nYou didn\'t enter anything.')
                continue

        # Prompt user for second line of billing address or skip if not applicable
        while True:
            self.client_info['payment_info']['address_2'] = input('\nPlease enter second line of mailing address\n'\
                                                   '(suite, apt, etc...) or leave blank if not applicable: ')
            if self.client_info['payment_info']['address_2']:
                print(f'\nThe second part of the street address entered is: {self.client_info["payment_info"]["address_2"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nPress "Enter" again to leave blank or enter "n" to retry: '):
                    break
                else:
                    continue

        # Prompt user for billing address state
        while True:
            self.client_info['payment_info']['state'] = input('\nPlease enter the billing address state: ')
            if self.client_info['payment_info']['state']:
                print(f'\nThe address entered is: {self.client_info["payment_info"]["state"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                print('\nYou didn\'t enter anything.')
                continue

        # Prompt user for billing address country or skip if US
        while True:
            self.client_info['payment_info']['country'] = input('\nPlease enter the billing address country or leave blank if US: ')
            if self.client_info['payment_info']['country']:
                print(f'\nThe second part of the street address entered is: {self.client_info["payment_info"]["country"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nPress "Enter" again if United States or enter "n" to retry: '):
                    self.client_info['country'] = 'US'
                    break
                else:
                    continue


    def get_client_contact(self):
        import re

        # Prompt user for email address and check if valid format
        while True:
            self.client_info['contact_info']['email_address'] = input('\nPlease enter contact email address: ').strip()
            if self.client_info['contact_info']['email_address']:
                # Basic test for valid email address but not a bulletproof regular expression
                if re.search(r'\S+@\S+\.\S+', self.client_info['contact_info']['email_address']):
                    print(f'\nYou entered the following email address: {self.client_info["contact_info"]["email_address"]}')
                    if system_tools.confirm_yes_no():
                        break
                    else:
                        continue
                else:
                    print('\nThe email entered was invalid.  Please reenter.')
                    continue
            else:
                print('\nEmail is a required field.  Please enter a contact email address.')

        # Prompt user for phone number and check if valid format
        while True:
            self.client_info['contact_info']['phone_number'] = input('\nPlease enter a phone number with no spaces or dashes or leave blank: ')
            if self.client_info['contact_info']['phone_number']:
                if self.client_info['contact_info']['phone_number'].isdigit() and len(self.client_info['contact_info']['phone_number']) == 10:
                    print('\nThe phone number entered is: ({}{}{}) {}{}{}-{}{}{}{}'.format(*self.client_info['contact_info']['phone_number']))
                    if system_tools.confirm_yes_no():
                        break
                else:
                    print('\nThe phone number entered was invalid.  Please retry.')
            else:
                if not input('Press "Enter" again to leave phone number blank.  Enter "n" to retry.'):
                    break
                else:
                    continue

        # Prompt user for mailing address and check if valid format
        while True:
            self.client_info['contact_info']['address_1'] = input('\nPlease enter first line of mailing address or\n'\
                                                   'leave blank if same as billing or decline to state: ')
            if self.client_info['contact_info']['address_1']:
                print(f'\nThe street address entered is: {self.client_info["contact_info"]["address_1"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nPress "Enter" again to skip address or enter "n" to retry: '):
                    break
                else:
                    continue


        while self.client_info['contact_info']['address_1']:
            self.client_info['contact_info']['address_2'] = input('\nPlease enter second line of mailing address\n'\
                                                   '(suite, apt, etc...) or leave blank if not applicable: ')
            if self.contact_info['address_2']:
                print(f'\nThe second part of the street address entered is: {self.client_info["contact_info"]["address_2"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nPress "Enter" again to leave blank or enter "n" to retry: '):
                    break
                else:
                    continue

        while self.client_info['contact_info']['address_1']:
            self.client_info['contact_info']['city'] = input('\nPlease enter the city for the mailing address: ')
            if self.client_info['contact_info']['city']:
                print(f'\nThe city entered is: {self.client_info["contact_info"]["city"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nYou entered a mailing address, which requires a city for mailing.\n'\
                             'If you meant to enter an address, enter "n" to retry.  Otherwise, leave blank to skip: '):
                    break
                else:
                    continue

        while self.client_info['contact_info']['address_1']:
            self.client_info['contact_info']['state'] = input('\nPlease enter the state for the mailing address: ')
            if self.client_info['contact_info']['state']:
                print(f'\nThe state entered was: {self.client_info["contact_info"]["state"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nA Mailing address was entered.  If state was meant to\n'\
                             'be entered, enter "n" to retry.  Otherwise, leave blank to skip: '):
                    break
                else:
                    continue

        while self.client_info['contact_info']['address_1']:
            self.client_info['contact_info']['zip'] = input('\nPlease enter the zip code for the mailing address: ')
            if self.client_info['contact_info']['zip']:
                print(f'\nThe zip code entered was: {self.client_info["contact_info"]["zip"]}')
                if system_tools.confirm_yes_no():
                    break
                else:
                    continue
            else:
                if not input('\nA Mailing address was entered.  If zip was meant to\n'\
                             'be entered, enter "n" to retry.  Otherwise, leave blank to skip: '):
                    break
                else:
                    continue
                
