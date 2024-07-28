.PHONY: build
build:
	docker build . -t poke-berries-stats-api

.PHONY: reset
reset:
	docker stop poke-berries-stats-api
	docker rm poke-berries-stats-api

.PHONY: run
run: build
	docker run -d -p 8080:8080 --name poke-berries-stats-api poke-berries-stats-api
