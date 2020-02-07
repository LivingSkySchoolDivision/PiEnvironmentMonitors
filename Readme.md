# Setting up a new temperature monitor on a raspberry pi

TODO

## Change the password for the pi user


## Enable and configure UFW

1. `ufw allow 22`
2. `ufw allow 80`
3. `ufw enable`

## Install required software and libraries

```
sudo apt-get update
sudo apt-get install python3-pip libgpiod2 nginx
pip3 install adafruit-circuitpython-dht
```

## Create a directory for the script to live in
`mkdir /temperature`

## Use git to clone this repository into your new folder
```
cd /temperature
git clone https://sourcecode.lskysd.ca/PublicCode/ServerRoomTemperatureMonitors.git .
```

## Replace Nginx config with a custom one
A custom nginx configuration file is included in this repository ([nginx.conf](nginx.conf))
```
sudo rm /etc/nginx/sites-enabled/default
sudo cp ./nginx.conf /etc/nginx/sites-enabled/
```

Restart nginx
```
sudo service nginx restart
```
## Allow the pi user write access to the nginx www root

```
sudo chown pi /var/www/html
```

## Set up crontab
**As the *pi* user**, run `crontab -e`

(Choose nano if it prompts you)

Add the following line at the bottom:
```
* * * * *  python3 /temperature/GenTempJSON.py > /var/www/html/index.json
```

## Finished!

Your raspberry pi should now be checking the temperature every minute, and serving that data over http in json format.