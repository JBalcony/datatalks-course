<!-- 
layout: template
title: Docker Installation Notes
filename: installation.md -->


# 1. Docker

### 1.1 Docker login / permission denied

  `sudo chmod 666 /var/run/docker.sock`

  [chmod](http://www.chmod.pl/chmod-666.html)

### 1.2 Docker Compose
   [Linux manuall install](https://docs.docker.com/compose/install/#install-compose)

  * `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
  
  * `sudo chmod +x /usr/local/bin/docker-compose`
   
### 1.3 Run Docker as non-root user (without sudo)

Create the docker group.

 `sudo groupadd docker`

Add your user to the docker group.

 `sudo usermod -aG docker $USER`

### 1.4 Start Docker on boot

 **systemd** manages which services start when the system boots
 
 
# 2. VS CODE

### 2.1 Installation


### Ubuntu based distributions

The easiest way to install Visual Studio Code for Debian/Ubuntu based distributions is to download and install the [.deb package (64-bit)](https://go.microsoft.com/fwlink/?LinkID=760868), either through the graphical software center if it's available, or through the command line with:

```bash
sudo apt install ./<file>.deb

# Older Linux distribution:
# sudo dpkg -i <file>.deb
# sudo apt-get install -f # Install dependencies
```


```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
```

Update the package cache and install the package using:

```bash
sudo apt install apt-transport-https
sudo apt update
sudo apt install code # or code-insiders
 
`sudo systemctl enable docker.service`

`sudo systemctl enable containerd.service`

to disable use `disable`
