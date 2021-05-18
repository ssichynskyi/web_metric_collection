# Service function
Implements a service that monitors website availability over the network, produces metrics:
- http response time
- http response status code
- availability of pre-defined text
and sends this along with other data to Kafka broker at Aiven (as a Kafka producer)

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
- extract / create documentation
- create CI for unit test execution
- create CI for integration test execution (?)
- add E2E tests with and without regexp pattern
- add E2E tests with invalid website
