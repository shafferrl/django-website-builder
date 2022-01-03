from django import forms
from pr0j3ct_n4m3_project.settings import APP_EMAIL, ADMIN_EMAIL

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    from_email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message_content = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        from django.core.mail import send_mail, BadHeaderError
        from django.http import HttpResponse
        from django.contrib import messages

        try:
            send_mail('pr0j3ct_n4m3 Contact | ' + subject,
                      '<From> ' + name + '\n<Email> ' from_email + ' \n\n<Message> ' + message_content,
                      APP_EMAIL,
                      [ADMIN_EMAIL])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        messages.success(self.request, 'Thank you for contacting pr0j3ct_n4m3!')
    
