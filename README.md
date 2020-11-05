# Automat

## About Automat
Automat is a common proxy PLATER instances. It aggregates the apidocs
coming from multiple PLATER instances and displays them in the common platform.
Each of the PLATER instance can be accessed using it's `PLATER-TITLE`, 
eg. http://<automat-host>:8080/<plater-title>/predicates

## Running

Automat is currently supported to run in a containerized environment. 
We recommend using [docker](https://docker.com)

### Building image

#### Automat image
```bash
cd <repo-root>/Automat/
docker build --tag automat --no-cache .
```

#### Plater clustered mode Image
```bash
cd <repo-root>/Automat/plater-deploy
docker build --tag plater-clustered --no-cache . 
```

### Running

Populate the following values and store them in a `.env`.

##### Environment :
```bash
# WEB_HOST and WEB_PORT as used by both Automat and Plater containers.
 WEB_HOST=0.0.0.0
 WEB_PORT=8080
 # Neo4j settings
 NEO4J_HOST=<neo4j_host>
 NEO4J_USERNAME=<neo4j_user_name>
 NEO4J_PASSWORD=<neo4j_password>
 NEO4J_HTTP_PORT=<neo4j_http_port>
 PLATER_TITLE=plater
 PLATER_VERSION=2.0.0
 PLATER_SERVICE_ADDRESS=plater
 AUTOMAT_HOST=http://automat:8080
 # Used for Swagger docs change to host name where automat is served from.
 AUTOMAT_SERVER_URL=http://localhost:8080
```

#### Starting the containers:

Create docker network 
```bash
docker network create automat-network
```
Start Automat container. (Note: `--name` arg for docker run should match `AUTOMAT_HOST` value.)

```bash
docker run -d --env-file .env -p 8080:8080 --network automat-network --name automat  automat
```
Start PLATER container. (Note: `--name` arg for docker run should much `PLATER_SERVICE_NAME` value.)
```bash
docker run -d --env-file .env --network automat-network --name plater plater-clustered 
```
If Neo4j is also running as a docker container make sure it joins `automat-network`, 
this can be done via the command `docker connect automat-network <neo4j-container-name> `


#### Demo

A demo docker compose file is found in `<automat-root>/Automat/demo`. To run 
add config parameters to the `.env.sample` save it as `.env`:
```bash
cd <automat-root>/Automat/demo
docker-compose up 
``` 

 
 
