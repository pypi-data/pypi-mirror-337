import pandas as pd

from ascend.resources import read
from ascend.application.context import ComponentExecutionContext


@read()
def read_guides(context: ComponentExecutionContext) -> pd.DataFrame:
    df = pd.read_csv(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/seed/guides.csv"
    )
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    return df
