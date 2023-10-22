import streamlit as st
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
import data as dataimport
# Set page title and theme

st.set_page_config(page_title="Medication Consumption App",
                  page_icon="💊",
                  layout="centered",
                  initial_sidebar_state="auto",)

st.header("💊Medication Consumption Analysis ")
st.title("What is the profil type of the french medication consumers ?")
st.write("Welcome to our Medication Consumption Analysis data visualization website. This platform allows you to explore and visually analyze data related to medication consumption in France. The dataset provides insights into various aspects, including medication categories, age groups, and refund amounts.")
st.write("Our interactive visualizations make it easy to uncover trends, discover patterns, and gain insights from the data. You can explore different facets of medication consumption, helping you make informed decisions and better understand the underlying data.")
st.write("Start exploring the data, visualize key insights, and enhance your understanding of medication consumption patterns through our user-friendly interface.")

# Create a menu with links to different sections
st.sidebar.title('Website Analysis Menu')
st.sidebar.write('Let me present myself : my name is Adrien Girard, I am currently studying at Efrei Paris in the 2025 promotion. I am majoring in Analytics and Business Intelligence. ')
st.sidebar.markdown("""
- [Gender distribution of the french medication consumers](#gender-distribution)
- [Age distribution of the analysed population](#age-distribution)
- [Medication consumption by age category](#medication-consumption-by-age)
- [Medication consumption by department](#medication-by-department)
- [Number of boxes prescribed by category of prescribers](#number-of-boxes)
- [Refund amount by age category](#refund-amount-by-age)
""")
st.sidebar.header("#dataviz2023efrei")

@st.cache_data
def load_data():
    url = "https://open-data-assurance-maladie.ameli.fr/medicaments/download.php?Dir_Rep=Open_MEDIC_Base_Complete&Annee=2022"
    return pd.read_csv(url, encoding='ISO-8859-1')

medic = load_data()
france_map = 'https://france-geojson.gregoiredavid.fr/repo/regions.geojson'


###                pie chart of gender distribution              ###
st.markdown('<a id="gender-distribution"></a>', unsafe_allow_html=True)
gender_labels = {1: "Male", 2: "Female", 9: "Unknown"}
medic['gender_label'] = medic['sexe'].map(gender_labels)
st.subheader("Gender Distribution")
st.write("This graph is a pie chart, it displays the distribution of consumption on the gender criteria. Thanks to this pie chart, we can see that women tend to consume more medication in France.")

gender_pie_chart = px.pie(medic, names="gender_label", )
st.plotly_chart(gender_pie_chart)


###                 bar chart ff age distribution               ###
st.markdown('<a id="age-distribution"></a>', unsafe_allow_html=True)
st.subheader("Medication Consumption by Age Category")
st.write("This is a bar chart, and visualises the population's age of our dataset. We can see that the majority of the population is over 60 years old.")
age_bins = [0, 19, 59, float("inf")]
age_labels = ["0-19", "20-59", "60 and above"]
medic['age_category'] = pd.cut(medic['age'], bins=age_bins, labels=age_labels, right=False)
age_histogram = px.histogram(medic, x="age_category")
age_histogram.update_traces(marker_color="green")
age_histogram.update_xaxes(categoryorder="array", categoryarray=age_labels)
st.plotly_chart(age_histogram)


###                medication consumption by age               ###
st.markdown('<a id="medication-consumption-by-age"></a>', unsafe_allow_html=True)
st.subheader("Medication Consumption by Age Category")
st.write("This is an interactive chart. you can select the desired age category, and look at the distribution of medication consumed for each category.")
selected_age = st.selectbox("Select Age Category", age_labels)
selected_categories = ['A', 'B', 'C', 'D', 'G']
medic['Age Category'] = pd.cut(medic['age'], bins=age_bins, labels=age_labels, right=False)
filtered_data = medic[medic['Age Category'] == selected_age]
medication_counts = filtered_data.groupby('ATC1').size().reset_index(name='Count')
fig = px.bar(medication_counts, x='ATC1', y='Count', title=f"Medication Counts for {selected_age} Age Category", labels={'Count': 'Count'}, category_orders={"ATC1": selected_categories})

fig.update_xaxes(categoryorder="array", categoryarray=selected_categories)
fig.update_layout(xaxis=dict(showgrid=False, showline=False))

st.plotly_chart(fig)
st.write("Bar plot description:")
df = pd.DataFrame(list(dataimport.category_mappings.items()), columns=['Category', 'Description'])
st.table(df)


###                medication consumption by department               ###
st.markdown('<a id="medication-by-department"></a>', unsafe_allow_html=True)
st.subheader("Medication Consumption by Department")
st.write("This is an interactive chart visualising the different french regions. This map shows the distribution of medication consumption in France.")
# Group the data by department and count the number of medications
medication_counts_by_department = medic.groupby('BEN_REG').size().reset_index(name='Medication Count')
# Merge the counts with department names
medication_counts_by_department['Department Name'] = medication_counts_by_department['BEN_REG'].map(
    dataimport.department_names)
# Streamlit app

fig = px.choropleth(medication_counts_by_department, geojson=france_map, locations='BEN_REG',
                    featureidkey="properties.code", color='Medication Count', hover_name='Department Name')

fig.update_geos(
    center={"lat": 48.8566, "lon": 2.3522},
    scope="europe",
)
st.plotly_chart(fig)

###         number of boxes by PSP_SPE          ###
st.markdown('<a id="number-of-boxes"></a>', unsafe_allow_html=True)
# Create a scatter plot
st.subheader("Scatter Plot: Number of Boxes by PSP_SPE")
st.write("This graph is a scatter plot. It visualizes the number of boxes sold by prescribers.")
fig = px.scatter(medic, x='PSP_SPE', y='BOITES')
fig.update_xaxes(type='category', categoryorder='total ascending')
st.plotly_chart(fig)
st.write("Here we have a table of the top 10 category of prescribers:")
selected_lines = [1, 90, 19, 7, 3, 12, 8, 5, 98, 15]
selected_data = [(key, dataimport.psp_spe_labels[key]) for key in selected_lines]
st.table(selected_data)

###         Refund amount by age category           ###
st.markdown('<a id="refund-amount-by-age"></a>', unsafe_allow_html=True)
# Categorize ages in the DataFrame
st.subheader("Refund Amount by Age Category")
st.write("This graph is a bar chart. It visualizes the average refund amount by age category.")
medic['Age Category'] = pd.cut(medic['age'], bins=age_bins, labels=age_labels, right=False)
# Convert 'REM' column to numeric
medic['REM'] = pd.to_numeric(medic['REM'].str.replace(',', '.'), errors='coerce')
# Group data by age category and calculate the mean refund amount in each category
age_refund_mean = medic.groupby('Age Category')['REM'].mean().reset_index()
# Create a bar chart to visualize refund amounts by age category
fig = px.bar(age_refund_mean, x='Age Category', y='REM', labels={'Age Category': 'Age Category', 'REM': 'Average Refund Amount (Euros)'})
st.plotly_chart(fig)
