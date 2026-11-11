from deltalake import DeltaTable

def load_labels_from_delta():
    # Open the default-history Delta table

    delta_table = DeltaTable("data/delta/labels")

    # Read the Delta table into an Arrow table
    label_table = delta_table.to_pyarrow_table()

    # Convert it into normal Python records
    labels = label_table.to_pylist()

    return labels
