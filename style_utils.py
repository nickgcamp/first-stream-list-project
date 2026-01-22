"""
Custom CSS Styles for NBA Scores Dashboard
iOS Dark Mode theme with rounded card components
"""

from constants import IOS_COLORS

# Use iOS color palette
COLORS = IOS_COLORS


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

        /* Hamburger menu styling - make it larger and more visible */
        [data-testid="collapsedControl"] {{
            width: 44px !important;
            height: 44px !important;
            top: 10px !important;
            left: 10px !important;
        }}

        [data-testid="collapsedControl"] svg {{
            width: 28px !important;
            height: 28px !important;
            stroke: {COLORS['text_primary']} !important;
            stroke-width: 2.5px !important;
        }}

        [data-testid="collapsedControl"]:hover {{
            background-color: {COLORS['surface_elevated']} !important;
            border-radius: 8px;
        }}

        /* Custom hamburger icon styling */
        button[kind="header"] {{
            width: 44px !important;
            height: 44px !important;
        }}

        /* Sidebar toggle button container */
        [data-testid="stSidebarCollapseButton"] {{
            width: 44px !important;
            height: 44px !important;
        }}

        [data-testid="stSidebarCollapseButton"] button {{
            width: 44px !important;
            height: 44px !important;
            padding: 8px !important;
        }}

        [data-testid="stSidebarCollapseButton"] svg {{
            width: 28px !important;
            height: 28px !important;
        }}

        /* Header styling */
        .dashboard-header {{
            text-align: center;
            padding: 20px 0 10px 0;
            margin-bottom: 10px;
        }}

        .dashboard-header h1 {{
            color: {COLORS['text_primary']};
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
        }}

        /* Navigation bar styling */
        .nav-bar {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 15px 20px;
            background-color: {COLORS['card_bg']};
            border-radius: 15px;
            margin-bottom: 25px;
        }}

        .nav-arrow {{
            background-color: {COLORS['surface_elevated']};
            border: none;
            border-radius: 10px;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background-color 0.2s ease, transform 0.1s ease;
            color: {COLORS['carolina_blue']};
            font-size: 1.3rem;
            font-weight: bold;
        }}

        .nav-arrow:hover {{
            background-color: {COLORS['carolina_blue']};
            color: white;
            transform: scale(1.05);
        }}

        .refresh-btn {{
            background-color: {COLORS['surface_elevated']};
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.2s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }}

        .refresh-btn:hover {{
            background-color: {COLORS['carolina_blue']};
        }}

        .refresh-btn:hover .refresh-text {{
            color: white;
        }}

        .refresh-text {{
            color: {COLORS['text_secondary']};
            font-size: 0.85rem;
        }}

        .date-display {{
            color: {COLORS['text_primary']};
            font-size: 1.1rem;
            font-weight: 500;
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
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
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
            background-color: rgba(48, 209, 88, 0.15);
        }}

        .game-status.scheduled {{
            color: {COLORS['carolina_blue']};
            background-color: rgba(75, 156, 211, 0.15);
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

        /* Team stats styling */
        .team-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px 12px;
            margin-top: 8px;
            padding: 8px 10px;
            background-color: {COLORS['surface_elevated']};
            border-radius: 8px;
            font-size: 0.7rem;
        }}

        .stat-item {{
            color: {COLORS['text_secondary']};
        }}

        .stat-label {{
            color: {COLORS['carolina_blue']};
            font-weight: 600;
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

        /* Custom button styling - Navy/Carolina blue mix */
        .stButton > button {{
            background-color: {COLORS['nav_button']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            width: 100%;
            min-height: 50px;
        }}

        .stButton > button:hover {{
            background-color: {COLORS['nav_button_hover']};
        }}

        .stButton > button:active {{
            background-color: {COLORS['nav_button_active']};
        }}

        /* Date input styling */
        .stDateInput > div > div > input {{
            background-color: {COLORS['surface_elevated']};
            color: {COLORS['text_primary']};
            border-color: {COLORS['card_border']};
        }}

        /* Multiselect styling */
        .stMultiSelect > div > div {{
            background-color: {COLORS['surface_elevated']};
            border-color: {COLORS['card_border']};
        }}

        /* Scheduled game time styling */
        .game-time {{
            color: {COLORS['carolina_blue']};
            font-weight: 600;
        }}

        /* ============================================
           TOUCH OPTIMIZATION & iOS SPECIFIC STYLES
           ============================================ */

        /* Smooth scrolling for iOS */
        .stApp {{
            -webkit-overflow-scrolling: touch;
        }}

        /* Global touch optimization for all buttons */
        .stButton > button {{
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
            min-height: 44px;
            touch-action: manipulation;
        }}

        /* Active state for touch feedback */
        .stButton > button:active {{
            background-color: {COLORS['nav_button_active']};
            transform: scale(0.96);
            transition: transform 0.1s ease, background-color 0.1s ease;
        }}

        /* Ensure minimum touch target size */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] button {{
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            touch-action: manipulation;
        }}

        /* ============================================
           TABLET RESPONSIVE STYLES (max-width: 768px)
           ============================================ */
        @media (max-width: 768px) {{
            /* Header adjustments */
            .dashboard-header {{
                padding: 15px 0 8px 0;
            }}

            .dashboard-header h1 {{
                font-size: 1.8rem;
            }}

            /* Scorecard adjustments */
            .scorecard {{
                margin: 8px 5px;
                padding: 15px;
                border-radius: 12px;
            }}

            /* Team info adjustments */
            .team-name {{
                font-size: 1rem;
            }}

            .team-logo {{
                width: 40px;
                height: 40px;
            }}

            .team-score {{
                font-size: 1.3rem;
            }}

            /* Team stats grid */
            .team-stats {{
                font-size: 0.65rem;
                gap: 4px 10px;
                padding: 6px 8px;
            }}

            /* Navigation buttons larger on tablet */
            .nav-arrow {{
                width: 50px !important;
                height: 50px !important;
                font-size: 1.4rem;
            }}

            /* Button minimum heights */
            .stButton > button {{
                min-height: 48px;
                font-size: 0.9rem;
            }}
        }}

        /* ============================================
           MOBILE RESPONSIVE STYLES (max-width: 480px)
           ============================================ */
        @media (max-width: 480px) {{
            /* Ensure minimum font size to prevent iOS zoom */
            html, body {{
                font-size: 16px;
            }}

            /* Header smaller on mobile */
            .dashboard-header {{
                padding: 10px 0 5px 0;
                margin-bottom: 5px;
            }}

            .dashboard-header h1 {{
                font-size: 1.5rem;
            }}

            /* Scorecard mobile optimization */
            .scorecard {{
                margin: 6px 0;
                padding: 12px;
                border-radius: 10px;
            }}

            .scorecard:hover {{
                transform: none;
                box-shadow: none;
            }}

            /* Team row tighter spacing */
            .team-row {{
                padding: 8px 0;
            }}

            .team-info {{
                gap: 8px;
            }}

            .team-name {{
                font-size: 0.9rem;
            }}

            .team-logo {{
                width: 35px;
                height: 35px;
            }}

            .team-score {{
                font-size: 1.2rem;
            }}

            /* Team stats more compact */
            .team-stats {{
                font-size: 0.6rem;
                gap: 3px 6px;
                padding: 5px 6px;
                margin-top: 6px;
            }}

            /* Game status badge smaller */
            .game-status {{
                font-size: 0.65rem;
                padding: 3px 10px;
                margin-bottom: 10px;
            }}

            /* Navigation buttons well-spaced */
            .stButton > button {{
                min-height: 50px;
                padding: 12px 8px;
                font-size: 1rem;
            }}

            /* No games message */
            .no-games {{
                padding: 40px 15px;
                font-size: 1rem;
            }}

            /* Filter header */
            .filter-header {{
                font-size: 0.8rem;
            }}

            /* Team divider */
            .team-divider {{
                margin: 3px 0;
            }}
        }}

        /* ============================================
           SMALL MOBILE STYLES (max-width: 375px)
           iPhone SE, older iPhones
           ============================================ */
        @media (max-width: 375px) {{
            .dashboard-header h1 {{
                font-size: 1.3rem;
            }}

            .team-name {{
                font-size: 0.85rem;
            }}

            .team-logo {{
                width: 32px;
                height: 32px;
            }}

            .team-score {{
                font-size: 1.1rem;
            }}

            .team-stats {{
                font-size: 0.55rem;
                gap: 2px 4px;
            }}

            .scorecard {{
                padding: 10px;
            }}
        }}

        /* ============================================
           PREVENT HORIZONTAL SCROLLING
           ============================================ */
        .main .block-container {{
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
            overflow-x: hidden;
        }}

        @media (max-width: 480px) {{
            .main .block-container {{
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }}
        }}

        /* ============================================
           NAVIGATION BUTTONS - ALWAYS HORIZONTAL
           ============================================ */
        /* Keep navigation button rows horizontal on ALL screen sizes */
        [data-testid="stHorizontalBlock"] {{
            flex-wrap: nowrap !important;
            gap: 8px;
        }}

        /* Make navigation buttons square-ish with equal sizing */
        .stButton > button {{
            min-width: 60px;
            aspect-ratio: 1.2;
        }}

        /* Mobile adjustments for navigation spacing */
        @media (max-width: 480px) {{
            [data-testid="stHorizontalBlock"] {{
                gap: 6px;
            }}

            /* Ensure columns don't expand to full width for nav buttons */
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
                flex: 1 1 auto !important;
                width: auto !important;
                min-width: 0 !important;
            }}
        }}

        @media (max-width: 375px) {{
            [data-testid="stHorizontalBlock"] {{
                gap: 4px;
            }}
        }}
    </style>
    """


def format_stat(made, attempted, stat_type=""):
    """
    Format a stat line like FG: 35/80 (43.8%).

    Args:
        made: Made shots/attempts
        attempted: Total attempts
        stat_type: Type prefix (FG, 3PT, FT)

    Returns:
        Formatted stat string
    """
    if made is None or attempted is None:
        return f"{stat_type}: - / - (-)"

    try:
        made = int(made)
        attempted = int(attempted)
        if attempted > 0:
            pct = (made / attempted) * 100
            return f"{stat_type}: {made}/{attempted} ({pct:.1f}%)"
        else:
            return f"{stat_type}: {made}/{attempted} (-)"
    except (ValueError, TypeError):
        return f"{stat_type}: - / - (-)"


def format_simple_stat(value, stat_type):
    """
    Format a simple stat like AST: 25.

    Args:
        value: The stat value
        stat_type: Type prefix (AST, REB, TO)

    Returns:
        Formatted stat string
    """
    if value is None:
        return f"{stat_type}: -"
    try:
        return f"{stat_type}: {int(value)}"
    except (ValueError, TypeError):
        return f"{stat_type}: -"


def render_team_stats_html(stats):
    """
    Renders the HTML for team stats in a compact grid.

    Args:
        stats: Dict with keys fg_made, fg_attempted, fg3_made, fg3_attempted,
               ft_made, ft_attempted, ast, reb, to

    Returns:
        HTML string for stats grid
    """
    if not stats:
        return ""

    fg = format_stat(stats.get("fg_made"), stats.get("fg_attempted"), "FG")
    fg3 = format_stat(stats.get("fg3_made"), stats.get("fg3_attempted"), "3PT")
    ft = format_stat(stats.get("ft_made"), stats.get("ft_attempted"), "FT")
    ast = format_simple_stat(stats.get("ast"), "AST")
    reb = format_simple_stat(stats.get("reb"), "REB")
    to = format_simple_stat(stats.get("to"), "TO")

    html = f'<div class="team-stats">'
    html += f'<span class="stat-item"><span class="stat-label">FG:</span> {fg.replace("FG: ", "")}</span>'
    html += f'<span class="stat-item"><span class="stat-label">3PT:</span> {fg3.replace("3PT: ", "")}</span>'
    html += f'<span class="stat-item"><span class="stat-label">FT:</span> {ft.replace("FT: ", "")}</span>'
    html += f'<span class="stat-item"><span class="stat-label">AST:</span> {ast.replace("AST: ", "")}</span>'
    html += f'<span class="stat-item"><span class="stat-label">REB:</span> {reb.replace("REB: ", "")}</span>'
    html += f'<span class="stat-item"><span class="stat-label">TO:</span> {to.replace("TO: ", "")}</span>'
    html += f'</div>'

    return html


def render_scorecard(game_data):
    """
    Renders a single scorecard HTML for a game.

    Args:
        game_data: dict with keys:
            - home_team: dict with name, logo, score, stats (optional)
            - away_team: dict with name, logo, score, stats (optional)
            - status: str (e.g., "Final", "In Progress", "7:00 PM CT")
            - is_scheduled: bool (optional) - True for future games
    """
    home = game_data["home_team"]
    away = game_data["away_team"]
    status = game_data["status"]
    is_scheduled = game_data.get("is_scheduled", False)

    # Determine winner (only for completed games)
    if not is_scheduled and home["score"] > 0 or away["score"] > 0:
        home_winner = home["score"] > away["score"]
        away_winner = away["score"] > home["score"]
        home_score_class = "winner" if home_winner else "loser" if away_winner else ""
        away_score_class = "winner" if away_winner else "loser" if home_winner else ""
        home_score_display = home["score"]
        away_score_display = away["score"]
    else:
        home_score_class = ""
        away_score_class = ""
        home_score_display = "-"
        away_score_display = "-"

    # Status class for badge styling
    status_lower = status.lower()
    if status_lower == "final":
        status_class = "final"
    elif is_scheduled or "scheduled" in status_lower or "pm" in status_lower or "am" in status_lower:
        status_class = "scheduled"
    else:
        status_class = ""

    # Get team stats if available
    home_stats_html = render_team_stats_html(home.get("stats"))
    away_stats_html = render_team_stats_html(away.get("stats"))

    # Build HTML as single line to avoid Streamlit markdown parsing issues
    html = f'<div class="scorecard">'
    html += f'<div style="text-align: center;"><span class="game-status {status_class}">{status}</span></div>'

    # Away team
    html += f'<div class="team-row"><div class="team-info">'
    html += f'<img class="team-logo" src="{away["logo"]}" alt="{away["name"]}">'
    html += f'<span class="team-name">{away["name"]}</span></div>'
    html += f'<span class="team-score {away_score_class}">{away_score_display}</span></div>'
    html += away_stats_html

    html += f'<div class="team-divider"></div>'

    # Home team
    html += f'<div class="team-row"><div class="team-info">'
    html += f'<img class="team-logo" src="{home["logo"]}" alt="{home["name"]}">'
    html += f'<span class="team-name">{home["name"]}</span></div>'
    html += f'<span class="team-score {home_score_class}">{home_score_display}</span></div>'
    html += home_stats_html

    html += f'</div>'

    return html


def render_header(title="Nico's NBA Scores"):
    """Renders the dashboard header."""
    return f"""
    <div class="dashboard-header">
        <h1>{title}</h1>
    </div>
    """


def render_navigation_bar(date_str, last_updated):
    """
    Renders the navigation bar with date arrows and refresh button.

    Args:
        date_str: Current date string to display
        last_updated: Last refresh timestamp string

    Returns:
        HTML string for the navigation bar
    """
    return f"""
    <div class="nav-bar">
        <div class="date-display">{date_str}</div>
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
