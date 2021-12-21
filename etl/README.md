# ETL UGC

## Описание

Реализован ETL для загрузки сообщений из Kafka в ClickHouse

### Инфраструктура

Минимальная сборка:

```bash
docker-compose -f ../ugc_infra/docker-compose.min.yml up -d
docker-compose -f ../ugc_infra/docker-compose.min.yml down -v
```

Инфраструктурная сборка:

```bash
docker-compose -f ../ugc_infra/docker-compose.infra.yml up -d
docker-compose -f ../ugc_infra/docker-compose.infra.yml down -v
```

ETL:

```bash
cp .env_example .env
docker-compose -f docker-compose.etl.yaml up -d
docker-compose -f docker-compose.etl.yaml down -v
```
