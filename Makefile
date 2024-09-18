build:
	docker-compose up --force-recreate --build

rm:
	sudo rm -rf ./pgdata

rebuild: rm build

dev:
	docker-compose up

deploy:
	docker-compose up -d
