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

- Custom bridge network

- Database container
  · PostgreSQL 15

- Backend container
  · Flask API

- Frontend container
  · nginx reverse proxy 
  · Tailwind CSS
