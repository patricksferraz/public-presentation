docker network create \
    -d bridge postgres-network
docker run \
    --network=postgres-network \
    --name postgres-address \
    -e POSTGRES_PASSWORD=$POSTGRES_PW \
    -d postgres
docker run \
    --network=postgres-network \
    -p 80:80 \
    -e PGADMIN_DEFAULT_EMAIL=$PGADMIN_DE \
    -e PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DP \
    -d dpage/pgadmin4
