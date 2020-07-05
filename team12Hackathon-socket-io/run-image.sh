docker kill team12-socket-io
docker rm -v team12-socket-io
docker container run --name team12-socket-io --network=host --detach team12-socket-io:0.1a
