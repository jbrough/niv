.PHONY: up

up:
	rm -rf data
	docker-compose up --build
