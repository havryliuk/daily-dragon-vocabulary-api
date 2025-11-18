# daily-dragon

## Local Development
### Install dependencies
```bash
pip install -r requirements.txt
```
### Run tests with coverage
```bash
pytest --cov=.
```

### Run app locally
```bash
uvicorn daily_dragon.daily_dragon_app:app --reload
```