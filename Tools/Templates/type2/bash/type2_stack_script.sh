#!/bin/bash
yes | apt-get update && yes | apt-get upgrade
hostnamectl set-hostname proj_dir_prefix
mv ~/hosts /etc/hosts
yes | apt-get install apache2
apt-get install libapache2-mod-wsgi-py3
yes | apt-get install python3-pip
yes | apt-get install python3-venv
apt-get install ufw
ufw default allow outgoing
ufw default deny incoming
ufw allow ssh
yes | ufw enable
adduser admin << END_OF_INPUTS
insecurepassword
insecurepassword
n/a
n/a
n/a
n/a
n/a
y
END_OF_INPUTS
adduser admin sudo
mkdir /home/admin/.ssh
cp .ssh/authorized_keys /home/admin/.ssh/authorized_keys
mv proj_dir_prefix_project /home/admin/
mv settings.py /home/admin/proj_dir_prefix_project/proj_dir_prefix_project/
mv proj_dir_prefix_http.conf /etc/apache2/sites-available/
a2ensite proj_dir_prefix_http.conf
a2dissite 000-default.conf
chown :www-data /home/admin/proj_dir_prefix_project/db.sqlite3
chmod 664 /home/admin/proj_dir_prefix_project/db.sqlite3
chown :www-data /home/admin/proj_dir_prefix_project/
chmod 775 -R /home/admin/proj_dir_prefix_project/
chmod 700 /home/admin/.ssh
chmod 600 /home/admin/.ssh/authorized_keys
python3 -m venv /home/admin/proj_dir_prefix_project/django_venv
source /home/admin/proj_dir_prefix_project/django_venv/bin/activate
pip install -r type1_requirements.txt
python /home/admin/proj_dir_prefix_project/manage.py collectstatic
deactivate
ufw allow http/tcp
service apache2 restart
exit
