import streamlit as st
import pandas as pd
import plotly.express as px
import os



# Load pre-segmented data
df= pd.read_csv('bank.csv')
# Sidebar Navigation
page = st.sidebar.radio("📂 Navigation", ["🏠 Home", "📊 Customer Segments", "📈 Customer Clusters", "👤 Customer Profile"])

total_customers = df['CustomerID'].nunique()
avg_trxn = df['Monetary'].mean()
avg_balance = df['CustAccountBalance'].mean()
avg_age = df['CustomerAge'].mean()
segments = sorted(df['Segment'].unique())

cluster_name = {
    0: "Potential",
    1: "At risk",
    2: "High Value",
    3: "Loyal"
}
# --- Home Page ---
if page == "🏠 Home":
    st.title("🏠 Welcome to the Customer Insights Dashboard ")
    st.markdown("""
        This dashboard provides insights into customer behaviour using:
        - **RFM Segmentation**: Categorises customers based on Recency, Frequency, and Monetary value.
        - **Clustering Analysis**: Uses machine learning to discover behavioural patterns in customers.

        Use the sidebar to navigate between analysis views.
    """)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", total_customers)
    col2.metric("Average Transaction Amount", f"₹{avg_trxn:,.0f}")
    col3.metric("Average Account Balance", f"₹{avg_balance:,.0f}")
    col4.metric("Average Age", f"{avg_age:.1f} yrs")

       #Gender
    gender_fig = px.pie(df, names='CustGender', title="Gender Distribution",
        color_discrete_sequence=['purple', 'indianred'])
    st.plotly_chart(gender_fig, use_container_width=True)
    
        # Age Distribution Chart using seaborn
    age_fig = px.histogram(
    df, 
    x='CustomerAge', 
    nbins=20, 
    title='Customer Age Distribution',
    color_discrete_sequence=['indianred']
    )
    st.plotly_chart(age_fig, use_container_width=True)
    oc_df = (
        df['CustLocation']
        .value_counts()
        .nlargest(10)
        .reset_index()
        )
    oc_df.columns=['CustLocation', 'Custcount']
    
    oc_fig = px.bar(
    oc_df,
     x='CustLocation',
     y='Custcount',
    color='CustLocation',
    color_continuous_scale='plasma',
        labels={'CustLocation': 'Location', 'Custcount': 'Customer Count'},
        title="Top 10 Customer Locations"
    )

    st.plotly_chart(oc_fig, use_container_width=True)
    
     

    # --- Segments Page ---
elif page == "📊 Customer Segments":
    st.title("📊 Customer Segmentation Analysis")
    st.markdown('''
                 
                - **High Value** : High spending and frequent transactions
                - **Loyal** : Customers who have been active for a while with good engagement
                - **Potential** : Very recent activity but few transactions
                - **At Risk** :  declining activity or low recency
                ''')
    
    selected_segment = st.sidebar.selectbox("Select Customer Segment", segments)

    # Filter the DataFrame based on the selected segment
    segment_data = df[df['Segment'] == selected_segment]
    Total_seg_cust = segment_data['CustomerID'].nunique()
    seg_avg_trxn = segment_data['Monetary'].mean()
    seg_avg_balance = segment_data['CustAccountBalance'].mean()
    seg_avg_age = segment_data['CustomerAge'].mean()

    st.subheader(f"Segment: {selected_segment}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", Total_seg_cust)
    col2.metric("Average Transaction Amount", f"₹{seg_avg_trxn:,.0f}")
    col3.metric("Average Account Balance", f"₹{seg_avg_balance:,.0f}")
    col4.metric("Average Age", f"{seg_avg_age:.1f} yrs")
    
    # Columns for gender and age charts
    col1, col2 = st.columns(2)

    # Gender distribution
    with col1:
        gender_fig = px.pie(segment_data, names='CustGender', title="Gender Distribution",
                        color_discrete_sequence=['purple', 'indianred'])
        st.plotly_chart(gender_fig, use_container_width=True)

    # Age distribution
    with col2:
        age_fig = px.histogram(segment_data, 
                           x='CustomerAge', 
                           nbins=15, 
                           title="Age Distribution",
                           color_discrete_sequence=['indianred'])
        st.plotly_chart(age_fig, use_container_width=True)


        # Top 10 customer locations
    loc_df = (
        segment_data['CustLocation']
        .value_counts()
        .nlargest(10)
        .reset_index()
        )
    loc_df.columns=['CustLocation', 'Custcount']
    
        # 
    oc_fig = px.bar(
        loc_df,
        x='CustLocation',
        y='Custcount',
        color='CustLocation',
        color_continuous_scale='plasma',
        labels={'CustLocation': 'Location', 'Custcount': 'Customer Count'},
        title="Top 10 Customer Locations"
        )

    st.plotly_chart(oc_fig, use_container_width=True)
    
   
    # Monetary summary
    st.markdown("#### Summary Statistics")
    st.dataframe(segment_data[['Recency', 'Frequency', 'Monetary', 'CustAccountBalance']].describe())

    
      #Top 10 Customers
    with st.expander("🔍 View Top 10 Customers in this Segment", expanded=False):  
        top_customers = (
            segment_data[segment_data['Segment'] == selected_segment]
            .sort_values(by='Monetary', ascending=False)
            .head(10)
            )

        st.write(f"Top 10 Customers in '{selected_segment}' Segment")
        st.dataframe(top_customers[['CustomerID', 'Monetary', 'Frequency', 'Recency', 'CustomerAge']].reset_index(drop=True))

       # Dictionary of strategies
    segment_strategies = {
        "High Value": [
            "💎 Offer personalised premium services or rewards",
            "🚀 Provide early access to new products or services",
            "🤝 Encourage referrals with loyalty incentives",
            "💼 Cross-sell high-end or complementary financial products",
            "📢 Regularly engage with updates and exclusive content"
        ],
        "Loyal": [
            "🏅 Reward loyalty with tailored offers",
            "🎁 Send appreciation messages or gifts",
            "✨ Offer upgrades or benefits for continued usage",
            "🗣 Request feedback to maintain engagement",
            "👥 Encourage community involvement or referrals"
        ],
        "Potential": [
            "📧 Nurture with welcome emails or onboarding support",
            "📊 Promote benefits of frequent usage",
            "⏰ Send timely reminders or educational content",
            "🎉 Offer first-time incentives",
            "🔍 Track activity to personalise future engagement"
        ],
        "At Risk": [
            "🎯 Send re-engagement offers or discounts",
            "📋 Check in with satisfaction surveys",
            "🔔 Remind of unused features or benefits",
            "🌟 Highlight success stories or positive testimonials",
            "🧭 Simplify the user journey to reduce friction"
        ]
        }

        # Get selected segment strategy
    strategy_list = segment_strategies.get(selected_segment, [])

    # Display in stylised format
    st.markdown(f"### 💡 Strategies for '{selected_segment}' Customers")

    if strategy_list:
        for strategy in strategy_list:
            st.write(f"✅ {strategy}")
    else:
        st.info("No strategy defined for this segment yet.")
        


    # --- Clusters Page ---
