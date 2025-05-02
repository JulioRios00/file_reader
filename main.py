import file_readers

billing_inflair_path = "s3://mtw-elementar-dev-018061303185/public/airline_files/Airline Price Report/TRANSPORTADORA ORLANDO LTDA - 01698119000142-Inflair_-_January_1st_2024_effective_date_up_until_February_2025.xlsx"
billing_promeus_path = "examples/Billing - Promeus - VS Invoice Report January 2025.xlsx"

pricing_inflair_path = "examples/Pricing - Inflair - January 1st 2024 effective date up until February 2025.xlsx"
pricing_promeus_path = "examples/Pricing - Promeus - Price History Report January 2025.xlsx"


# billing_promeus = file_readers.billing_promeus_invoice_report(
#     billing_promeus_path
#     )

billing_inflair = file_readers.billing_inflair_recon_report(
    billing_inflair_path
)

pricing_promeus = (
    file_readers.pricing_read_promeus_with_flight_classes(pricing_promeus_path)
)

pricing_inflair = file_readers.pricing_read_inflair(pricing_inflair_path)

# print(pricing_inflair)
# print(pricing_promeus)
print(billing_inflair)
