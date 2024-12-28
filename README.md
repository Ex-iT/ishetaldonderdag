# IsHetAlDonderdag.nl

A rebuild of the original `ishetaldonderdag.nl` based on Python 3.11 and [Flask v2.3.3](https://flask.palletsprojects.com/).

## Development

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Install dependencies:

```bash
pipenv install --dev
```

To start a local development server on port `5000` run:

```bash
pipenv run flask --app index.py --debug run
```

## Attribution

Icons made by [Becris](https://www.flaticon.com/authors/becris) from [www.flaticon.com](https://www.flaticon.com/).
