"""
Data Manager for NBA Scores Dashboard
Handles data fetching from nba_api, caching, and state management
"""

import streamlit as st
from datetime import datetime, timedelta
from constants import NBA_TEAMS

try:
    from nba_api.live.nba.endpoints import scoreboard, boxscore
    from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
    from nba_api.stats.endpoints import scoreboardv2
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


def extract_team_stats_from_live(team_data):
    """
    Extract team statistics from live API team data.

    Args:
        team_data: Team dict from live scoreboard API

    Returns:
        Dict with stats or None if not available
    """
    try:
        statistics = team_data.get("statistics", {})
        if not statistics:
            return None

        return {
            "fg_made": statistics.get("fieldGoalsMade"),
            "fg_attempted": statistics.get("fieldGoalsAttempted"),
            "fg3_made": statistics.get("threePointersMade"),
            "fg3_attempted": statistics.get("threePointersAttempted"),
            "ft_made": statistics.get("freeThrowsMade"),
            "ft_attempted": statistics.get("freeThrowsAttempted"),
            "ast": statistics.get("assists"),
            "reb": statistics.get("reboundsTotal"),
            "to": statistics.get("turnovers"),
        }
    except Exception:
        return None


def fetch_live_boxscore_stats(game_id):
    """
    Fetch detailed box score stats for a live game.

    Args:
        game_id: The game ID

    Returns:
        Dict with home and away team stats
    """
    if not NBA_API_AVAILABLE:
        return None, None

    try:
        box = boxscore.BoxScore(game_id=game_id)
        box_data = box.get_dict()

        game_data = box_data.get("game", {})
        home_team = game_data.get("homeTeam", {})
        away_team = game_data.get("awayTeam", {})

        home_stats = extract_team_stats_from_live(home_team)
        away_stats = extract_team_stats_from_live(away_team)

        return home_stats, away_stats
    except Exception:
        return None, None


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

            game_status_code = game_data.get("gameStatus", 1)

            # Handle scores for games that haven't started
            if game_status_code == 1:
                home_score = 0
                away_score = 0

            # Parse game status
            status = parse_game_status(game_data)

            # Extract stats from the scoreboard data (available for in-progress and finished games)
            home_stats = extract_team_stats_from_live(home_team_data)
            away_stats = extract_team_stats_from_live(away_team_data)

            # If stats not in scoreboard, try fetching from boxscore for finished/in-progress games
            if (home_stats is None or away_stats is None) and game_status_code >= 2:
                game_id = game_data.get("gameId")
                if game_id:
                    box_home, box_away = fetch_live_boxscore_stats(game_id)
                    if home_stats is None:
                        home_stats = box_home
                    if away_stats is None:
                        away_stats = box_away

            game = {
                "id": game_data.get("gameId", f"{today.isoformat()}-{home_tricode}-{away_tricode}"),
                "date": today,
                "status": status,
                "is_scheduled": game_status_code == 1,
                "home_team": {
                    "abbrev": home_team_info["abbrev"],
                    "name": home_team_info["name"],
                    "logo": home_team_info["logo"],
                    "score": home_score,
                    "stats": home_stats,
                },
                "away_team": {
                    "abbrev": away_team_info["abbrev"],
                    "name": away_team_info["name"],
                    "logo": away_team_info["logo"],
                    "score": away_score,
                    "stats": away_stats,
                },
            }
            games.append(game)

        return games

    except Exception as e:
        st.error(f"Error fetching NBA data: {str(e)}")
        return []


def fetch_historical_boxscore_stats(game_id):
    """
    Fetch box score stats for a historical game using stats API.

    Args:
        game_id: The game ID

    Returns:
        Dict mapping team_id to stats dict
    """
    if not NBA_API_AVAILABLE:
        return {}

    try:
        box = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        dfs = box.get_data_frames()

        # Team stats are in the second dataframe (index 1)
        if len(dfs) < 2:
            return {}

        team_stats_df = dfs[1]

        stats_by_team = {}
        for _, row in team_stats_df.iterrows():
            team_id = row.get("TEAM_ID")
            stats_by_team[team_id] = {
                "fg_made": row.get("FGM"),
                "fg_attempted": row.get("FGA"),
                "fg3_made": row.get("FG3M"),
                "fg3_attempted": row.get("FG3A"),
                "ft_made": row.get("FTM"),
                "ft_attempted": row.get("FTA"),
                "ast": row.get("AST"),
                "reb": row.get("REB"),
                "to": row.get("TO"),
            }

        return stats_by_team
    except Exception:
        return {}


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

            # Fetch detailed box score stats
            boxscore_stats = fetch_historical_boxscore_stats(game_id)

            home_team_id = home_row.get("TEAM_ID")
            away_team_id = away_row.get("TEAM_ID")

            home_stats = boxscore_stats.get(home_team_id)
            away_stats = boxscore_stats.get(away_team_id)

            game = {
                "id": game_id,
                "date": date,
                "status": "Final",
                "is_scheduled": False,
                "home_team": {
                    "abbrev": home_team_info["abbrev"],
                    "name": home_team_info["name"],
                    "logo": home_team_info["logo"],
                    "score": home_score,
                    "stats": home_stats,
                },
                "away_team": {
                    "abbrev": away_team_info["abbrev"],
                    "name": away_team_info["name"],
                    "logo": away_team_info["logo"],
                    "score": away_score,
                    "stats": away_stats,
                },
            }
            games.append(game)

        return games

    except Exception as e:
        st.error(f"Error fetching historical NBA data: {str(e)}")
        return []


