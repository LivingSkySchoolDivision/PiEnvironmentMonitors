# Setting up a new temperature monitor on a raspberry pi

Set up a Raspberry pi with *Raspbian Buster Lite*, or the most recent headless (desktop-less) distribution of Raspbian.

You **must** complete these steps as a sudoable user from the start - Python components will fail to run if you don't, and you may have to start over.

Update your OS before continuing
```
sudo apt update
sudo apt full-upgrade
```

## Enable SSH access
Follow the instructions found at https://www.raspberrypi.org/documentation/remote-access/ssh/

## Configure Raspbian (hostname, static IP, password)

Use the built-in `raspi-config` menu to:
1. Change the password to the `pi` user to something unique
2. Set a static IP
3. Change the hostname to something memorable

```
sudo raspi-config
```

## Enable and configure UFW
1. `sudo apt install ufw`
2. `sudo ufw allow 22`
3. `sudo ufw allow 80`
4. `sudo ufw enable`

## Install required software and libraries

```
sudo apt update
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
sudo apt install git python3-pip libgpiod2 nginx python3-libgpiod
pip3 install adafruit-circuitpython-dht gpiozero adafruit_dht
```

## Create a directory for the script to live in
```
sudo mkdir /temperature
sudo chown pi /temperature
```

## Use git to clone this repository into your new folder
```
cd /temperature
git clone https://github.com/LivingSkySchoolDivision/PiEnvironmentMonitors.git .
```
Make sure you keep the period at the end, it's important.

## Copy the Python script so that you can customize it
The script in this repository should be renamed before you use it. This is so that this software repository doesn't overwrite your custom script if you use Git to update the repo.

```
cp GenTempJSON-TEMPLATE.py GenTempJSON.py
```

Keep in mind that Linux is case-sensitive - if you name your file differently, you will need to use your version of the filename when editing the crontab (below).

## Replace Nginx config with a custom one
A custom nginx configuration file is included in this repository ([nginx.conf](nginx.conf))
```
sudo rm /etc/nginx/sites-enabled/default
sudo cp ./nginx.conf /etc/nginx/sites-enabled/
```
Alternatively, you can edit the nginx config so that the "index" setting includes "index.json".

This config file does not support SSL encryption.

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
The number of asterisks in this line is important.

## Finished!

Your raspberry pi should now be checking the temperature every minute, and serving that data over http in json format. Access it via your raspberry pi's IP address using a web browser.

Find your device's IP address by running the following command, or by plugging your Raspberry Pi into a screen (it should be displayed on the screen if nobody is logged in).
```
ifconfig
```
Should get you the following output:
```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.177.54.82  netmask 255.255.254.0  broadcast 10.177.55.255
        inet6 fe80::13ee:20eb:49d1:af53  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:66:eb:8b  txqueuelen 1000  (Ethernet)
        RX packets 314711  bytes 32694125 (31.1 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 5192  bytes 570310 (556.9 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```
The IP address in the above output is **10.177.54.82**

```
http://10.177.54.82
```

```
{
 "Hostname": "raspberrypi",
 "TemperatureCelsius": 24.0,
 "Humidity": 7.0,
 "LastScan": "2020-02-10 15:08:01.916936+00:00",
 "errmessage": "",
 "iserror": false
}
```

# How to update your script from this repository after you've installed it

Assuming your paths are the same as in the instructions above, updating your copy of this repository is as easy as running the following commands on the device (via SSH or in person):

```
cd /temperature
git pull
```

This shouldn't update your copy of the Python script, assuming you've named yours `GenTempJSON.py`.
