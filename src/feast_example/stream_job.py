"""stream_aggregate example."""

# pyright: reportUnknownMemberType=false
import json

from denormalized import Context
from denormalized.datafusion import col
from denormalized.datafusion import functions as f
from denormalized.datafusion import lit

bootstrap_server = "localhost:9092"

sample_event = {
    "occurred_at_ms": 100,
    "sensor_name": "foo",
    "reading": 0.0,
}

ctx = Context()
ds = ctx.from_topic("temperature", json.dumps(sample_event), bootstrap_server)

# pyright: reportUnknownMemberType=false
ds = ds.window(
    [col("sensor_name")],
    [
        f.count(col("reading"), distinct=False, filter=None).alias("count"),
        f.min(col("reading")).alias("min"),
        f.max(col("reading")).alias("max"),
        f.avg(col("reading")).alias("average"),
    ],
    1000,
    None,
).filter(col("max") > (lit(113)))
