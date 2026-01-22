"""
Custom CSS Styles for NBA Scores Dashboard
Dark mode theme with rounded card components
"""

# Color palette
COLORS = {
    "background": "#0E1117",
    "card_bg": "#262730",
    "card_border": "#3D3D3D",
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0B0B0",
    "accent": "#FF4B4B",
    "winner_highlight": "#00D26A",
}


def get_main_styles():
    """Returns the main CSS styles for the dashboard."""
    return f"""
    <style>
        /* Main app background */
        .stApp {{
            background-color: {COLORS['background']};
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['card_bg']};
        }}

        /* Header styling */
        .dashboard-header {{
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
        }}

        .dashboard-header h1 {{
            color: {COLORS['text_primary']};
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
        }}

        .dashboard-header p {{
            color: {COLORS['text_secondary']};
            font-size: 1rem;
            margin-top: 5px;
        }}

        /* Scorecard container */
        .scorecard {{
            background-color: {COLORS['card_bg']};
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid {COLORS['card_border']};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .scorecard:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }}

        /* Game status badge */
        .game-status {{
            text-align: center;
            font-size: 0.75rem;
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            padding: 4px 12px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            display: inline-block;
        }}

        .game-status.final {{
            color: {COLORS['winner_highlight']};
            background-color: rgba(0, 210, 106, 0.15);
        }}

        /* Team row styling */
        .team-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 0;
        }}

        .team-info {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .team-logo {{
            width: 45px;
            height: 45px;
            object-fit: contain;
        }}

        .team-name {{
            color: {COLORS['text_primary']};
            font-size: 1.1rem;
            font-weight: 500;
        }}

        .team-score {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {COLORS['text_primary']};
        }}

        .team-score.winner {{
            color: {COLORS['winner_highlight']};
        }}

        .team-score.loser {{
            color: {COLORS['text_secondary']};
        }}

        /* Divider between teams */
        .team-divider {{
            height: 1px;
            background-color: {COLORS['card_border']};
            margin: 5px 0;
        }}

        /* No games message */
        .no-games {{
            text-align: center;
            padding: 60px 20px;
            color: {COLORS['text_secondary']};
            font-size: 1.2rem;
        }}

        /* Filter section header */
        .filter-header {{
            color: {COLORS['text_primary']};
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Custom button styling */
        .stButton > button {{
            background-color: {COLORS['accent']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            width: 100%;
        }}

        .stButton > button:hover {{
            background-color: #FF6B6B;
        }}
    </style>
    """


def render_scorecard(game_data):
    """
    Renders a single scorecard HTML for a game.

    Args:
        game_data: dict with keys:
            - home_team: dict with name, logo, score
            - away_team: dict with name, logo, score
            - status: str (e.g., "Final", "In Progress")
    """
    home = game_data["home_team"]
    away = game_data["away_team"]
    status = game_data["status"]

    # Determine winner
    home_winner = home["score"] > away["score"]
    away_winner = away["score"] > home["score"]

    home_score_class = "winner" if home_winner else "loser" if away_winner else ""
    away_score_class = "winner" if away_winner else "loser" if home_winner else ""

    status_class = "final" if status.lower() == "final" else ""

    return f"""
    <div class="scorecard">
        <div style="text-align: center;">
            <span class="game-status {status_class}">{status}</span>
        </div>

        <div class="team-row">
            <div class="team-info">
                <img class="team-logo" src="{away['logo']}" alt="{away['name']}">
                <span class="team-name">{away['name']}</span>
            </div>
            <span class="team-score {away_score_class}">{away['score']}</span>
        </div>

        <div class="team-divider"></div>

        <div class="team-row">
            <div class="team-info">
                <img class="team-logo" src="{home['logo']}" alt="{home['name']}">
                <span class="team-name">{home['name']}</span>
            </div>
            <span class="team-score {home_score_class}">{home['score']}</span>
        </div>
    </div>
    """


def render_header(date_str):
    """Renders the dashboard header with the selected date."""
    return f"""
    <div class="dashboard-header">
        <h1>NBA Scores</h1>
        <p>{date_str}</p>
    </div>
    """


def render_no_games_message():
    """Renders a message when no games are found."""
    return """
    <div class="no-games">
        <p>No games scheduled for this date</p>
        <p style="font-size: 0.9rem; margin-top: 10px;">Try selecting a different date or adjusting your filters</p>
    </div>
    """
