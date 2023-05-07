# Flask Authentication

## Learning Goals

- Use the session object to authenticate a user

- Securely store the password in a hash

- Use the session object to determine when a user is logged in

- Authorize only certain resources depending on whether a user is logged in

## Getting Started

Fork / clone the repo and run `pipenv install`.

To start the client, create a seperate terminal and run `npm install --prefix client` followed by `npm start --prefix client`.

To start the server, first run `pipenv shell` and `cd server`. Then run `flask db upgrade` and `flask run --debug`.
