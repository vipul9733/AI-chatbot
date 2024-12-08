import pandas as pd
import sqlite3
import json
from datetime import datetime

def export_data_for_powerbi():
    # Connect to database
    conn = sqlite3.connect('restaurant.db')
    
    # Export orders
    orders_df = pd.read_sql_query("""
        SELECT 
            id,
            customer_name,
            items,
            total_amount,
            order_status,
            order_date
        FROM orders
    """, conn)
    
    # Process items column to extract individual items
    def expand_items(row):
        items = json.loads(row['items'])
        return pd.DataFrame(items)
    
    # Create detailed items dataframe
    items_df = orders_df.apply(expand_items, axis=1)
    items_df['order_id'] = orders_df['id'].repeat(items_df.shape[0])

    # Export to CSV
    current_date = datetime.now().strftime('%Y%m%d')
    orders_df.to_csv(f'data/orders_{current_date}.csv', index=False)
    items_df.to_csv(f'data/order_items_{current_date}.csv', index=False)
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    export_data_for_powerbi()