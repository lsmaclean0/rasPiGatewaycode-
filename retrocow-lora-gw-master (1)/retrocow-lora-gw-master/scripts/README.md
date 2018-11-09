This project contain python scripts for lora gateway process.

to set shutdown button python script as service:

create a file called pi3_shutdown.service as following:

```
[Unit]
Description=rp3 button push to shutdown service
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
if device restart, the service will start automatically, if you see the blue light is on, means it start.

pi3_shutdown.sh as following

```
#!/bin/bash
python /home/pi/retrocow-lora-gw/raspberry_pi3_shutdown.py
```

make pi3_shutdown.sh executable by following command:
```
sudo chmod +x pi3_shutdown.sh
```