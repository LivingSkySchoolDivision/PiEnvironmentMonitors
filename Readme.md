# Setting up the script on a raspberry pi

# Initial set up on Raspberry pi

TODO

## Make a non-default user

`sudo adduser lssdadmin`
Give it a strong password, record it in KeePass

Add to sudoers group
`sudo usermod -aG sudo lssdadmin`

Enable sudo without password
`sudo nano /etc/suders.d/lssd`
```
lssdadmin ALL=(ALL) NOPASSWD:ALL
```

## Enable UFW

1. `ufw allow 22`
2. `ufw allow 80`
3. `ufw enable`

This guide assumes you have a raspberry pi already set up, with Python installed.

The scripts in this repository require **Python3**, and will not work with Python2.

## Create a directory for the script to live in
`mkdir /temperature`

## Install and set up NGINX

1. `sudo apt-get update`
2. `sudo apt-get install nginx`

Edit the configuration

`sudo nano /etc/nginx/sites-enabled/default`

You can replace the entire default file with the following:
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        root /var/www/html;
        index index.json
        server_name _;
        location / {
                try_files $uri $uri/ =404;
        }
}
```

Restart nginx
`sudo service nginx restart`

## Set up crontab
Log in a a **non-root** user (the script will fail if it's run by root)
`crontab -e`

(Choose nano if it prompts you)

Add the following line at the bottom
```
* * * * *  python3 /temperature/GenTempJSON.py > /var/www/html/index.json
```
