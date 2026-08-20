import zipfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA_DIR = Path("data")
ARCHIVE_PATH = Path("archive.zip")
CSV_NAME = "user_behavior_dataset.csv"

CHART_SURFACE = "#fcfcfb"
CATEGORICAL_COLORS = px.colors.qualitative.Set2

st.set_page_config(page_title="Device Usage EDA", page_icon="📱", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    csv_path = DATA_DIR / CSV_NAME
    if not csv_path.exists():
        DATA_DIR.mkdir(exist_ok=True)
        with zipfile.ZipFile(ARCHIVE_PATH) as zf:
            zf.extract(CSV_NAME, DATA_DIR)
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    return df


def style_fig(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        plot_bgcolor=CHART_SURFACE,
        paper_bgcolor=CHART_SURFACE,
        font_color="#0b0b0b",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


df = load_data()

st.title("📱 Device Usage & Behavior EDA")
st.caption(
    "Exploratory analysis of the Mobile Device Usage and User Behavior dataset "
    f"({len(df):,} users)."
)

# --- Sidebar filters -------------------------------------------------------
st.sidebar.header("Filters")
os_options = sorted(df["Operating System"].unique())
selected_os = st.sidebar.multiselect("Operating System", os_options, default=os_options)

device_options = sorted(df["Device Model"].unique())
selected_devices = st.sidebar.multiselect("Device Model", device_options, default=device_options)

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
selected_age = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

filtered = df[
    df["Operating System"].isin(selected_os)
    & df["Device Model"].isin(selected_devices)
    & df["Age"].between(*selected_age)
]

if filtered.empty:
    st.warning("No rows match the current filters.")
    st.stop()

# --- Summary metrics ---------------------------------------------------
st.subheader("Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Users", f"{len(filtered):,}")
c2.metric("Avg screen time (hrs/day)", f"{filtered['Screen On Time (hours/day)'].mean():.1f}")
c3.metric("Avg app usage (min/day)", f"{filtered['App Usage Time (min/day)'].mean():.0f}")
c4.metric("Avg data usage (MB/day)", f"{filtered['Data Usage (MB/day)'].mean():.0f}")

# --- Raw data + describe ---------------------------------------------------
with st.expander("Raw data"):
    st.dataframe(filtered, use_container_width=True)

with st.expander("Summary statistics"):
    st.dataframe(filtered.describe().T, use_container_width=True)
    st.write("Missing values per column:")
    st.dataframe(filtered.isnull().sum().rename("missing").to_frame(), use_container_width=True)

st.divider()

# --- Distributions -----------------------------------------------------
st.subheader("Distributions")
numeric_cols = [
    "App Usage Time (min/day)",
    "Screen On Time (hours/day)",
    "Battery Drain (mAh/day)",
    "Number of Apps Installed",
    "Data Usage (MB/day)",
    "Age",
]
dist_col = st.selectbox("Choose a metric", numeric_cols)

hist_col, box_col = st.columns(2)
with hist_col:
    fig_hist = px.histogram(
        filtered, x=dist_col, color="Operating System", nbins=30,
        color_discrete_sequence=CATEGORICAL_COLORS, barmode="overlay", opacity=0.75,
        title=f"Distribution of {dist_col}",
    )
    st.plotly_chart(style_fig(fig_hist), use_container_width=True)

with box_col:
    fig_box = px.box(
        filtered, x="Operating System", y=dist_col, color="Operating System",
        color_discrete_sequence=CATEGORICAL_COLORS,
        title=f"{dist_col} by OS",
    )
    st.plotly_chart(style_fig(fig_box), use_container_width=True)

st.divider()

# --- Relationships -------------------------------------------------------
st.subheader("Relationships")
rel_col1, rel_col2 = st.columns(2)
with rel_col1:
    x_axis = st.selectbox("X axis", numeric_cols, index=0, key="x_axis")
with rel_col2:
    y_axis = st.selectbox("Y axis", numeric_cols, index=1, key="y_axis")

fig_scatter = px.scatter(
    filtered, x=x_axis, y=y_axis, color="Device Model", size="User Behavior Class",
    hover_data=["Gender", "Age"], color_discrete_sequence=CATEGORICAL_COLORS,
    title=f"{y_axis} vs {x_axis}",
)
st.plotly_chart(style_fig(fig_scatter), use_container_width=True)

fig_corr = px.imshow(
    filtered[numeric_cols + ["User Behavior Class"]].corr().round(2),
    text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
    title="Correlation matrix",
)
st.plotly_chart(style_fig(fig_corr), use_container_width=True)

st.divider()

# --- Categorical breakdowns ------------------------------------------------
st.subheader("Categorical breakdowns")
cat_col1, cat_col2 = st.columns(2)
with cat_col1:
    device_counts = filtered["Device Model"].value_counts().reset_index()
    device_counts.columns = ["Device Model", "Count"]
    fig_devices = px.bar(
        device_counts, x="Device Model", y="Count", color="Device Model",
        color_discrete_sequence=CATEGORICAL_COLORS, title="Users by device model",
    )
    st.plotly_chart(style_fig(fig_devices), use_container_width=True)

with cat_col2:
    behavior_counts = (
        filtered.groupby(["User Behavior Class", "Gender"]).size().reset_index(name="Count")
    )
    fig_behavior = px.bar(
        behavior_counts, x="User Behavior Class", y="Count", color="Gender",
        barmode="group", color_discrete_sequence=CATEGORICAL_COLORS,
        title="User behavior class by gender",
    )
    st.plotly_chart(style_fig(fig_behavior), use_container_width=True)

fig_gender_os = px.sunburst(
    filtered, path=["Operating System", "Gender"], color_discrete_sequence=CATEGORICAL_COLORS,
    title="OS and gender breakdown",
)
st.plotly_chart(style_fig(fig_gender_os), use_container_width=True)
