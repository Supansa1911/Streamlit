import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime
import plotly.express as px

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#data
st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] 

st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)

st.subheader('Map of time filter')
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


#1. PyDeck, convert from 2D to 3D map
# สร้างข้อมูลสุ่ม
chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [40.75, -73.98],
    columns=["lat", "lon"],
)


# 3D Map ด้วย HexagonLayer
st.subheader('3D Map with HexagonLayer')
st.pydeck_chart(
    pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=40.75,
            longitude=-73.98,
            zoom=11,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=chart_data,
                get_position="[lon, lat]",
                radius=300,
                elevation_scale=10,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )
        ],
    )
)


st.subheader('3D Map with ScatterplotLayer')
st.pydeck_chart(
    pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=40.75,
            longitude=-73.98,
            zoom=11,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_color="[255, 0, 0, 160]",
                get_radius=200,
                pickable=True,
            )
        ],
    )
)


st.subheader('3D Map with ColumnLayer')
st.pydeck_chart(
    pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=40.75,
            longitude=-73.98,
            zoom=11,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_elevation="100",  # หรือจะกำหนดตามค่าอื่นใน DataFrame ก็ได้
                elevation_scale=5,
                radius=100,
                extruded=True,
                get_fill_color="[255, 165, 0, 200]",
            )
        ],
    )
)




df = pd.DataFrame({
    "Date/Time": pd.date_range(start="2023-01-01", periods=10, freq='D')
})
#2. dete input
d = st.date_input("Date input", datetime.date(2019, 7, 6))
st.write("Date is:", d)




#3. selectbox
option = st.selectbox(
    "Date time selested",
    df["Date/Time"].dt.strftime("%Y-%m-%d %H:%M:%S"),
    index=None,
    placeholder="Select date/time...",
)

st.write("You selected:", option)




#4. plotly
data["date/time"] == "Date/Time"
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Mock data (ตัวอย่างตามที่บอกว่าชื่อ column ตัวเล็ก)
data = pd.DataFrame({
    "date/time": pd.date_range("2023-01-01", periods=100, freq="H"),
    "lat": np.random.uniform(13.70, 13.90, size=100),
    "lon": np.random.uniform(100.40, 100.60, size=100)
})

DATE_COLUMN = "date/time"  # ชื่อคอลัมน์ตัวเล็ก

st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')
hist_values = data[DATE_COLUMN].dt.hour.value_counts().sort_index()

fig_bar = px.bar(
    x=hist_values.index,
    y=hist_values.values,
    labels={"x": "Hour", "y": "Number of pickups"},
    title="Pickups by Hour",
)
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader('Map of all pickups')

if "lat" in data.columns and "lon" in data.columns:
    fig_map = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lon",
        hover_name=DATE_COLUMN,
        hover_data={DATE_COLUMN: True},
        zoom=10,
        height=500
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.error("Data is missing 'lat' and 'lon' columns.")





#5. Click a button to increase the number x in the folling message, "This page has run X times."
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")
