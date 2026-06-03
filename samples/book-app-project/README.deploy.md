Deployment instructions for the sample book app

Build locally with Docker:

```bash
cd samples/book-app-project
docker build -t bookkeeper-app:local .
```

Run the container (interactive CLI):

```bash
docker run --rm -it -v "$(pwd)/data.json:/app/data.json" bookkeeper-app:local python book_app.py list
```

Or use docker-compose for an interactive shell session:

```bash
cd samples/book-app-project
docker-compose run --rm bookkeeper-app list
```

Run tests inside the image:

```bash
docker run --rm bookkeeper-app:local pytest -q
```
