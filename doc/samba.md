## samba service
raspberry pi run command to open Samba server
```bash
sudo apt-get update
sudo apt-get install samba samba-common-bin
```
config smb.conf 
```bash 
sudo nano /etc/samba/smb.conf
```
Add the following at the end of the file
```bash
[share]  
path = /home/pi 
valid users = pi   
browseable = yes 
public = yes  
writable = yes   
```
Restart service and add Samba shared user, Input password
```bash
sudo service smbd restart
sudo smbpasswd -a pi
```
Enter in the computer: \\local ip (local ip is raspberry pi ip),Access to shared folders