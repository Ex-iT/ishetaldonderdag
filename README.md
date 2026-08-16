# IsHetAlDonderdag.nl

A rebuild of the original `ishetaldonderdag.nl` based on Python 3.14 and [Flask 3.x](https://flask.palletsprojects.com/).

## Development

Create a virtual environment:

```bash
python3.14 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

To start a local development server on port `5000` run:

```bash
flask --app index.py --debug run
```

## Attribution

Icons made by [Becris](https://www.flaticon.com/authors/becris) from [www.flaticon.com](https://www.flaticon.com/).
