# Ejemplo en Python

## Comandos utiles en desarrollo

### Limpiar el repositorio

```shell
git clean -dx -e ".vs*" -e "env" -e ".env" -e "*.sqlite3" -f
```

### Test coverage

```shell
coverage run --source='.' manage.py test --noinput
coverage report --show-missing
coverage html
coverage xml
rm .coverage coverage.xml
```

## Docker
