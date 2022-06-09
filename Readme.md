# Docker Healtheck Sample

This sample allows Docker to check if a running container is healthy. Most solutions I found to implement a health check, used a webserver for it. I wanted a simple solution that worked on one of my Python containers without a running webserver.

## How does it work?

A file within the container keeps track of the status of the container. It is created during startup and filled with a **0** until the logic determines that the container is not healthy anymore. In that case a **1** is written to the file.

The dockerfile contains the healthcheck. It will execute a file that just checks for the file content and report the current status of the container.

![unhealthy container](/assets/unhealthy_container.png)

## Implementation

A very simple Python script will simulate failures.

### app.py

The [app.py](/app.py) writes to a file */app/system-status.txt* within the container on startup. A condition with a random generator will simulate an error condition and write it to the mentioned file.

### check-running.sh

This file reads the content of the state file and exists with that code. This is required by the docker healthcheck in the dockerfile.

### dockerfile

To enable healthcheck of the container, add it to the dockerfile.

```docker
HEALTHCHECK --interval=10s --timeout=3s \
  CMD ["bash", "/app/check-running.sh"]
```

## Testing

Since Docker ist not respecting the health status for restarting it, you need to force restarting of unhealthy containers.

### Check the status of a running container

```bash
docker inspect --format='{{json .State.Health}}' customhealthcheck
```

### Autoheal

```bash
docker run -d --rm --name autoheal \
    -e AUTOHEAL_CONTAINER_LABEL=all \
    -v /var/run/docker.sock:/var/run/docker.sock \
    willfarrell/autoheal:latest
```

The container will detect the healthstatus of other containers, and restart them.

![healed container](/assets/healed_container.png)

## Links

- [Restarting an unhealthy docker container based on healthcheck](https://rotadev.com/restarting-an-unhealthy-docker-container-based-on-healthcheck-dev/)
- [autoheal](https://hub.docker.com/r/willfarrell/autoheal) container by [Will Farrell](https://github.com/willfarrell)
- [Portainer](https://www.portainer.io/) Container Management Made Easy