elif page == "📈 Customer Clusters":
    st.title("📈 Customer Clustering Analysis")
    clusters = sorted(df['Cluster'].unique())
    selected_cluster = st.sidebar.selectbox("Select Cluster", clusters)
    #Filter for Cluster Data
    cluster_data =df[df['Cluster'] == selected_cluster]
    #st.subheader(f"Cluster: {selected_cluster}")
    # Display header with cluster name
    st.subheader(f"Cluster {selected_cluster}: {cluster_name.get(selected_cluster, 'Unknown')} Customers")

    Total_clu_cust = cluster_data['CustomerID'].nunique()
    clu_avg_trxn = cluster_data['Monetary'].mean()
    clu_avg_balance = cluster_data['CustAccountBalance'].mean()
    clu_avg_age = cluster_data['CustomerAge'].mean()


    #st.subheader(f"Cluster: {selected_cluster}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", Total_clu_cust)
    col2.metric("Average Transaction Amount", f"₹{clu_avg_trxn:,.0f}")
    col3.metric("Average Account Balance", f"₹{clu_avg_balance:,.0f}")
    col4.metric("Average Age", f"{clu_avg_age:.1f} yrs")
    

    # Columns for gender and age charts
    col1, col2 = st.columns(2)

    # Gender distribution
    with col1:
        gender_fig = px.pie(cluster_data, names='CustGender', title="Gender Distribution")
        st.plotly_chart(gender_fig, use_container_width=True)

    # Age distribution
    with col2:
        age_fig = px.histogram(cluster_data, 
                            x='CustomerAge', 
                            nbins=15, 
                            title="Age Distribution",
                            color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(age_fig, use_container_width=True)

        
    # Top 10 customer locations
    loc_df = (
        cluster_data['CustLocation']
        .value_counts()
        .nlargest(10)
        .reset_index())

    loc_df.columns = ['CustLocation', 'CustCount']
    
    loc_fig = px.bar(
        loc_df,
        x='CustLocation',
        y='CustCount',
        color='CustLocation',
        color_continuous_scale='plasma',
        labels={'CustLocation': 'Location', 'CustCount': 'Customer Count'},
        title="Top 10 Customer Locations"
        )

    st.plotly_chart(loc_fig, use_container_width=True)

    # Monetary summary
    st.markdown("#### Summary Statistics")
    st.dataframe(cluster_data[['Recency', 'Frequency', 'Monetary', 'CustAccountBalance']].describe())
        #   Top 10 Customers
    with st.expander("🔍 View Top 10 Customers in this Segment", expanded=False):  
        top_customers = (
            cluster_data[cluster_data['Cluster'] == selected_cluster]
            .sort_values(by='Monetary', ascending=False)
            .head(10)
            )

        st.write(f"Top 10 Customers in '{selected_cluster}' Segment")
        st.dataframe(top_customers[['CustomerID', 'Monetary', 'Frequency', 'Recency', 'CustomerAge']].reset_index(drop=True))

elif page == "👤 Customer Profile":
    st.title("📊 Customer Profile Lookup")   
    customer_id_input = st.text_input("Enter Customer ID")
    st.write("For example C1010011")
    if customer_id_input:
        if customer_id_input in df["CustomerID"].astype(str).values:
            cust_profile = df[df["CustomerID"].astype(str) == customer_id_input].squeeze()
            st.subheader(f"Customer Profile: {cust_profile['CustomerID']}")
                        # Format Monetary with commas for readability
                #monetary_value = f"{cust_profile['Monetary']:,.0f}" if pd.notnull(cust_profile['Monetary']) else "N/A"

                # Format values into a table
            profile_data = {
                "Metric": ["Recency (days)", "Frequency", "Monetary (INR)", "Location", "Gender", "Age", "Account Balance", "Segment"],
                "Value": [
                        cust_profile.get("Recency", "N/A"),
                        cust_profile.get("Frequency", "N/A"),
                        cust_profile.get("Monetary","N/A"),
                        cust_profile.get("CustLocation", "N/A"),
                        cust_profile.get("CustGender", "N/A"),
                        cust_profile.get("CustomerAge", "N/A"), 
                        cust_profile.get("CustAccountBalance", "N/A"),
                        cust_profile.get("Segment", "N/A") 
                        ]
            }
            profile_df = pd.DataFrame(profile_data)

            st.table(profile_df)
            
        else:
            st.warning("Customer ID not found.")