def fetch_future_games(date):
    """
    Fetch scheduled games for a future date.

    The nba_api has limited support for future games, so we try
    scoreboardv2 first, then fall back gracefully.

    Args:
        date: datetime.date object (future date)

    Returns:
        List of game dictionaries for scheduled games
    """
    if not NBA_API_AVAILABLE:
        return []

    try:
        # Format date for the API
        date_str = date.strftime("%m/%d/%Y")

        # Try using scoreboardv2 for the specific date
        sb = scoreboardv2.ScoreboardV2(game_date=date_str)
        dfs = sb.get_data_frames()

        if not dfs or len(dfs) < 1:
            return []

        # GameHeader dataframe contains game info
        game_header_df = dfs[0]

        if game_header_df.empty:
            return []

        games = []

        for _, row in game_header_df.iterrows():
            home_team_id = row.get("HOME_TEAM_ID")
            away_team_id = row.get("VISITOR_TEAM_ID")

            # Get team abbreviations - we need to map from team IDs
            # The row should have team city and name info
            game_status_id = row.get("GAME_STATUS_ID", 1)
            game_status_text = row.get("GAME_STATUS_TEXT", "Scheduled")

            # Try to get team tricodes from the data
            # ScoreboardV2 provides GAMECODE which contains date and team codes
            gamecode = row.get("GAMECODE", "")

            # Parse home/away from additional fields
            home_abbrev = ""
            away_abbrev = ""

            # Try to find team abbrevs in the LineScore dataframe
            if len(dfs) > 1:
                line_score_df = dfs[1]
                game_id = row.get("GAME_ID")
                game_lines = line_score_df[line_score_df["GAME_ID"] == game_id] if "GAME_ID" in line_score_df.columns else line_score_df

                if not game_lines.empty:
                    for _, ls_row in game_lines.iterrows():
                        team_abbrev = ls_row.get("TEAM_ABBREVIATION", "")
                        team_id = ls_row.get("TEAM_ID")

                        if team_id == home_team_id:
                            home_abbrev = team_abbrev
                        elif team_id == away_team_id:
                            away_abbrev = team_abbrev

            # If we still don't have abbreviations, try to derive from gamecode
            if not home_abbrev or not away_abbrev:
                # GAMECODE format is typically "YYYYMMDD/VVVHHH" where VVV=visitor, HHH=home
                if "/" in gamecode and len(gamecode) >= 17:
                    teams_part = gamecode.split("/")[1] if "/" in gamecode else ""
                    if len(teams_part) >= 6:
                        away_abbrev = away_abbrev or teams_part[:3]
                        home_abbrev = home_abbrev or teams_part[3:6]

            home_team_info = get_team_info(home_abbrev)
            away_team_info = get_team_info(away_abbrev)

            # Parse game time
            game_time_str = row.get("GAME_DATE_EST", "")
            status = "Scheduled"

            if game_status_text:
                # Use the status text which often includes the time
                status = game_status_text

            game = {
                "id": row.get("GAME_ID", f"{date.isoformat()}-{away_abbrev}-{home_abbrev}"),
                "date": date,
                "status": status,
                "is_scheduled": True,
                "home_team": {
                    "abbrev": home_team_info["abbrev"],
                    "name": home_team_info["name"],
                    "logo": home_team_info["logo"],
                    "score": 0,
                    "stats": None,
                },
                "away_team": {
                    "abbrev": away_team_info["abbrev"],
                    "name": away_team_info["name"],
                    "logo": away_team_info["logo"],
                    "score": 0,
                    "stats": None,
                },
            }
            games.append(game)

        return games

    except Exception as e:
        # Future games may not be available - fail gracefully
        return []


@st.cache_data(ttl=60)  # Cache for 1 minute for live scores
def fetch_games_for_date(date):
    """
    Fetches games for a specific date.
    Uses live API for today, historical API for past dates,
    and scoreboardv2 for future dates.

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
        # Future games - try to fetch scheduled games
        return fetch_future_games(date)


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

    # Last refresh timestamp
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.now()


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
    st.session_state.last_refresh = datetime.now()
    # Clear the cache for fetch_games_for_date
    fetch_games_for_date.clear()


def get_last_refresh_time():
    """Returns the last refresh timestamp formatted as a time string."""
    if "last_refresh" in st.session_state:
        return st.session_state.last_refresh.strftime("%I:%M %p")
    return datetime.now().strftime("%I:%M %p")


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


def navigate_date(direction):
    """
    Navigate to the previous or next day.

    Args:
        direction: -1 for previous day, +1 for next day
    """
    today = datetime.now().date()
    min_date = today - timedelta(days=7)
    max_date = today + timedelta(days=7)

    new_date = st.session_state.selected_date + timedelta(days=direction)

    if min_date <= new_date <= max_date:
        st.session_state.selected_date = new_date
        return True
    return False


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
