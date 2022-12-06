A GitHub Action workflow for automating the collection of [crime and fire logs](https://dps.usc.edu/alerts/log/) posted by the University of Southern California's Department of Public Safety.

## Links

* Runner: [github.com/biglocalnews/usc-crime-reports-scraper/actions/workflows/etl.yaml](https://github.com/biglocalnews/usc-crime-reports-scraper/actions/workflows/etl.yaml)
* PDF collection: [documentcloud.org/app?q=%2Bproject%3Ausc-department-of-public--210827%20](https://www.documentcloud.org/app?q=%2Bproject%3Ausc-department-of-public--210827%20)
* Source: [dps.usc.edu/alerts/log/](https://dps.usc.edu/alerts/log/)

## Contributing

Fork the repository and clone the repository. Move into the code directory. Install the dependencies.

```bash
pipenv install --dev;
```

Install the pre-commit hooks.

```bash
pipenv run pre-commit install
```

Create a `.env` file and set the required DocumentCloud variables. You'll need to provide credentials with access to our project. Contact Ben Welsh if you need to be given access to the project.

```
DOCUMENTCLOUD_USER=
DOCUMENTCLOUD_PASSWORD=
DOCUMENTCLOUD_PROJECT_ID=usc-department-of-public--210827
```

Run the scrape command.

```bash
pipenv run python -m src.scrape
```
