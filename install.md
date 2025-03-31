### ssh into server

```
ssh -i privatekey.openSSH [ip|hostname]
```

### Update & Upgrade & Download github-repository Downloader & cd into repo-dir & execute install Script
```
apt update
apt upgrade -y
apt install git curl expect -y 
wget https://raw.githubusercontent.com/Izzy3110/cloudserver-install/refs/heads/main/download.sh
bash download.sh
cd cloudserver-install
bash install.sh
```
