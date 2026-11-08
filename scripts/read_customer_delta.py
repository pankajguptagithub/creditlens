from deltalake import DeltaTable


def read_customer_delta():
    # Open the customer Delta Table
    delta_table = DeltaTable("data/delta/customers")

    # Read the Delta table as an Arrow table
    customer_table = delta_table.to_pyarrow_table()

    # Convert the Arrow table to Python records
    customers = customer_table.to_pylist()

    return customers

customers = read_customer_delta()

print(customers)
