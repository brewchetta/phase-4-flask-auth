# Flask / React Deployment

## Intro

The purpose of this lecture repo is to show how deployment works with the render service. In order to make this work, you must first sign up for a free render account at https://render.com/ where your site will be hosted.

## Install Postgresql

The first step here will be to install postgresql onto your computer and make sure that it's running. This process depends on your OS but can easily be searched on the internet.

## Create a Database on Render

In your Render dashboard choose to create a new postgresql database from the dashboard. The name and region are important (you'll most likely choose Ohio), everything else should be left as is and considered optional. Be sure to select `hobby project` for the pricing model.

Very importantly, this database will disappear around the 60 day mark so be ready to reset it often while job hunting.

The `External Database URL` on the following page will be important so make sure to copy it down somewhere.

## Environment

Create a `.env` file at the root of the project. From there follow these steps to load your `.env` variables into flask...

In your terminal:

```bash
pipenv install python-dotenv
```

Somewhere near the start of `app.py` add:

```python
from dotenv import load_dotenv
load_dotenv()
```

Be sure to add the `.env` file to your `.gitignore` so your variables don't get pushed up to github.

At this point you'll add in a line to your `.env` file for postgresql. Create a line for the `POSTGRES_URL` and paste in the external url from the previous steps with Render.

```env
POSTGRES_URL=your_url_goes_here
```

Inside your flask project you'll need to change the `SQLALCHEMY_DATABASE_URI` to use your `POSTGRES_URL` rather than use the sqlite version. In `app.py` or `config.py` change `app.config['SQLALCHEMY_DATABASE_URI']` so it reads like this:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os`.env`iron.get('POSTGRESQL_URL')
```

It's also strongly recommended if you have any other secret keys or API keys that they get added with similar lines.

## React Build

Once your client directory is ready for prime time run `npm run build --prefix client` from the top directory or `npm run build` in the client directory. You should now be able to see `client/build` as a new directory. This should be added to your `.gitignore` by default but if not be sure to ignore it since it's just extra code.

The purpose of this is mainly to see whether React will build properly, this step will also happen when we deploy the site.

## Setting Default Flask Routes

We'll set up flask to default to react code if it doesn't hit a proper flask route. In app.py make amend these lines for the `app=Flask` and `@app.route('/')`:

```python
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")
```

This will enable flask to find and render the React code as a fallback route. You can try it now by starting your flask server and going to your normal `http://localhost:5555`.

## Additional Flask Config #####

We'll need to install a pair of packages for flask to run properly on render, specifically gunicorn which is what they utilize to run their flask servers:

```bash
pipenv install gunicorn psycopg2-binary
```

From here we add our application requirements to a file that render will read when downloading its own packages:

```bash
pipenv requirements > requirements.txt
```

## Configuring a New Render Project

Ok that was a lot but we're at the exciting part! Once done, you'll want to add and commit potentially on a `deployment` branch.

Go to the render dashboard and choose `New+` in the top right choosing `Web Service`. Use github to find your committed and pushed project (you should be able to choose the branch as well).

When creating your new web application be sure to add these configurations:

```
Environment: Python 3

Branch: main (or deployment)

Build Command: pip install -r requirements.txt && npm install --prefix client && npm run build --prefix client

Start Command: gunicorn --chdir app:app
```

At first the app will fail to build and that's totally ok because we need to add in one more bit of configuration in the `environment` tab:

```
PYTHON_VERSION=3.8.13
DATABASE_URI=whatever_postgresql_uri_you_got
```

You should also add any additional secret keys or API keys that are in your regular `.env` file.

## Conclusion

From here your app should build and run! Because this is the free tier, be ready for it to remain at the back of any queues and load slowly during busy times. Additionally, your app will "go to sleep" after a period of time and take upwards of a minute to wake up and reload in certain circumstances.

Additionally, depending on the configurations you chose then any changes to your deployed branch should eventually make their way onto your rendered website.

Nevertheless, congrats! You have a fullstack application on the internet!