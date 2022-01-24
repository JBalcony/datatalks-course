
layout: template
title: Docker Installation Notes
filename: installation.md


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
 
`sudo systemctl enable docker.service`

`sudo systemctl enable containerd.service`

to disable use `disable`
