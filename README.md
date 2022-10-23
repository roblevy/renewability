# Renewability

A renewable energy game which, coincidentally, is a way for me to show off
about all my various software powers. 🥷

## Running the stack

```bash
docker-compose up
```

## Starting the wind generator

```bash
docker-compose exec weather scripts/generate_wind
```

## Reading Kafka topics to the console

```bash
docker-compose exec kafka read-topic <TOPIC_NAME>
```
