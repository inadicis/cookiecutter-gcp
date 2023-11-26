# GCP Cookiecutter

This is a mirror/fork from the Ella Cookiecutter to make it findable from github, and explore more
options.

Project Template for backend services. Provides easy project creation through a command line
interface (cookiecutter), with the configuration of the tech-stack provided ( especially GCP CI/CD
pipeline, but also logging, databases, fastapi, socketio, pubsubs, ssr etc.).

## How to use this cookiecutter?

### Fast version

In order to create a new project that uses this cookiecutter as template, you will need to:

- (Assuming your current working directory is where you want to create a new project)
- Clone this repository `ella-cookiecutter`
- Create a virtual environment and activate it.
- Install the requirements: `pip install -r requirements.txt`
- Execute `cookiecutter ella-cookiecutter`
- In terminal, you can now see it waiting for your input. Enter a value for each param (directory
  name etc.), or press `Enter` to use the default. Those are all the options for the new repo.
- Your new project should now be created. Execute `ls` to verify a new directory with your
  specified name was created
- Find the next steps in the `<your_project_slug>/README.md` and with the `TODO-CONFIG` in the
  generated repo.

### Alternative

- You can also use the cookiecutter without cloning it before hand, as long as you
  have `cookiecutter`, `black` and `ruff` installed.
  then you can execute `cookiecutter https://bitbucket.org/ella_ai/ella-cookiecutter/src/stable/`
  (use either branch `main` or tag `stable`)

## What does this cookiecutter contain?

### Base Components

#### Git

- Git was initialized in the generated repo.
- There is a gitignore already, excluding common files, the `.env` file, as well as the `logs` and
  the `local`
  directories
- The auto-formatting step was added as separated commit
- the default branch is `main`

#### Webapp + tests

- FastAPI (REST) app
- env variables parsing from file (.env) and from process environment
- pytest with HTTPX (and mongomock) allowing async tests
- using fixture/factories to prepare required data

#### CI-CD, GCP deployment

- docker to build the app (not meant to be used locally)
- docker-compose to start a mongoDB with docker (for local development)
- cloudbuild.yaml (two versions,
    - one for building a new image, testing it and saving it in the artifacts registry
    - one for deploying a new revision (usable for all deploy environments through substitutions)
- For local deployment: environment variables can be set in the `deployment/.env` file
    - You can define multiple `.env` files, e.g. `.env.dev-db`, `.env.local-db`. You will simply
      have to update the `EnvSettings.model_config.env_file` value

#### Logs

- Logs for local deployment and for tests (two separate files in directory `/logs`)
- Logs for deployment in GCP

### Options (require input while creating)

_in order of prompting_

#### database - Setup of a DB connection

1. No setup
2. Setup for MongoDB through ODM beanie and driver motor.io (asynchronous)
3. Setup for MongoDB through pymongo driver (synchronous)
4. Setup for MongoDB through motor.io driver (asynchronous)
5. (WIP) Setup for SQL connection

#### use_socketio - Websockets with Socket.io

Whether to include (Yes/No) setup code for a socket.io (event-driven) application
mounted to the fastapi app.

#### use_graphql - GraphQL app

Whether to mount (Yes/No) a strawberry graphQL application to the fastAPI app (includes a basic
ping pong example).

#### use_gcp_pubsubs - Google Cloud PubSubs

Whether to include (Yes/No) example code for publishing and receiving messages of a push
subscription (using the GCP PubSub product).

- Example subscription - push route, decoding etc.
- Example publish to PubSub Topic

#### use_filters_package - Server Side Rendered Filters

Whether to include (Yes/No) code for dynamically rendered filter options for any DB resource,
using the private package `ella-filteraspi`.

#### use_auth0 - Authentication and Authorization

Whether to include (Yes/No) code for authentication and authorization of users following oauth2,
through JWTs and JWKS provided by an auth0 tenant.
Contains code for authentication via google authentication as well.

- Auth0
    - Connection to auth0 to retrieve jwks and logic to decode and validate JWTs, usable in any
      route
      with `Security(get_user(), ["your:permission"])` as parameter in a route.
- GoogleAuth for service accounts
- Authentication is mocked in tests and local deployment (via a hardcoded public/private key in
  this repo), so they can
  run without internet connection, with easier
  permission attribution. (For local dev, this can be deactivated with an environment
  variable `MOCK_AUTH` set to
  false (see `EnvSettings` class))

#### use_server_side_rendering - SSR Graphical User Interface

- Whether to add setup for jinja templates as well as an example to have the ability to
  setup a GUI using server side rendering.

#### use_gradio - Gradio Graphical User Interface

Whether to mount (Yes/No) a basic gradio UI to the fastAPI app.

## How to maintain this cookiecutter

- I recommend using a virtualenv that has all possible dependencies
  installed (`pip install -r all_possible_requirements.txt`).
- [there is one test](test_generation.py) that tries to generate a new repo for each possible
  cookiecutter variable combinations. The repo is created
  in [the directory generated_repos](generated_repos), and is deleted after the test if the test
  passed successfully. To make the repo not deleted if the test failed (cookiecutter default), you
  have to overwrite some cookiecutter code (see tutorial in the test).
- After generating a repo, the post_gen_hook runs the tests in this repo (so you have tests running
  inside a test, testception here we go), as well as ruff. This helps catching mistakes when
  maintaining this cookiecutter.
- A useful trick sometimes is to append filenames with the `.jinja` extension (keep the real
  extension before the `.jinja`: e.g. `main.py.jinja`) to have templating syntax
  highlighting. No worries the post_gen_hook will delete all unwanted `.jinja` file-suffixes for
  you.
- The test might take a lot of time. You can run it in parallel (thanks xdist)
  with `pytest -n auto test_generation.py`.


