import file_readers

billing_inflair_path = "examples/Billing - Inflair - VS Flight & Airline Billing Report_List of Flight Invoices_JAN 2025.xlsx"
billing_promeus_path = "examples/Billing - Promeus - VS Invoice Report January 2025.xlsx"

pricing_inflair_path = "examples/Pricing - Inflair - January 1st 2024 effective date up until February 2025.xlsx"
pricing_promeus_path = "examples/Pricing - Promeus - Price History Report January 2025.xlsx"

file_readers.read_clean_invoice_report(billing_promeus_path)
file_readers.read_flight_invoice_report(billing_inflair_path)

promeus_pricing = (
    file_readers.read_pricing_promeus_with_flight_classes(pricing_promeus_path)
)

inflair_data = file_readers.read_pricing_inflair(pricing_inflair_path)

# print(inflair_data)
print(promeus_pricing)