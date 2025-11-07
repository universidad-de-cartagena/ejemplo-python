# Ejemplo en Python

## Comandos utiles en desarrollo

### Limpiar el repositorio durante desarrollo

Es util limpiar archivos no deseados del ambiente de ejecucion durante desarrollo local.
Se consigue limpiar todos los archivos y directorios no rastreados por git con exclusiones sensibles
para desarollo local usando virtualenv, vscode o base de datos sqlite. Este comando muestra solamente.
Para eliminar sin confirmacion, usa opcion `-f`.

```shell
git clean -dx -e ".vs*" -e "env" -e ".env" -e "*.sqlite3"
git clean -dx -e ".vs*" -e "env" -e ".env" -e "*.sqlite3" -f
```

### Test coverage

Con la dependencia para generar reportes instalada, esto ejecuta todas las pruebas y generan reportes html o xml.

```shell
coverage run --source='.' manage.py test --noinput
coverage report --show-missing
coverage html
coverage xml
rm .coverage coverage.xml
```

Mira `scripts/docker-entrypoint.sh` para mas.
