# NBA Scores Dashboard

A real-time NBA scores dashboard built with Streamlit that displays live game scores, standings, and historical data.

## Features

- **Live Scores**: Real-time game scores updated every minute during games
- **Historical Data**: Browse past game results up to 7 days back
- **Team Filtering**: Filter games by specific teams
- **Dark Mode UI**: Modern dark theme with responsive scorecard design
- **Team Logos**: Official team logos via ESPN CDN
- **Central Time Display**: Game times converted to Central Time

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nickgcamp/first-stream-list-project.git
cd first-stream-list-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- nba_api >= 1.4.1
- pytz >= 2023.3

## Project Structure

```
├── app.py              # Main Streamlit application
├── data_manager.py     # NBA API data fetching and caching
├── style_utils.py      # CSS styles and HTML rendering
├── constants.py        # Team data and logo mappings
└── requirements.txt    # Python dependencies
```

## Data Source

This app uses the unofficial [nba_api](https://github.com/swar/nba_api) Python package to fetch real-time and historical NBA game data. No API key required.

## License

MIT
