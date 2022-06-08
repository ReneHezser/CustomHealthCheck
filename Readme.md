# Docker Healtheck Sample

This sample allows Docker to check if a running container is healthy. Most solutions I found to implement a health check used a webserver for it. I wanted a simple solution that worked on one of my Python containers without a running webserver.

## How does it work?

A file within the container keeps track of the status of the container. It is created during startup and filled with a *0* until the logic determines that the container is not healthy anymore. In that case a *1* is written to the file.

The dockerfile contains the healthcheck. It will execute a file that just checks for the file content.

## Implementation

### dockerfile

```docker
HEALTHCHECK --interval=10s --timeout=3s \
  CMD ["bash", "/app/check-running.sh"]
```

## Check the status of a running container

```bash
docker inspect --format='{{json .State.Health}}'
```