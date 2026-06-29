from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
  "airline_api_requests_total",
  "Total number of api requests",
  ['endpoint','method']
)

REQUEST_LATENCY = Histogram(
  "airline_api_request_latency_seconds",
  "API requests latency in seconds",
  ['endpoint']
)

CACHE_HITS = Counter(
 "airline_cache_hits_total",
 "Total redis cache hits",
 ['agent']
)

CACHE_MISSES = Counter(
  "ariline_cache_misses_total",
  "Total redis cache misses",
  ['agent']
)

KAFKA_EVENTS_PUBLISHED = Counter(
  "airline_kafka_events_published_total",
  "Total Kafka events publshed",
  ['topic']
)

