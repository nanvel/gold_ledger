# Gold Ledger

## Development

Backend:
```shell
docker-compose up --no-start && docker-compose start
alembic upgrade head
ENV=test alembic upgrade head

uv build
uv pip install -e .

gold_ledger dev-server
```

Frontend:
```shell
cd web
nvm use 22
npm install
npm run dev
```
