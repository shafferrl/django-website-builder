import django_deployment_tools

django_website = django_deployment_tools.DjangoWebsite()
#django_website.ssh_keygen()
#django_website.create_package_reqs()
django_website.create_linode_acct()
