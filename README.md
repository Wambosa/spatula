# Spatula
_A web scraping system. Named by Lori Diaz whilst watching Great British Bake-off._

# Table of Contents

* [C4 Diagrams](#c4-diagrams)
* [System Requirements](#system-requirements)
* [Running Local](#running-local)
* [Test Overview](#test-overview)
* [Deploy Overview](#deploy-overview)
* [Contributing](#contributing)

-----

## C4 Diagrams
![c4 context](./docs/c4-context.svg)
![c4 container](./docs/c4-container.svg)
![c4 container scoped](./docs/c4-container-scoped.svg)


## System Requirements
- Ubuntu 18.x
- python 3.7
  - `python` not `python3`
- docker
- docker-compose
- awscli

## Running Local
_install+shim will establish all dependencies for local runs._

Before running locally, ensure that the proper system requirements are met.
Then,
```
make install
make shim
```

Calling `make run` will rebuild the target script in the `.build/` direectory, 
and execute the `main.py` with any provided run arguments.

```
make run FUNC=scrape RUN_ARGS=' \
--raw_bucket=raw-data \
--s3_endpoint=http://localhost:4572 \
--db_host=127.0.0.1 \
--db_port=13306 \
--db_name=optimal \
--db_user=root \
--db_pass=password \
--target=https://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591 \
--target_shape=php_bb \
--target_protocol=html \
--out_file=../../thread.csv
'
```

## Test Overview
Before running tests, ensure that the proper system requirements are met. 
Then, `make install`.

Unit tests can be called with `make test`.
Additionally linting is available for both the business logic language and IaC _(terraform)_ with `make lint`.
Both commands should be wired up in any CI/CD solution.

```
make test
make lint
```


## Deploy Overview _(Not implemented, will be done in sprint X story SPAT-4567)_
Manual deploys are possible directly from the command line if the appropriate permissions are configured.

```
export AWS_ACCESS_KEY_ID=AAAAAAAABBBBBBBCCCCCC
export AWS_SECRET_ACCESS_KEY=******************************
export AWS_DEFAULT_REGION=us-west-2

export TF_VAR_rds_user=bot
export TF_VAR_rds_pass=password
```

```
make build deploy TARGET=role ENV=lab
make build deploy TARGET=network ENV=lab
make build deploy TARGET=aurora ENV=lab
make build deploy TARGET=ecs ENV=lab
```

These commands can be easily wired up to a CI/CD pipeline.
The builds and deploys can be triggered by events specified by the team _(on push, on merge to master, on tag, etc)_.


### Contributing
_Changing the system, adding a new method or updating an existing method._

1. Tests should be invoked with `make test` after changes.
2. A test runner can be activated with `make watch`.
3. Run `make lint` before push and fix any hangups. _(ci/cd will catch it if you dont)_.


-----


### Optional Dependency install tips

pyenv+awscli
```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

...(configure your shell)...

pyenv virtualenv 3.7.0 example
pyenv activate example
make install
```

docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)"  -o /usr/local/bin/docker-compose \
&& sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose \
&& sudo chmod +x /usr/bin/docker-compose
```


-----


### Future
_given more time_

  - need to complete the ECR/ECS terraform example
  - spellcheck
  - show how to connect to the rds behind vpc
    - likely jump host
  - complete IaC as shows in diagram
  - complete the docker build and deploy
  - flesh out a better db schema after examininig other sources.
  - try to integrate pylint with pytest instead of standalone
  - optimize build scripts
  - support full context injection _(i rushed this and the context is therefore not easily testable)_
  - implement retry _(in infra, not code)_
  - move out local lib into a repository manager _(like nexus)_
    - especially the `transform.py` which could be a lib for all parsing business logic
  - use typing consistently
  - implement a real logging solution
  - fill out comment docs more
  - error handling
  - check Makefile compatibility with local apple/windows _(I only dev on ubuntu these days for python)_
  - abstract serializer to support various output types _(json, yml, csv, etc)_
  - way more unit tests for all the `src/lib/`
  - implement snapshots for some tests with large comparisons
  - deal with pytest warnings
  - more obvious ready-state for successfully run `make shim`
    - currently when done, it just waits and logs activity, no setup confirm message.

-----
