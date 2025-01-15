# Gold Ledger

## Development

```
docker-compose up --no-start && docker-compose start
alembic upgrade head
ENV=test alembic upgrade head
```