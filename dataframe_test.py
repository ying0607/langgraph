import pandas as pd
import numpy as np

# Read the CSV file
file_path = 'LangGraph/Data/Halen.Yu/Shipment_印能科技_1249774.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# Generate the unit_price column
df['unit_price'] = np.where(df['qty'] != 0, df['us_amt'] / df['qty'], np.nan)

# Filter the DataFrame for the specific customer and order number
filtered_df = df[(df['customername'] == '印能科技股份有限公司') & (df['po_no'] == '1249774')]

# Display the filtered DataFrame to verify its contents
print(filtered_df)

# Check if the filtered DataFrame is empty
if filtered_df.empty:
    print("No matching records found for the specified customer and order number.")
else:
    # Find the product with the highest unit price
    max_unit_price_product = filtered_df.loc[filtered_df['unit_price'].idxmax()]

    # Select relevant columns and rename them
    result_df = max_unit_price_product[['ymd', 'customername', 'po_no', 'part', 'us_amt', 'qty', 'unit_price']]
    result_df = result_df.rename(columns={
        'ymd': 'Date',
        'customername': 'Customer Name',
        'po_no': 'PO No',
        'part': 'Part',
        'us_amt': 'US Amount',
        'qty': 'Qty',
        'unit_price': 'Unit Price'
    })

    # Convert the result to a DataFrame
    result_df = pd.DataFrame(result_df).T

    # Save the result to a CSV file
    output_path = 'LangGraph/Data/Halen.Yu/customer_order_output.csv'
    result_df.to_csv(output_path, index=False)