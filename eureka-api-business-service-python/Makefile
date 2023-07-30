DB_URL=postgresql://eureka_admin:admin@localhost:5432/test-admin?sslmode=disable

proto:
	rm -f ./src/protos/*.py
	python3 -m grpc_tools.protoc -I ./src/protos --python_out=./src/protos --grpc_python_out=./src/protos ./src/protos/business.proto

postgres:

	docker run --name postgres15-alpine -p 5432:5432 -e POSTGRES_USER=eureka_admin -e POSTGRES_PASSWORD=admin -d postgres:15-alpine

createdb:

	docker exec -it postgres15-alpine createdb --username=eureka_admin --owner=eureka_admin eureka_db

migrateup:

	alembic upgrade head

migratedown:

	alembic downgrade base


server:
	python src/main.py

.PHONY : proto