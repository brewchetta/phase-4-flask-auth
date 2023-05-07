# Flask Authentication

## Learning Goals

- Use the session object to authenticate a user

- Securely store the password in a hash

- Use the session object to determine when a user is logged in

- Authorize only certain resources depending on whether a user is logged in

## Getting Started

Fork / clone the repo and run
```bash
pipenv install
```

To start the client, create a separate terminal and run:
```bash
npm install --prefix client
npm start --prefix client
```

To start the server:
```bash
pipenv shell
cd server
flask db upgrade
flask run --debug
```
