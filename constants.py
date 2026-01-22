"""
NBA Team Constants and Logo URL Mappings
Uses ESPN's logo CDN for reliable team logos
"""

# ESPN Logo CDN base URL
ESPN_LOGO_BASE = "https://a.espncdn.com/i/teamlogos/nba/500"

# iOS Dark Mode Color Palette
IOS_COLORS = {
    "background": "#1C1C1E",           # iOS dark grey background
    "card_bg": "#2C2C2E",              # iOS elevated surface
    "card_border": "#3A3A3C",          # iOS separator color
    "text_primary": "#FFFFFF",          # Primary text
    "text_secondary": "#8E8E93",        # iOS secondary label
    "carolina_blue": "#4B9CD3",         # Accent - Carolina Blue
    "carolina_blue_light": "#7BAFD4",   # Lighter Carolina Blue
    "fire_red": "#CC0000",              # Accent - Fire Truck Red
    "fire_red_light": "#E63946",        # Lighter Fire Red
    "winner_highlight": "#30D158",      # iOS green
    "surface_elevated": "#3A3A3C",      # Elevated surface
    "nav_button": "#00D4FF",            # Bright electric cyan / Miami blue
    "nav_button_hover": "#33DFFF",      # Lighter hover state
    "nav_button_active": "#00A8CC",     # Darker teal on press
}

# NBA Teams with their abbreviations and full names
NBA_TEAMS = {
    "ATL": {"name": "Atlanta Hawks", "logo": f"{ESPN_LOGO_BASE}/atl.png"},
    "BOS": {"name": "Boston Celtics", "logo": f"{ESPN_LOGO_BASE}/bos.png"},
    "BKN": {"name": "Brooklyn Nets", "logo": f"{ESPN_LOGO_BASE}/bkn.png"},
    "CHA": {"name": "Charlotte Hornets", "logo": f"{ESPN_LOGO_BASE}/cha.png"},
    "CHI": {"name": "Chicago Bulls", "logo": f"{ESPN_LOGO_BASE}/chi.png"},
    "CLE": {"name": "Cleveland Cavaliers", "logo": f"{ESPN_LOGO_BASE}/cle.png"},
    "DAL": {"name": "Dallas Mavericks", "logo": f"{ESPN_LOGO_BASE}/dal.png"},
    "DEN": {"name": "Denver Nuggets", "logo": f"{ESPN_LOGO_BASE}/den.png"},
    "DET": {"name": "Detroit Pistons", "logo": f"{ESPN_LOGO_BASE}/det.png"},
    "GSW": {"name": "Golden State Warriors", "logo": f"{ESPN_LOGO_BASE}/gs.png"},
    "HOU": {"name": "Houston Rockets", "logo": f"{ESPN_LOGO_BASE}/hou.png"},
    "IND": {"name": "Indiana Pacers", "logo": f"{ESPN_LOGO_BASE}/ind.png"},
    "LAC": {"name": "LA Clippers", "logo": f"{ESPN_LOGO_BASE}/lac.png"},
    "LAL": {"name": "Los Angeles Lakers", "logo": f"{ESPN_LOGO_BASE}/lal.png"},
    "MEM": {"name": "Memphis Grizzlies", "logo": f"{ESPN_LOGO_BASE}/mem.png"},
    "MIA": {"name": "Miami Heat", "logo": f"{ESPN_LOGO_BASE}/mia.png"},
    "MIL": {"name": "Milwaukee Bucks", "logo": f"{ESPN_LOGO_BASE}/mil.png"},
    "MIN": {"name": "Minnesota Timberwolves", "logo": f"{ESPN_LOGO_BASE}/min.png"},
    "NOP": {"name": "New Orleans Pelicans", "logo": f"{ESPN_LOGO_BASE}/no.png"},
    "NYK": {"name": "New York Knicks", "logo": f"{ESPN_LOGO_BASE}/ny.png"},
    "OKC": {"name": "Oklahoma City Thunder", "logo": f"{ESPN_LOGO_BASE}/okc.png"},
    "ORL": {"name": "Orlando Magic", "logo": f"{ESPN_LOGO_BASE}/orl.png"},
    "PHI": {"name": "Philadelphia 76ers", "logo": f"{ESPN_LOGO_BASE}/phi.png"},
    "PHX": {"name": "Phoenix Suns", "logo": f"{ESPN_LOGO_BASE}/phx.png"},
    "POR": {"name": "Portland Trail Blazers", "logo": f"{ESPN_LOGO_BASE}/por.png"},
    "SAC": {"name": "Sacramento Kings", "logo": f"{ESPN_LOGO_BASE}/sac.png"},
    "SAS": {"name": "San Antonio Spurs", "logo": f"{ESPN_LOGO_BASE}/sa.png"},
    "TOR": {"name": "Toronto Raptors", "logo": f"{ESPN_LOGO_BASE}/tor.png"},
    "UTA": {"name": "Utah Jazz", "logo": f"{ESPN_LOGO_BASE}/utah.png"},
    "WAS": {"name": "Washington Wizards", "logo": f"{ESPN_LOGO_BASE}/wsh.png"},
}

# Get list of all team names for multi-select filter
def get_all_team_names():
    """Returns a list of all NBA team full names."""
    return [team["name"] for team in NBA_TEAMS.values()]

# Get team info by abbreviation
def get_team_by_abbrev(abbrev):
    """Returns team info dict for given abbreviation."""
    return NBA_TEAMS.get(abbrev, None)

# Get team abbreviation by full name
def get_abbrev_by_name(name):
    """Returns team abbreviation for given full name."""
    for abbrev, info in NBA_TEAMS.items():
        if info["name"] == name:
            return abbrev
    return None
