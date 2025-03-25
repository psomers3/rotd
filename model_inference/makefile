format:
	uv run ruff check . --fix
	uv run ruff format

format-check:
	uv run ruff check .
	uv run ruff format --check

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

test:
	uv run pytest -s tests