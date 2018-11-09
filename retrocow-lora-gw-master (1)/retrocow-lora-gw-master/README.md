This project is modified based on WAZIUP project, customized for Retrocow Lorawan project.

### Pre requirement
#### Hardware
> [Raspberry Pi 3 B](https://pi-store.com/products/raspberry-pi-3-model-b?variant=34450610510) or [Raspberry Pi 3 B+](https://pi-store.com/products/raspberry-pi-3-b)

> [5V 2.4A Power Supply with MircoUSB](https://pi-store.com/products/5v-2-4a-switching-power-supply-with-20awg-microusb-cable)

> [8G+ Micro SD card]()

> [Retrcow Lorawan Radio Kit](https://pi-store.com/products) 

#### Software
> [Latest version of Raspbian Stretch Lite - Non-desk version](https://www.raspberrypi.org/downloads/raspbian/)

> [This github](https://github.com/lastcow/retrocow-lora-gw)


### Kit Installation
#### Install OLED display driver
Kit preinstall 0.9" OLED display model SH1106, we tested on Luma oled driver, you can install different drive and change code accordingly.

Enable I2C for Pi device by following command
```
$ sudo raspi-config
```

Install drive, substitute python3 for python in the following examples if you are using python3.
```
$ sudo apt-get update
$ sudo usermod -a -G i2c,spi,gpio pi
$ sudo apt install python-dev python-pip libfreetype6-dev libjpeg-dev build-essential
$ sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
$ pip install luma.oled
```
    

#### Install core project executable
```
$ sudo apt-get install git
$ sudo git clone https://github.com/lastcow/retrocow-lora-gw.git
$ cd retrocow-lora-gw
$ sudo make lora_gateway_retro
$ sudo chmod +x *.sh
```
and try following command
```
// Install psutil for reading system info
$ sudo pip install psutil
// Install google cloud lib before start (for push to google cloud server, will throw error due to the demo, but screen should works fine.
$ sudo pip install --upgrade google-cloud-pubsub
$ ./start.sh
```
if you see output on screen and oled display, means kit start successfully.


### Start gateway as service
create a file called lora.service as following:

```
[Unit]
Description=Retrocow Lorawan Gatway Service
After=network.target

[Service]
ExecStart=/home/pi/retrocow-lora-gw/start.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

setup service:
```
sudo mv lora.service /etc/systemd/system/.
sudo systemctl enable lora.service
sudo systemctl start lora.service
```
if device restart, the service will start automatically, if you see the screen is on and message display, means it start.

### Shutdown button
We integrated a shutdown button as well on the board, to make it works, create a file called pi3_shutdown.service:

```
[Unit]
Description=Retrocow RPi3 Shutdown Service
After=network.target

[Service]
ExecStart=/home/pi/retrocow-lora-gw/pi3_shutdown.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

setup service:
```
sudo mv pi3_shutdown.service /etc/systemd/system/.
sudo systemctl enable pi3_shutdown.service
sudo systemctl start pi3_shutdown.service
```

### Option
Once data been send to post python script: retrocow_lora_gw.py, you are free to use those data, here in example we send those data to google cloud pub/sub, then broadcast to different locations, if you like to use this feature, please follow google cloud tutorial to create a pub/sub topic and subscription.

### Retrocow Lorawan Kit Node Setup
Please following [Lora Node Temperature Sample](https://github.com/lastcow/iot-lora_node_temperature) to setup Lora node.

### Many thanks
- Zhijiang Chen (zhijiang@chen.me)
- Bo Yuan (hosyp11@yahoo.com)
