"""
Data Manager for NBA Scores Dashboard
Handles data fetching from nba_api, caching, and state management
"""

import streamlit as st
from datetime import datetime, timedelta
from constants import NBA_TEAMS

try:
    from nba_api.live.nba.endpoints import scoreboard
    from nba_api.stats.endpoints import leaguegamefinder
    NBA_API_AVAILABLE = True
except ImportError:
    NBA_API_AVAILABLE = False

import pytz


# Mapping from nba_api team tricode to our constants abbreviation
# Most are the same, but some differ
NBA_API_TEAM_MAP = {
    "ATL": "ATL",
    "BOS": "BOS",
    "BKN": "BKN",
    "CHA": "CHA",
    "CHI": "CHI",
    "CLE": "CLE",
    "DAL": "DAL",
    "DEN": "DEN",
    "DET": "DET",
    "GSW": "GSW",
    "HOU": "HOU",
    "IND": "IND",
    "LAC": "LAC",
    "LAL": "LAL",
    "MEM": "MEM",
    "MIA": "MIA",
    "MIL": "MIL",
    "MIN": "MIN",
    "NOP": "NOP",
    "NYK": "NYK",
    "OKC": "OKC",
    "ORL": "ORL",
    "PHI": "PHI",
    "PHX": "PHX",
    "POR": "POR",
    "SAC": "SAC",
    "SAS": "SAS",
    "TOR": "TOR",
    "UTA": "UTA",
    "WAS": "WAS",
}


def get_team_info(tricode):
    """
    Get team info from our constants using nba_api tricode.

    Args:
        tricode: Team abbreviation from nba_api

    Returns:
        Dict with team name and logo, or fallback if not found
    """
    our_abbrev = NBA_API_TEAM_MAP.get(tricode, tricode)
    team_info = NBA_TEAMS.get(our_abbrev)

    if team_info:
        return {
            "abbrev": our_abbrev,
            "name": team_info["name"],
            "logo": team_info["logo"],
        }

    # Fallback for unknown teams
    return {
        "abbrev": tricode,
        "name": tricode,
        "logo": "",
    }


def parse_game_status(game_data):
    """
    Parse the game status from nba_api response.

    Args:
        game_data: Game dict from nba_api

    Returns:
        Human-readable status string
    """
    game_status = game_data.get("gameStatus", 1)
    game_status_text = game_data.get("gameStatusText", "")

    if game_status == 1:
        # Game not started - show scheduled time
        game_time_utc = game_data.get("gameTimeUTC", "")
        if game_time_utc:
            try:
                utc_time = datetime.fromisoformat(game_time_utc.replace("Z", "+00:00"))
                central = pytz.timezone("America/Chicago")
                local_time = utc_time.astimezone(central)
                return local_time.strftime("%I:%M %p CT")
            except (ValueError, AttributeError):
                pass
        return game_status_text if game_status_text else "Scheduled"

    elif game_status == 2:
        # Game in progress
        period = game_data.get("period", 0)
        game_clock = game_data.get("gameClock", "")

        if period and game_clock:
            # Format period (1st, 2nd, 3rd, 4th, OT, etc.)
            if period <= 4:
                period_str = f"Q{period}"
            else:
                ot_num = period - 4
                period_str = f"OT{ot_num}" if ot_num > 1 else "OT"

            # Clean up game clock format (remove PT prefix if present)
            clock = game_clock.replace("PT", "").replace("M", ":").replace("S", "")
            if clock.startswith(":"):
                clock = "0" + clock

            return f"{period_str} {clock}"

        return game_status_text if game_status_text else "In Progress"

    elif game_status == 3:
        # Game finished
        return "Final"

    return game_status_text if game_status_text else "Unknown"


def fetch_live_games():
    """
    Fetch today's live games from nba_api.

    Returns:
        List of game dictionaries in our standard format
    """
    if not NBA_API_AVAILABLE:
        return []

    try:
        # Get today's scoreboard
        board = scoreboard.ScoreBoard()
        games_data = board.get_dict()

        games_list = games_data.get("scoreboard", {}).get("games", [])

        if not games_list:
            return []

        games = []
        today = datetime.now().date()

        for game_data in games_list:
            # Get team info
            home_team_data = game_data.get("homeTeam", {})
            away_team_data = game_data.get("awayTeam", {})

            home_tricode = home_team_data.get("teamTricode", "")
            away_tricode = away_team_data.get("teamTricode", "")

            home_team_info = get_team_info(home_tricode)
            away_team_info = get_team_info(away_tricode)

            # Get scores
            home_score = home_team_data.get("score", 0)
            away_score = away_team_data.get("score", 0)

            # Handle scores for games that haven't started
            if game_data.get("gameStatus", 1) == 1:
                home_score = 0
                away_score = 0

            # Parse game status
            status = parse_game_status(game_data)

            game = {
                "id": game_data.get("gameId", f"{today.isoformat()}-{home_tricode}-{away_tricode}"),
                "date": today,
                "status": status,
                "home_team": {
                    "abbrev": home_team_info["abbrev"],
                    "name": home_team_info["name"],
                    "logo": home_team_info["logo"],
                    "score": home_score,
                },
                "away_team": {
                    "abbrev": away_team_info["abbrev"],
                    "name": away_team_info["name"],
                    "logo": away_team_info["logo"],
                    "score": away_score,
                },
            }
            games.append(game)

        return games

    except Exception as e:
        st.error(f"Error fetching NBA data: {str(e)}")
        return []


