format:
	ruff check . --fix
	ruff format

requirements:
	uv export --no-hashes --no-dev --format requirements-txt > requirements.txt

build_docker:
	@make requirements
	@docker compose -f docker-compose.yaml build

run_docker:
	@make export_env
	@docker compose -f docker-compose.yaml up

export_env:
	@rm .env; exit 0
	set >> .env