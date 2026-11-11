import json

import pyarrow as pa
from deltalake import write_deltalake

def load_labels():
    # Load out synthetic default-history labels
    with open("data/labels.json", "r") as file:
        labels = json.load(file)

    return labels

def create_label_delta():
    labels = load_labels()

    label_table = pa.Table.from_pylist(labels)

    write_deltalake(
        "data/delta/labels",
        label_table,
        mode = "overwrite"
    )

create_label_delta()
