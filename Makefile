export PYTHONPATH=.

format:
	pre-commit run -a

start_min:
	docker-compose -f ugc_infra/docker-compose.min.yml up -d
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml up -d
	docker-compose -f etl/docker-compose.etl.yaml up -d


stop_min:
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml down -v
	docker-compose -f ugc_infra/docker-compose.min.yml down -v
	docker-compose -f etl/docker-compose.etl.yaml down -v


start:
	docker-compose -f ugc_infra/docker-compose.infra.yml up -d
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml up -d
	docker-compose -f etl/docker-compose.etl.yaml up -d


stop:
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml down -v
	docker-compose -f ugc_infra/docker-compose.infra.yml down -v
	docker-compose -f etl/docker-compose.etl.yaml down -v


