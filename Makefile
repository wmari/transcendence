all: 
	mkdir -p /home/$(USER)/data/postgresql
	docker compose -f ./srcs/docker-compose.yml build
	docker compose -f ./srcs/docker-compose.yml up -d

logs:
	@docker p -q name=transcendence && docker logs transcendence || echo "Container 'transcendence' not running"
	@docker p -q name=postgresql && docker logs postgresql || echo "Container 'postgresql' not running"

clean:
	docker container stop postgresql transcendence || true
	docker network rm mynetwork || true
	docker system prune -af

fclean: clean
	docker volume rm srcs_postgresql
	@docker system prune -af

rebuild:
	@echo "Usage: make rebuild CONTAINER=<nom_du_conteneur>"
	@[ -n "$(CONTAINER)" ] && (docker compose -f ./srcs/docker-compose.yml build $(CONTAINER) && docker compose -f ./srcs/docker-compose.yml up -d $(CONTAINER)) || echo "Error: CONTAINER variable not set"

re: fclean all

.PHONY: all logs clean fclean