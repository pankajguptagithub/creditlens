import pyarrow as pa

from deltalake import write_deltalake

from app.data.customer_repository import load_customers

def create_customer_delta():
    # Load the customer data we already understand

    customers = load_customers()

    # Convert the customer records to an Arrow table
    customer_table = pa.Table.from_pylist(customers)

    # Write the records as a Delta table 
    write_deltalake(
        "data/delta/customers",
        customer_table,
        mode="overwrite"
    )

create_customer_delta()
