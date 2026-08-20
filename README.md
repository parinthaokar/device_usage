# Device Usage EDA

A Streamlit app for exploring the [Mobile Device Usage and User Behavior](https://www.kaggle.com/datasets/valakhorasani/mobile-device-usage-and-user-behavior-dataset) dataset — 700 users across Android/iOS devices, with screen time, app usage, battery drain, data usage, and a derived behavior class.

## Features

- Sidebar filters for OS, device model, and age range
- Summary metrics and raw data / summary statistics viewer
- Distribution plots (histogram + box plot) per metric, split by OS
- Scatterplot with selectable X/Y axes, colored by device model
- Correlation heatmap across numeric features
- Categorical breakdowns: device model counts, behavior class by gender, OS/gender sunburst

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync
uv run streamlit run app.py
```

The app extracts `user_behavior_dataset.csv` from `archive.zip` into `data/` on first run.

## Screenshots

<!-- Paste app screenshots below -->



