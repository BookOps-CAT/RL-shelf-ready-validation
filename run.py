from rl_sr_validation.models import Record, Item, Order, Invoice, BibData
from pydantic import ValidationError

item = Item(
    call_tag="8528",
    call_no="ReCAP 23-99999",
    barcode="12345678901234",
    price="12.34",
    initials="EV",
    location="rcmb2",
    item_type="2",
    agency="43",
)
order = Order(location="MAB", price="1234", fund="123456apprv")
bib = BibData(call_no="ReCAP 23-99999", vendor="EV", rl_identifier="RL", lcc="Z123")
invoice = Invoice(date="240101", price="1234")

r_valid = Record(item_data=item, order_data=order, bib_data=bib, invoice_data=invoice)

print(r_valid)
