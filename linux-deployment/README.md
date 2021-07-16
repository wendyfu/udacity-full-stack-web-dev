IP Address: 52.76.220.190
URL: http://ec2-52-76-220-190.ap-southeast-1.compute.amazonaws.com

### Software installed:
- PostgreSQL
- Python 3.5
- pip3
- virtualenv
- Apache2
- mod_wsgi-py3
- git

### Configurations:
- Update packages:
```
sudo apt-get update
sudo apt-get upgrade
```

- Change the SSH port from 22 to 2200
  - Run: `sudo nano /etc/ssh/sshd_config`
  - Change the port number from 22 to 2200
  - Restart SSH: `sudo service ssh restart`

- Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow 123/udp
sudo ufw deny 22
sudo ufw enable
```

- Enable access for user `grader`
  - Create new user `grader`: `sudo adduser grader`
  - Give sudo permission to `grader`:
    - Run: `sudo visudo`
    - Add `grader  ALL=(ALL:ALL) ALL`

- Create an SSH key pair for `grader` using the `ssh-keygen` tool
 - On the local machine:
  1. Run: `ssh-keygen`
	2. Enter file name `grader_key` which will be saved in the local directory `~/.ssh`
	3. Enter in a passphrase twice. Two files will be generated ( `~/.ssh/grader_key` and `~/.ssh/grader_key.pub`)
	4. Run `cat ~/.ssh/grader_key.pub` and copy the contents of the file
	5. Log in to the `grader`'s virtual machine
 - On the grader's virtual machine:
	1. Create a new directory called: `mkdir .ssh`
	2. Run: `sudo nano ~/.ssh/authorized_keys` and paste the content into this file, save and exit
	3. Give the permissions: `chmod 700 .ssh` and `chmod 644 .ssh/authorized_keys`
	4. Check in `/etc/ssh/sshd_config` file if `PasswordAuthentication` is set to `no`
	5. Restart SSH: `sudo service ssh restart`

- Configure local timezone to UTC
Run: `sudo dpkg-reconfigure tzdata`

- Install and configure Apache to serve a Python mod_wsgi application
  - Install Apache: `sudo apt-get install apache2`
  - Install the Python 3 mod_wsgi package: `sudo apt-get install libapache2-mod-wsgi-py3`
  - Enable mod_wsgi: `sudo a2enmod wsgi`

- Install and setup PostgreSQL
  - Install PostgreSQL: `sudo apt-get install postgresql`
  - Login as user postgres: `sudo su - postgres`
  - Get into terminal: `psql`
  - Create database `catalog` and provision user `catalog`:
    `CREATE DATABASE catalog;`
    `CREATE USER catalog;`
  - Set password for user `catalog`:
    `ALTER ROLE catalog WITH PASSWORD 'catalog';`
  - Grant user `catalog` permission to database `catalog`:
    `GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;`

- Install git: `sudo apt-get install git`

- Setup deployment
  - Create `/var/www/catalog/` directory and put the catalog project inside
  - Install pip: `sudo apt-get install python3-pip`
  - Install the virtual environment: `sudo apt-get install python-virtualenv`
  - In `/var/www/catalog/catalog/` directory, run: `sudo virtualenv -p python3 venv3`
  - Change ownership to `grader`: `sudo chown -R grader:grader venv3/`
  - Activate new env: `. venv3/bin/activate`
  - Install the following dependencies:
```
pip install httplib2
pip install requests
pip install --upgrade oauth2client
pip install sqlalchemy
pip install flask
sudo apt-get install libpq-dev
pip install psycopg2
```
  - Run `deactivate` to deactivate

- Setup and enable virtual host
  - Add the following line in `/etc/apache2/mods-enabled/wsgi.conf` file to use Python 3:
    `WSGIPythonPath /var/www/catalog/catalog/venv3/lib/python3.5/site-packages`
  - Create `/etc/apache2/sites-available/catalog.conf` and add the following lines:
```
<VirtualHost *:80>
    ServerName 52.76.220.190
  ServerAlias ec2-52-76-220-190.ap-southeast-1.compute.amazonaws.com
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalog/>
    	Order allow,deny
  	  Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalog/static
    <Directory /var/www/catalog/catalog/static/>
  	  Order allow,deny
  	  Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
  - Enable virtual host: `sudo a2ensite catalog`
  - Reload Apache: `sudo service apache2 reload`

- Set up the Flask application
  - Create `/var/www/catalog/catalog.wsgi` file add the following lines:
```
activate_this = '/var/www/catalog/catalog/venv3/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/catalog/")
sys.path.insert(1, "/var/www/catalog/")

from catalog import app as application
application.secret_key = "super_secret_key"
```

- Adjust Flask application:
  - Rename the `application.py` file to `__init__.py` using: `mv application.py __init__.py`
  - Adjust database engine from sqlite to postgresql: `engine = create_engine('postgresql://catalog:PASSWORD@localhost/catalog')`
  - Update credentials in Google Console and update the `/var/www/catalog/catalog/client_secret.json`. Also update the reference in .py file.

- Restart Apache: `sudo service apache2 restart`

### References:
- https://help.ubuntu.com/community/UFW
- https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-ubuntu-16-04
- https://askubuntu.com/questions/138423/how-do-i-change-my-timezone-to-utc-gmt
- https://superuser.com/questions/1039369/create-a-python-3-virtual-environment
- https://flask.palletsprojects.com/en/0.12.x/deploying/mod_wsgi/#working-with-virtual-environments
- https://github.com/kamalneel178/Linux_Server_Configuration