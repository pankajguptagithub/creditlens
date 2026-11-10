import pyarrow as pa

from deltalake import write_deltalake

from app.data.payment_repository import load_payments

def create_payment_delta():
    # Load the payment data we already understand
    payments = load_payments()

    # Convert the payment records to an Arrow table
    payment_table = pa.Table.from_pylist(payments)

    # Write the records as a Delta table
    write_deltalake(
        "data/delta/payments",
        payment_table,
        mode="overwrite",
    )

create_payment_delta()
