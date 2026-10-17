# Deployment guide

## Streamlit Community Cloud

1. Push this folder to a Git repository.
2. Create a new Streamlit app pointing to `app.py`.
3. Add API settings as secrets, not committed `.env` files.
4. Use a persistent external PostgreSQL database for multi-user deployments; SQLite is suitable for demos only.

## Docker

```bash
docker build -t cricbuzz-livestats .
docker run --rm -p 8501:8501 cricbuzz-livestats
```

## Render/Railway/Azure/AWS

Run the container or start command `streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT`. Store `DATABASE_PATH`, `CRICBUZZ_BASE_URL`, and API credentials in the platform's environment variable manager.
