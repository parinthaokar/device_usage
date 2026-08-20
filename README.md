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

<img width="1917" height="621" alt="Screenshot 2026-08-20 at 12 28 02 AM" src="https://github.com/user-attachments/assets/ceb8b93b-28ae-4850-817f-8622fda1da2b" />

<img width="1573" height="668" alt="Screenshot 2026-08-20 at 12 28 25 AM" src="https://github.com/user-attachments/assets/2117b374-1e3e-4eb1-83c5-75560b2ece34" />

<img width="1582" height="890" alt="Screenshot 2026-08-20 at 12 28 41 AM" src="https://github.com/user-attachments/assets/b048477d-1875-4d25-9a20-58bd5976a2c9" />

<img width="1589" height="888" alt="Screenshot 2026-08-20 at 12 29 02 AM" src="https://github.com/user-attachments/assets/201aaed2-0df6-471e-98d5-aeb94c8347f6" />





