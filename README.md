![CI status](https://github.com/ssichynskyi/web_metric_collection/actions/workflows/run_checks_and_tests.yml/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c88e5519a03f4fccb996837298f43f7d)](https://www.codacy.com/gh/ssichynskyi/web_metric_collection/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ssichynskyi/web_metric_collection&amp;utm_campaign=Badge_Grade)
# Web metric collector-producer

- [What it does](#what-it-does)

- [How to run](#how-to-run)
  - [Command line options](#command-line-options)

- [Out of scope](#out-of-scope)

- [Known issues](#known-issues)

## What it does
Implements a service that monitors website availability over the network, produces metrics:

- http response time
- http response status code
- availability of pre-defined text

... and sends this along with other data to Kafka broker at Aiven (as a Kafka producer).
Service can be started separately or used like a package.

## How to run
This is a python program, therefore you need Python3.9 for the execution and pipenv of version 2020.11.15 or close
for the creation of virtual environment
To run service with default parameters from shell, go to service project root folder and run:
```console
$pipenv shell
$python3.9 src/service.py
```

### Command line options
Service takes the default values of its settings from config/service.yaml file and partially from its own body.
For convenience, there's a possibility to overwrite most of these params using keyword arguments.
To get help, from the project root
```console
$pipenv shell
$python src/service.py --help

usage: service.py [-h] [--url URL] [--topic TOPIC] [--cycles CYCLES] [--pattern PATTERN] [--sleep SLEEP]
optional arguments:
  -h, --help         show this help message and exit
  --url URL          url to collect web metrics from, no quotes. Defaults to specified in service.yaml
  --topic TOPIC      topic name to publish, no quotes. Defaults to website-metrics
  --cycles CYCLES    number of cycles to run, infinite if not specified
  --pattern PATTERN  regexp to look at website. Defaults to one specified in service.yaml settings
  --sleep SLEEP      seconds to wait between broker polling, defaults to service.yaml settings
```

## Out of scope
- script to set up, configure, run and delete Aiven Kafka broker (assumption: always available)

- any optimization of multiple calls like async/await. Assumption - service shall
  not collect metrics too often or from too many websites.

- any optimization related to Kafka broker messaging. Same assumption as above.

- implementation of the service as a background service / daemon. For the testing task
  it hardly has any practical reason while complicates testing because of IPC layer.

- testing kafka producer with Aiven kafka broker (only done on E2E level)

- any additional environment setups / checks (like local dummy website, etc)

## Known issues
- smoke test for Kafka producer fails with SSL error. The reason is unclear.
  Possible workaround - to use SASL authentication instead of providing certificates

## ToDo
- move constants to separate module (fix this in tests and in service)
- update service usage here
- improve logging
- adjust CI
- move common code into separate repo and connect as submodule (authentication)
- improve import system
- add local kafka and postgres configuration for testing
- add containerized CI testing -> using kafka and postgres containers
- improve mock (with patching) if possible
- add commit hooks and CI manipulations
- change docu strings to restructuredText and add automatic formatting by black
- add automatic docu-string creation
