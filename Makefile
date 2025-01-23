all: 
	mkdir -p /home/$(USERNAME)/data/postgresql
	docker compose -f ./srcs/docker-compose.yml build
	docker compose -f ./srcs/docker-compose.yml up -d

logs:
	docker logs transcendence
	docker logs postgresql

clean:
	docker container stop postgresql transcendence
	docker network rm mynetwork
	docker system prune -af

fclean: clean
	@sudo rm -rf /home/$(USERNAME)/data/postgresql
	@docker system prune -af

re: fclean all

.Phony: all logs clean fclean