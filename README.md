# poke-berries-statistics-api

A simple api that gathers the names of all berries from **poke-api** (https://pokeapi.co/docs/v2#berries) as well as 
calculates statistics based on their growth time:
- minimum growth time
- median growth time
- max growth time
- variance growth time (the used formula is for population variance, not sample)
- mean growth time
- frequency of growth times

There are two endpoints:
**/allBerryStats (GET)** - gets the name of all berries and the statistics mentioned above
**/histogram (GET)** - create a histogram for the growth times

The application is currently deployed to Oracle Cloud Platform and can be accessed at http://158.180.60.63:8080/.

For running the application locally it is assumed that you have created a virtual environment using venv for Python 3.12.
Once that is done, clone this repo, open a terminal, activate the virtual environment and follow the steps:
1. Change the current directory to this project.
2. Install pipenv: `pip install pipenv` 
3. Install all required dependencies: `pipenv install`
4. From inside this repo run: `export PYTHONPATH='.' && python poke_berries_statistics_api/app/api.py`

If you have Docker installed and make command line tool installed, you can run (from the project's directory)
the application simply by typing `make run`. For stopping and deleting the running container run `make reset`. 
If you just want to build the Docker image run `make build`. If you don't have access to make, then just run the docker
commands separately:

    docker build . -t poke-berries-stats-api
    docker run -d -p 8080:8080 --restart always --name poke-berries-stats-api poke-berries-stats-api
The app should be available at http://localhost:8080.

Tests can be run by using `pytest poke_berries_statistics_api/tests/`. 

Tests can also be run with code coverage by using
`pytest --cov=poke_berries_statistics_api poke_berries_statistics_api/tests/ --cov-config .coveragearc`.

Last, but not least, there are a few environmental variables that can be configured in the .env file:

POKE_API_PAGE_LIMIT - its selection can impact the speed of obtaining all the berries from poke-api

CALCULATE_TIME - if set to True the execution time for some functions will be saved to the log file

POKE_API_URL - URL of poke api; should only be changed if the developers of poke api upgrade it with a new version or
change it for any reason in the future.

LOGS_LEVEL - for minimum level of logs recorded; should be one of DEBUG, INFO, WARNING, ERROR or CRITICAL.

RESET_LOGS - if False, the log file will not be reset when the app is running

CACHING_DIR - directory for caching used by flask_caching

Some future improvement ideas:
- adding a CI/CD pipeline which will automatically run all tests when creating a merge request or merging
- mapping a domain name to the IP address
- improving security by integrating SSL certification verification step