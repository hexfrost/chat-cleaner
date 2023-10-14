build:
	docker-compose -f docker-compose.dev.yml --env-file .env.docker up --force-recreate --build

rm:
	sudo rm -rf ./pgdata

new-build-and-migrate: rm
	docker-compose -f docker-compose.migrate.yml --env-file .env.docker up --build --force-recreate

rebuild: rm build

dev:
	docker-compose -f docker-compose.dev.yml --env-file .env.docker up
