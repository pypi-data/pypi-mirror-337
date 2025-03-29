Typically, sending metrics to Datadog requires installing a Datadog agent on the same host as your service. This library provides a simpler alternative, allowing you to send metrics directly to Datadog without an agent installation. It offers basic support for counters and gauges.

```python
from statsutil import Stats

stats = Stats(site="US3", api_key='123123123123')

stats.inc("counter1")
stats.gauge("gauge1", 10)
```
