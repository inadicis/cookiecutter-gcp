# Changelog Ella-Cookiecutter

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
More detail
in [our conventions](https://ellamedia.atlassian.net/wiki/spaces/FROGS42/pages/820805718/Project+Conventions)

## Unreleased

## [3.0.0] - 2023-11-26

### Changed 
- Fork from ella-cookiecutter
- renamed to cookiecutter-gcp 

### Removed
- Filters-api option, as the package is currently private.

## [2.4.0] - 2023-10-16 - [Ella-Cookiecutter]
### Added
- Documentation for each available option in the [README.md](README.md)

### Changed
- Order of user input options, to have them grouped by topic and relevance. 

## [2.3.0] - 2023-10-13

### Added

- Template side:
    - pre-generation hook validates versions of python (>=3.9) and cookiecutter (>=2.1)
    - post-generation hook dumps installed dependencies in the `cookiecutter.jsonl` file
- (Generated Repo Side) Check for installed requirements before tests run
- Documentation: Introduction to the topic deploying on GCP in the generated README
- Directory `{{cookiecutter.__project_slug}}/cookiecutter`  for all traces of the generation.

### Changed

- `cloudbuild.yaml` now deploys a revision on dev environment, not only building and storing an
  image (+ improved readme on this topics)
- Move `{{cookiecutter.__project_slug}}/cookiecutter.json` to
  `{{cookiecutter.__project_slug}}/cookiecutter/cc_context.jsonl`.
- Postgen appends to existing file `cc_context.jsonl` instead of creating one
- Move post generation instructions to `{{cookiecutter.__project_slug}}/cookiecutter/TODOs.md`

### Fixed

- Import of templates in example SSR route
- Cloudbuild:
    - Newlines in yaml multilines (set-env)
    - set-secrets if no secrets

## [2.2.0] - 2023-09-18

### Changed

- Generated Repo Side
    - Upgrade to pydantic v2 (update requirements, validators, model configs)

## [2.1.0] - 2023-09-18

### Added

- Template Side:
    - New cookiecutter option `use_graphql`
- Generated Repo Side:
    - GraphQL Query schema with strawberry-graphql, mounted as a router to the fastAPI app under
      url `graphql`.
    - There are example Input/Types/Query/Resolvers and a commented out Mutation
      example. There is as well an example test.
    - GraphiQL and Introspection are deactivated on production
    - Depth, Token amount and Alias amounted are limited

## [2.0.0] - 2023-09-18

### Changed (Breaking)

- User facing behaviour
    - user expected inputs (instead of 1-2 for yes no, now “y” for yes, rest is No)
    - make option to run tests post gen private

### Changed

- docs
    - fix changelog title
    - simplify readme
    - add ADRs directory
- Template Side:
    - Refactor postgeneration hook (deletion/renaming of files, cli usage,
- Generated repo side:
    - improve conftest mocking, fixtures
    - refactor authentication: split it from authorization

### Added

- Generated Repo Side:
    - add black settings to pyproject.toml
    - build: update cloudbuilds to be more minimal with substitutions
- Template Side:
    - add truthy local jinja extension (and use it instead of string comparisons)
    - add human readable prompts

### Removed

- delete example_env

## [1.1.3] - 2023-08-21

- Added: cookiecutter context (variables and values) is dumped into `cookiecutter_context.json`
  just after generation
- Changed: Refactor generation test setup to be simpler

## [1.1.2] - 2023-07-24

- Fixed: imports of `config.routing` instead of `config.routers`

## [1.1.1] - 2023-07-24

- Changed: generated readme (Project structure, fix jinja conditionnals, better description of
  post-gen steps: TODO-CONFIG)
- Changed: cookiecutter readme (Delete documentation that belonged to generared readme, )
- Changed: renamed `config.routers` to `config.routing`
- Added: gitkeep to folders that should be gitignored but consistent for all devs

## [1.1.0] - 2023-07-24

- Change cloudbuild: One cloudbuild to build and test image, one for deployment, no matter the
  environment
- Remove constant substitutions (e.g. `_PLATFORM`)
- Add cloudtraffic.yaml that redirects traffic to latest revision

## [1.0.1] - 2023-07-24

- Add Link to our conventions to the changelog
- Change cloudbuild: `--update-env-vars` -> `--set-env-vars` to delete previous env vars

## [1.0.0] - 2023-07-18 - commit ca41aac40be23eb7e42714428eb42ee8f9d874b3

- Warning: This section and all previous ones were retro-actively added and might miss some
  changes.
- Add WIP section to CHANGELOG.md

## 2023-07-11 - commit 6e583fe1bfcc448f7fb25ac16b600347bcd69263

- Change revision suffix of revisions (to include random number)
- Add revision tag for revisions

## 2023-07-10 - commit aa09797d64a30c35a2e0c6ba1dc1924d9da99db7

- Make postgen tests optional
- Add postgen db test (beanie, pymongo)
- Fix Beanie setup
- Change order of tests to run the minimal projects first
- Fix imports

## 2023-07-04 - commit b96bc8bad43fa639cc05656b89a33309fa66389b

- Add `EnvSettings.remote_environments` + other tiny EnvSettings improvements
- Fix test failing for minimal project

## 2023-07-03 - commit cf1ef5a89ebe9707652b0a6ba535e38c86d7ae0f

- Add gradio GUI option
- remove `cookiecutter.db_name`
- Improve jinja stripping newlines
- Change `cookiecutter.` defaults to be the minimal ones (No before Yes)

## 2023-06-30 - commit c4d2b98956308f14312bc987ef725f853352c8b8

- Add changelog to generated repo

## 2023-06-28 - commit 54622492bc24e04765cde76449a6041e9621b9d3

- Semver script: fix early return
- Fix cloudbuild.yaml files with multiple lines for envs and secrets
- Update requirements.txt
- Fix config imports
- Improve formatting post gen (with jinja newlines)

## 2023-06-26 - commit b35765c25264a0f3b4f09c9264bd4be8fad6d222

- Add semver script: cli to update version, commit, tag and push
    - see `-h` param for documentation of options
- Rename `Settings` to `EnvSettings`
- Add version, description, app name, contact, URLs to pyproject.toml
- Add `ProjectSettings` that parses and validates the pyproject.toml at app-launch
- Add SSR with jinja
- Add postgen step that removes all untagged `.jinja` suffixes of generated files
- Improve cloudbuild.yaml files
- Refactor authentication, tests setup, app init, configuration, pubsub logic
- Add Pubsub publish example
- Add logging for 422 Validation errors
- Add running tests in postgen hook
- Multiple fixes (generation of repo, resulted logic, file deletion)
- Add option to connect to remote DB even if deployed locally through env variable `use_local_db`
- Add `all_possible_requirements.txt` for easier testing of generation
- Move `asyncapi.yaml` to `docs` folder, move jwks to own file, delete `constants.py`
- Make auth0 optional (`cookiecutter.use_auth0`)
- Add tests for each `cookiecutter.` variable
- Add possibility to run generation tests in parallel
- Improve README

## 2023-03-22 - commit b545e1e21caafb003cf7b97d5034982d1869d976

- Improve `Settings`
- Add google auth logic
- Add Pubsub example route
- Add pyproject.toml
- Add ruff
- Refactor postgen hook
- Add `/wsdocs` specification rendered from `asyncapi.yaml` for
  `cookiecutter.use_socketio == "Yes"`
- Refactor socketio config

## 2023-02-10 - commit 8ce5236f7724953ddd5fe4b4ba76ee9833795f73

- Add example socketio app (ping)
- Update README
- fixes for combination socketio + mvc

## 2023-02-07 - commit 04eb07fa3245cb8d59a1eb1566649d59d9b73fc5

- Rename `app` to `src`
- Add more files to be removed postgen
- add socketio option
- Improve `Settings`
- Rename some `cookiecutter.` variable values to standard `"Yes" "No"`
- Fix GCP values (image name, service name)
- Add auth0 secrets

## 2023-02-06

- Add `cookiecutter.use_mvc`, `cookiecutter.use_filters_package`, `cookiecutter.keep_examples`
- Remove `cookiecutter.contact_email`, `cookiecutter.project_slug`, `app_name` -> only default
  value is kept
- Update Dockerfile and cloudbuild.yaml
- Rename Examples classes (`Prompt`) to `MyResource`
- Add post_gen removal of unused files
- Multiple fixes, for `cookiecutter.use_mvc = "No"` to use auth + db, for beanie/pymongo

## 2023-24-01

- Remove filters (extract it to its own package: filters-api)
- Changed: make `cookiecutter.python_version` a choice
- remove `cookiecutter.git_initial_branch` -> `main` is the default branch name
- change some `Settings` defaults and validators

## 2023-24-01

- Add sorting option to filters

## 2023-06-01

- cookiecutter with variables
    - project_name
    - project_slug
    - app_name
    - app_description
    - contact_person
    - contact_email
    - python_version
    - auth0_domain_name
    - gcp_service_prefix
    - gcp_image_name
    - db_name
    - repo_name
    - git_initial_branch

TODO-CONFIG: Update changelog
