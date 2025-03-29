import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("stores"),
        ref("warehouses"),
    ]
)
def staff(
    stores: ibis.Table,
    warehouses: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    staff = (
        stores.select(CONTACT="OWNER")
        .union(warehouses.select(CONTACT="OWNER"))
        .distinct(on="CONTACT")
    )

    return staff
