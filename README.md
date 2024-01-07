
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=kea-semester-1_Semester-Project&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=kea-semester-1_Semester-Project)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=kea-semester-1_Semester-Project&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=kea-semester-1_Semester-Project)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=kea-semester-1_Semester-Project&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=kea-semester-1_Semester-Project)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=kea-semester-1_Semester-Project&metric=bugs)](https://sonarcloud.io/summary/new_code?id=kea-semester-1_Semester-Project)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=kea-semester-1_Semester-Project&metric=coverage)](https://sonarcloud.io/summary/new_code?id=kea-semester-1_Semester-Project)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=kea-semester-1_Semester-Project&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=kea-semester-1_Semester-Project)
# Project Source Code

Access the complete source code of the project on GitHub: [Semester Project Repository](https://github.com/kea-semester-1/Semester-Project).

- **API Documentation**: Auto-updated via Github actions, visible [here](https://github.com/kea-semester-1/Semester-Project/blob/main/docs/API_DOCUMENTATION.md)
- **DB Dumps**: Database dumps for MongoDB and Neo4j, here [here](https://github.com/kea-semester-1/Semester-Project/tree/main/db-dumps)


# Project Setup Instructions

## Using AWK

If AWK is installed on your system, execute the following command from the project's root directory:

```bash
make run
```


## Using Docker Compose

In the absence of AWK, execute the following docker-compose command from the project's root directory:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```


This command sets up docker containers, initializing the project and databases. It also loads test data into the databases.
Look inside the `Makefile`, to see every command available.

## Project Deployment

- **Backend**: Deployed on Azure, accessible [here](https://rpg-project.azurewebsites.net/api/docs).
- **Frontend**: Hosted on Vercel, available [here](https://semester-project-ochre.vercel.app/login).

## Running Tests

### With AWK

```bash
make test
```

### With Docker Compose

Execute the following command:

```bash
docker container exec $(docker ps | grep api-1 | awk '{print $1}') pytest ./rpg_api/tests/pytest -s
```

# Test Data Scripts

## Relational Database Scripts

Access the relational database scripts on GitHub:
- [Main DB Scripts](https://github.com/kea-semester-1/Semester-Project/tree/main/db-scripts)
- [Startup Data Script](https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/web/startup_data_pg.py)
- **Audit Log**: Trigger/function in migration file [here](https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/db/postgres/migrations/versions/2023-12-14-17-28_f24e163963f2.py)

## Document and Graph Database Scripts

For Document and Graph databases, test data is managed by the backend application upon startup:
- [MongoDB Startup Data Script](https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/web/startup_data_mongo.py)
- [Neo4j Startup Data Script](https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/web/startup_data_neo4j.py)
