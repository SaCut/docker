# Docker and Kubernetes
- [Personal Docker-Hub account](https://hub.docker.com/repository/docker/savcut "SavCut DockerHub")

#### What is docker?
- Docker is a containerisation tool created by Google and later made open source and trasferred to the Linux foundation
- Docker helps create, modify, delete and otherwise manage containers 

#### Difference between containers and VMs
- A container is similar to a Virtual Machine in that both are closed boxes (separated from the host machine) on which to run software. The main difference between a VM and a container is that while a virtual machine simulates the whole operating system on which to run software, a container is only provided with the minimal necessary dependencies to run a specific application, and is therefore much more lightweight and faster, but while trading-off flexibility and scope.

#### Docker working diagram:
![img](https://imgur.com/2fPezMd.png)

#### Docker installation and setup
- Installing docker on linux is simple:
- `sudo apt update && sudo apt upgrade -y`
- Install docker dependencies with `sudo apt install apt-transport-https ca-certificates curl software-properties-common`
- add the GPG key `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
- add the PPA `sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`
- `sudo apt update`
- `sudo apt-get install docker-ce -y`
- Create an account on Docker-Hub
- run the command `docker login`
- insert your account credentials as required

#### Some commands:
- `docker --version`
- `docker run hello-world`
- `docker pull NAME-OF-IMAGE`
- `docker run NAME-OF-IMAGE` (it will download images from the public registry if not already present)
- run on ports `docker run -d -p 88:80 NAME-OF-IMAGE`
- delete image `docker rmi NAME-OF-IMAGE` or `docker rmi NAME-OF-IMAGE -f`
- checking running containers `docker ps`
- go into container `docker exec -it CONTAINER-ID`
- move/copy files between host and container `docker cp /source/file/path.txt CONTAINER:/dest/file/path/.txt`

#### Building customised images, microservices
- After editing an image, while still running:
- `docker commit !NAME!-OF-IMAGE OPTIONAL-TAGS` (it's recommended to tag the images with a dockerhub repo address, like `USERNAME/NAME-OF-REPO`)
- `docker push IMAGE`
