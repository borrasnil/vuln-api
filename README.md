# Vulnerable API lab
Explore common vulnerabilities in APIs and exploit them in a safe enviroment.

---

## Instalation
```bash
git clone https://github.com/borrasnil/vuln-api.git 
cd vuln-api
docker compose up --build
```

## Docker compose scheme
!! This project is only meant to run in a safe local network, database password and Flask key are hardcoded into `docker-compose.yml` !!
1. PostgreSQL container starts and initializes
2. Health check monitors PostgreSQL readiness
3. Flask API waits for PostgreSQL to be healthy, then starts
4. Nginx starts after Flask API is running
5. Application is fully operational
