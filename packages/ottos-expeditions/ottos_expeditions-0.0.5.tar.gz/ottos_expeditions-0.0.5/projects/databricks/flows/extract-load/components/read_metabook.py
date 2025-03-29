import polars as pl
import pyarrow as pa

from ascend.resources import read
from ascend.common.events import log
from ascend.application.context import ComponentExecutionContext


@read(
    strategy="incremental",
    incremental_strategy="merge",
    unique_key="id",
    on_schema_change="sync_all_columns",
)
def read_metabook(context: ComponentExecutionContext) -> pa.Table:
    df = pl.read_parquet(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/generated/events/metabook.parquet/year=*/month=*/day=*/*.parquet"
    )
    current_data = context.current_data()
    if current_data is not None:
        current_data = current_data.to_polars()
        max_ts = current_data["timestamp"].max()
        log(f"Reading data after {max_ts}")
        df = df.filter(df["timestamp"] > max_ts)
    else:
        log("No current data found, reading all data")

    log(f"Returning {df.height} rows")
    return df.to_arrow()


"""
import gcsfs
import polars as pl
import pyarrow as pa

from ascend.resources import CustomPythonPartitionedReader
from ascend.common.events import log
from ascend.common.filters import ListItem
from ascend.application.context import ComponentExecutionContext

reader = CustomPythonPartitionedReader(name="read_metabook")


@reader.list()
def list_partitions(context: ComponentExecutionContext):
    fs = gcsfs.GCSFileSystem()
    files = fs.glob(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/generated/events/metabook.parquet/year=*/month=*/day=*/*.parquet"
    )
    files = [ListItem(name=file) for file in files]
    log(f"Found {len(files)} partitions")
    yield from files


@reader.read()
def read_partition(context: ComponentExecutionContext, item: ListItem) -> pa.Table:
    log(f"Reading partition {item.name}")
    df = pl.read_parquet(f"gs://{item.name}")
    return df.to_arrow()
"""
