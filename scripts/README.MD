# Scripts for GreenGrass

## systemctl script for Raspberry Pi

1. Softlnk `greengrassd.service` to /etc/systemd/system 
2. Enable and start the GreenGrass Daemon `sudo systemctl enable greengrassd && sudo systemctl start greengrassd`
3. Check the process is running ````ps -fp `cat /run/greengrassd.pid` ````