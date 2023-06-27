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

Notes:

Send credentials from frontend

Find user with the username

Make sure they put in the correct password

Confirmation message that they're logged in

Set a cookie --> browser information
HTTP/HTTPS is STATELESS

Once cookies is set....

When we refresh:

Check the cookie on the backend to make sure it's valid

If user attached to cookie...

Send that user info back

To log out DESTROY THE COOKIEEEEEEE