def fetch_historical_games(date):
    """
    Fetch games for a specific date using the stats API.

    Args:
        date: datetime.date object

    Returns:
        List of game dictionaries in our standard format
    """
    if not NBA_API_AVAILABLE:
        return []

    try:
        # Format date as required by nba_api
        date_str = date.strftime("%m/%d/%Y")

        # Use leaguegamefinder to get games for the date
        game_finder = leaguegamefinder.LeagueGameFinder(
            date_from_nullable=date_str,
            date_to_nullable=date_str,
            league_id_nullable="00"
        )

        games_df = game_finder.get_data_frames()[0]

        if games_df.empty:
            return []

        # Group games by game_id (each game appears twice - once per team)
        game_ids = games_df["GAME_ID"].unique()
        games = []

        for game_id in game_ids:
            game_rows = games_df[games_df["GAME_ID"] == game_id]

            if len(game_rows) < 2:
                continue

            # Determine home/away by matchup string (@ indicates away team)
            home_row = None
            away_row = None

            for _, row in game_rows.iterrows():
                matchup = row.get("MATCHUP", "")
                if "@" in matchup:
                    away_row = row
                else:
                    home_row = row

            if home_row is None or away_row is None:
                # Fallback: first row is home, second is away
                home_row = game_rows.iloc[0]
                away_row = game_rows.iloc[1]

            home_abbrev = home_row.get("TEAM_ABBREVIATION", "")
            away_abbrev = away_row.get("TEAM_ABBREVIATION", "")

            home_team_info = get_team_info(home_abbrev)
            away_team_info = get_team_info(away_abbrev)

            home_score = int(home_row.get("PTS", 0) or 0)
            away_score = int(away_row.get("PTS", 0) or 0)

            game = {
                "id": game_id,
                "date": date,
                "status": "Final",
                "home_team": {
                    "abbrev": home_team_info["abbrev"],
                    "name": home_team_info["name"],
                    "logo": home_team_info["logo"],
                    "score": home_score,
                },
                "away_team": {
                    "abbrev": away_team_info["abbrev"],
                    "name": away_team_info["name"],
                    "logo": away_team_info["logo"],
                    "score": away_score,
                },
            }
            games.append(game)

        return games

    except Exception as e:
        st.error(f"Error fetching historical NBA data: {str(e)}")
        return []


@st.cache_data(ttl=60)  # Cache for 1 minute for live scores
def fetch_games_for_date(date):
    """
    Fetches games for a specific date.
    Uses live API for today, historical API for past dates.

    Args:
        date: datetime.date object

    Returns:
        List of game dictionaries
    """
    today = datetime.now().date()

    if date == today:
        # Use live scoreboard for today's games
        return fetch_live_games()
    elif date < today:
        # Use historical data for past games
        return fetch_historical_games(date)
    else:
        # Future games - return empty (no reliable future game data)
        return []


def filter_games_by_teams(games, selected_teams):
    """
    Filters games to only show those involving selected teams.

    Args:
        games: List of game dictionaries
        selected_teams: List of team names to filter by (empty = show all)

    Returns:
        Filtered list of games
    """
    if not selected_teams:
        return games

    filtered = []
    for game in games:
        home_name = game["home_team"]["name"]
        away_name = game["away_team"]["name"]

        if home_name in selected_teams or away_name in selected_teams:
            filtered.append(game)

    return filtered


def initialize_session_state():
    """
    Initializes session state variables for the dashboard.
    Called once at app startup.
    """
    # Selected date (defaults to today)
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = datetime.now().date()

    # Selected teams filter (empty = all teams)
    if "selected_teams" not in st.session_state:
        st.session_state.selected_teams = []

    # Refresh counter (used to force cache invalidation)
    if "refresh_counter" not in st.session_state:
        st.session_state.refresh_counter = 0


def reset_to_today():
    """Resets the selected date to today."""
    st.session_state.selected_date = datetime.now().date()
    st.session_state.selected_teams = []


def trigger_refresh():
    """
    Triggers a data refresh by incrementing the refresh counter.
    This can be used to invalidate cached data.
    """
    st.session_state.refresh_counter += 1
    # Clear the cache for fetch_games_for_date
    fetch_games_for_date.clear()


def get_available_dates():
    """
    Returns a range of dates that have game data available.
    Returns last 7 days and next 7 days.
    """
    today = datetime.now().date()
    dates = []

    for i in range(-7, 8):
        dates.append(today + timedelta(days=i))

    return dates


def get_games_with_filters():
    """
    Gets games for the currently selected date with team filters applied.
    Uses session state for all parameters.

    Returns:
        Tuple of (filtered_games, total_games_count)
    """
    date = st.session_state.selected_date
    selected_teams = st.session_state.selected_teams

    # Fetch all games for the date (cached)
    all_games = fetch_games_for_date(date)

    # Apply team filter
    filtered_games = filter_games_by_teams(all_games, selected_teams)

    return filtered_games, len(all_games)
