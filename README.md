# Web metric collector-producer

- [What it does?](#what-it-does)
- [Out of scope](#out-of-scope)
- [ToDo](#todo)

## What it does?
Implements a service that monitors website availability over the network, produces metrics:
- http response time
- http response status code
- availability of pre-defined text
and sends this along with other data to Kafka broker at Aiven (as a Kafka producer).
Service can be started separately or used like a package.

## Out of scope
- script to set up, configure, run and delete Aiven Kafka broker (assumption: always available)
- any optimization of multiple calls like async/await. Assumption - service shall
not collect metrics too often or from too many websites.
- any optimization related to Kafka broker messaging. Same assumption as above.
- implementation of the service as a background service / daemon. For the testing task
it hardly has any practical reason while complicates testing because of IPC layer.
- testing kafka producer with Aiven kafka broker (only done on E2E level)
- any additional environment setups / checks (like local dummy website, etc)

## ToDo:
- create CI for unit test execution
- create CI for integration test execution (?)
