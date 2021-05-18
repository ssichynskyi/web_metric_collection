# Service function
Implements a service that monitors website availability over the network, produces metrics:
- http response time
- http response status code
- availability of pre-defined text
and sends this to Kafka broker at Aiven (as a Kafka producer)

### Out of scope
- script to setup, configure, run and delete Aiven Kafka broker
- any optimization of multiple calls like async/await. Assumption - service shall
not collect metrics too often or from too many websites.
- any optimization related to Kafka broker messaging. Same assumption as above.
- implementation of the service as a background service / daemon. For the testing task
it hardly has any practical reason while complicates testing because of IPC layer.

## ToDo:
- add unit tests for service
- add integration tests for service
- extract / create documentation
- create CI for unit test execution
- create CI for integration test execution
- add E2E tests with and without regexp pattern
- add E2E tests with invalid website
