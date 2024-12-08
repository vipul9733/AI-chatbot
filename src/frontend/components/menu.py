import streamlit as st
import pandas as pd

class MenuDisplay:
    def __init__(self, database):
        self.db = database

    def show(self):
        st.subheader("Our Menu")
        
        # Get menu items from database
        menu_items = self.db.get_menu()
        
        # Convert to DataFrame for better display
        df = pd.DataFrame(menu_items)
        
        # Group by category
        categories = df['category'].unique()
        
        for category in categories:
            st.write(f"### {category}")
            category_items = df[df['category'] == category]
            
            for _, item in category_items.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{item['item_name']}**")
                    st.write(item['description'])
                with col2:
                    st.write(f"${item['price']:.2f}")
                st.divider()