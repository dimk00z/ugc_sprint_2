# API UGC

## Описание

Реализован API для загрузки сообщений в Kafka

### Endpoints

`http://{ip-address}:8000/api/openapi` - Генерированное описание OpenAPI

`http://{ip-address}:8000/api/v1/produce` - пишет сообщение об одном событии

`http://{ip-address}:8000/api/v1/batch_produce` - пишет массив сообщений об одном событии

`http://{ip-address}:8000//api/v1/random_batch_produce?batch_count=1000` - "ручка" для дебага, пишет batch_count валидных собщений, включена/выключена по переменной окружения `DEBUG=True|False`


### Формат сообщения

```json
{
  "payload": {
    "movie_id": "1ec4cd73-2fd5-4f25-af68-b6595d279af2",
    "user_id": "1ec4cd73-2fd5-4f25-af68-b6595d279af2",
    "event": "some_event",
    "event_data": "some_event_data",
    "event_timestamp": 1621932759
  },
  "language": "RU",
  "timezone": "Europe/Moscow",
  "ip": "192.168.1.1",
  "version": "1.0",
  "some_client_data": "some_client_data"
}
```

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

API:

```bash
cp .env_example .env
docker-compose -f docker-compose.api_ugc.yaml up -d
docker-compose -f docker-compose.api_ugc.yaml down -v
```
