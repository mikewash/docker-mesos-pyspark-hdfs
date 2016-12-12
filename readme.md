These scripts allow you to simulate a multi-node Mesos cluster for running Spark using Docker containers (except for Hadoop, which is currently configured only as a single node).

With a little modification of IP addresses this can easily be adapted to an actual multi-node deployment.

The basic arrangement is this:

- a Docker host machine, which also acts as the Spark _client_ (where Spark tasks are submitted from). This is what you are building images and running containers on.
- Docker container(s) running a Mesos master process to act as a leader
- Docker container(s) running a Mesos slave process to act as a follower

Almost everything is handled via the `run` script.

### Client setup

If you don't have `docker` and `docker-compose`, run:

    ./run install_docker

This also pulls the `ubuntu:14.04` image which is used as the base for the other images.

The client also needs an installation of Mesos and Spark to properly submit jobs to the cluster.

These can be setup by running:

    ./run install_mesos
    ./run install_spark


### Running the Mesos Cluster

These containers and examples are from this project, https://github.com/mesosphere/docker-containers/tree/master/mesos

For Master

```
docker run -p 5050:5050 -d --net=host \
  -e MESOS_PORT=5050 \
  -e MESOS_QUORUM=1 \
  -e MESOS_REGISTRY=in_memory \
  -e MESOS_LOG_DIR=/var/log/mesos \
  -e MESOS_WORK_DIR=/var/tmp/mesos \
  -v "$(pwd)/log/mesos:/var/log/mesos" \
  -v "$(pwd)/tmp/mesos:/var/tmp/mesos" \
  mesosphere/mesos-master:0.28.0-2.0.16.ubuntu1404
```

For Slaves

```
docker run -p 5051:5051 -d --net=host --privileged \
  -e MESOS_SWITCH_USER=0 \
  -e MESOS_PORT=5051 \
  -e MESOS_LOG_DIR=/var/log/mesos \
  -v "$(pwd)/log/mesos:/var/log/mesos" \
  -e MESOS_MASTER=<ip address of the mesos master>:5050 \
  mesosphere/mesos-slave:0.28.0-2.0.16.ubuntu1404
```

### Running the example

This program generates 10000 letters and does a letter count and prints out a list of the letters in ascending order of the top 50.

python example5.py <ip address of the mesos master>

Make sure the ip address is the same as the one you inputted for the slave or you will get this error message in the logs of the master and slave

Failed to shutdown socket with fd 7: Transport endpoint is not connected

or you will see this message after running the script

Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources

### Checking progress 

http://<public ip address for mesos master>:5050/#/

This link will show you if your slave is properly connected with your master

### Other tools

The `run` script provides some other commands useful for development and testing:

- `ips` - list ips of docker containers
- `rmi` - remove all mesos-related images and dangling images
- `rmc` - stop and remove all mesos-related containers
- `nuke` - runs `rmc` and `rmi`
