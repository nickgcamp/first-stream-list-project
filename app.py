"""
NBA Scores Dashboard - Main Application
A professional Streamlit dashboard for viewing NBA game scores
"""

import streamlit as st
from datetime import datetime, timedelta

from constants import get_all_team_names, IOS_COLORS
from data_manager import (
    initialize_session_state,
    reset_to_today,
    trigger_refresh,
    get_games_with_filters,
    navigate_date,
    get_last_refresh_time,
)
from style_utils import (
    get_main_styles,
    render_scorecard,
    render_header,
    render_no_games_message,
)

# Page configuration
st.set_page_config(
    page_title="Nico's NBA Scores",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
initialize_session_state()

# Inject custom CSS
st.markdown(get_main_styles(), unsafe_allow_html=True)


def render_sidebar():
    """Renders the sidebar with date picker, team filter, and controls."""
    with st.sidebar:
        st.markdown("### 🏀 Nico's NBA Scores")
        st.markdown("---")

        # Date picker section
        st.markdown('<p class="filter-header">Select Date</p>', unsafe_allow_html=True)

        # Calculate date range (7 days back, 7 days forward)
        today = datetime.now().date()
        min_date = today - timedelta(days=7)
        max_date = today + timedelta(days=7)

        selected_date = st.date_input(
            "Date",
            value=st.session_state.selected_date,
            min_value=min_date,
            max_value=max_date,
            key="date_picker",
            label_visibility="collapsed",
        )

        # Update session state if date changed
        if selected_date != st.session_state.selected_date:
            st.session_state.selected_date = selected_date
            st.rerun()

        st.markdown("---")

        # Team filter section
        st.markdown('<p class="filter-header">Filter by Team</p>', unsafe_allow_html=True)

        all_teams = get_all_team_names()
        selected_teams = st.multiselect(
            "Teams",
            options=sorted(all_teams),
            default=st.session_state.selected_teams,
            placeholder="All Teams",
            key="team_filter",
            label_visibility="collapsed",
        )

        # Update session state if teams changed
        if selected_teams != st.session_state.selected_teams:
            st.session_state.selected_teams = selected_teams
            st.rerun()

        st.markdown("---")

        # Action buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Refresh", key="sidebar_refresh", use_container_width=True):
                trigger_refresh()
                st.rerun()

        with col2:
            if st.button("📅 Today", key="sidebar_today", use_container_width=True):
                reset_to_today()
                st.rerun()

        # Display current filter info
        st.markdown("---")
        st.markdown("##### Current Filters")

        date_str = st.session_state.selected_date.strftime("%B %d, %Y")
        st.markdown(f"**Date:** {date_str}")

        if st.session_state.selected_teams:
            st.markdown(f"**Teams:** {len(st.session_state.selected_teams)} selected")
        else:
            st.markdown("**Teams:** All")


def render_navigation_bar():
    """Renders the interactive navigation bar with date arrows and refresh button."""
    # Last updated text on top
    last_updated = get_last_refresh_time()
    st.markdown(
        f'<p style="text-align: center; color: #8E8E93; font-size: 0.85rem; margin-bottom: 10px;">'
        f'Last updated: {last_updated}</p>',
        unsafe_allow_html=True,
    )

    # Three equal columns for buttons - use on_click callbacks for better mobile touch handling
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.button("←", key="prev_day", use_container_width=True, on_click=lambda: navigate_date(-1))

    with col2:
        st.button("🔄", key="refresh_nav", use_container_width=True, on_click=trigger_refresh)

    with col3:
        st.button("→", key="next_day", use_container_width=True, on_click=lambda: navigate_date(+1))

    # Date display below nav buttons
    date_str = st.session_state.selected_date.strftime("%A, %B %d, %Y")
    st.markdown(
        f'<p style="text-align: center; color: {IOS_COLORS["text_primary"]}; '
        f'font-size: 1.1rem; font-weight: 500; margin: 10px 0 20px 0;">{date_str}</p>',
        unsafe_allow_html=True,
    )


def render_games_grid(games):
    """
    Renders games in a responsive grid layout.

    Args:
        games: List of game dictionaries
    """
    # Use 2 columns for the grid
    num_cols = 2

    # Create rows of games
    for i in range(0, len(games), num_cols):
        cols = st.columns(num_cols)

        for j in range(num_cols):
            game_idx = i + j

            if game_idx < len(games):
                with cols[j]:
                    game = games[game_idx]
                    card_html = render_scorecard(game)
                    st.markdown(card_html, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Render sidebar
    render_sidebar()

    # Main content area
    # Render header
    st.markdown(render_header("Nico's NBA Scores"), unsafe_allow_html=True)

    # Render navigation bar
    render_navigation_bar()

    # Get filtered games
    games, total_count = get_games_with_filters()

    # Show filter status if filtering
    if st.session_state.selected_teams:
        st.markdown(
            f"<p style='text-align: center; color: {IOS_COLORS['text_secondary']}; margin-bottom: 20px;'>"
            f"Showing {len(games)} of {total_count} games</p>",
            unsafe_allow_html=True,
        )

    # Render games or no games message
    if games:
        render_games_grid(games)
    else:
        st.markdown(render_no_games_message(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
