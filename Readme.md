# Setting up a new temperature monitor on a raspberry pi

TODO

## Change the password for the pi user


## Enable and configure UFW
1. `sudo apt install ufw`
2. `sudo ufw allow 22`
3. `sudo ufw allow 80`
4. `sudo ufw enable`

## Install required software and libraries

```
sudo apt-get update
sudo apt-get install python3-pip libgpiod2 nginx
pip3 install adafruit-circuitpython-dht
```

## Create a directory for the script to live in
```
sudo mkdir /temperature
sudo chown pi /temperature
```

## Use git to clone this repository into your new folder
```
cd /temperature
git clone https://sourcecode.lskysd.ca/PublicCode/ServerRoomTemperatureMonitors.git .
```

## Rename the appropriate script

This repository contains several scripts for different sensors (The DHT11 and DHT22). 

Choose the appropriate one for the sensor that you are using, and copy that file to `GenTempJSON.py`. Your copy will be the script that the system actually uses.

Keep in mind that Linux is case-sensitive - if you name your file differently, you will need to use your version of the filename when editing the crontab (below).

```
cp GenTempJSON.py.DHT11 GenTempJSON.py
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