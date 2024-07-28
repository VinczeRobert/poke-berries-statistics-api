FROM python:3.12-slim
EXPOSE 8080
WORKDIR /poke_berries_statistics_api

COPY Pipfile Pipfile.lock ./
COPY ./poke_berries_statistics_api ./poke_berries_statistics_api
RUN pip3 install pipenv==2024.0.1
RUN pipenv install --system --ignore-pipfile --deploy --dev --verbose

CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8080", "poke_berries_statistics_api.app.api:app"]