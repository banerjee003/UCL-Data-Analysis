import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UCL Analytics Dashboard",
    page_icon="./images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COLORS
# ============================================================

UCL_NAVY = "#0B1D4A"
UCL_GOLD = "#C4A35A"
UCL_BLUE = "#1B4B8C"
UCL_LIGHT_BLUE = "#5B8DEF"
UCL_RED = "#8B1E3F"
UCL_GREEN = "#2E8B57"
UCL_GREY = "#7A8BA3"


# ============================================================
# PLOTLY DEFAULTS
# ============================================================

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = [
    UCL_BLUE,
    UCL_GOLD,
    UCL_LIGHT_BLUE,
    UCL_RED,
    UCL_GREEN,
]


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    path = os.path.join(
        os.path.dirname(__file__),
        "ucl.csv"
    )

    df = pd.read_csv(path)

    # --------------------------------------------------------
    # REMOVE TRUE DUPLICATE MATCH RECORDS
    # --------------------------------------------------------
    match_columns = [
        "season",
        "home_team",
        "away_team",
        "home_goals",
        "away_goals",
        "result"
    ]

    df = df.drop_duplicates(
        subset=match_columns,
        keep="first"
    ).reset_index(drop=True)

    # Create total goals
    df["total_goals"] = (
        df["home_goals"] +
        df["away_goals"]
    )

    return df


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def apply_filters(df, seasons):

    if not seasons:
        return df.copy()

    return df[
        df["season"].isin(seasons)
    ].copy()


def unique_teams(df):

    return pd.Index(
        pd.concat(
            [
                df["home_team"],
                df["away_team"]
            ]
        ).unique()
    )


def team_matches(df):

    home = df.groupby("home_team").size()

    away = df.groupby("away_team").size()

    return home.add(
        away,
        fill_value=0
    ).astype(int)


def team_goals_scored(df):

    home = (
        df.groupby("home_team")["home_goals"]
        .sum()
    )

    away = (
        df.groupby("away_team")["away_goals"]
        .sum()
    )

    return home.add(
        away,
        fill_value=0
    ).astype(int)


def team_goals_conceded(df):

    home = (
        df.groupby("home_team")["away_goals"]
        .sum()
    )

    away = (
        df.groupby("away_team")["home_goals"]
        .sum()
    )

    return home.add(
        away,
        fill_value=0
    ).astype(int)


def team_wins(df):

    home_wins = (
        df[df["result"] == "H"]
        .groupby("home_team")
        .size()
    )

    away_wins = (
        df[df["result"] == "A"]
        .groupby("away_team")
        .size()
    )

    return home_wins.add(
        away_wins,
        fill_value=0
    ).astype(int)


def team_draws(df):

    home_draws = (
        df[df["result"] == "D"]
        .groupby("home_team")
        .size()
    )

    away_draws = (
        df[df["result"] == "D"]
        .groupby("away_team")
        .size()
    )

    return home_draws.add(
        away_draws,
        fill_value=0
    ).astype(int)


def team_losses(df):

    matches = team_matches(df)

    wins = team_wins(df)

    draws = team_draws(df)

    return matches - wins - draws

def style_fig(fig, height=420):

    fig.update_layout(
        height=height,

        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        ),

        title_font=dict(
            size=17,
            color="#FFFFFF"
        ),

        font=dict(
            family="Segoe UI, sans-serif",
            color="#E5E7EB"
        ),

        plot_bgcolor="#151B26",

        paper_bgcolor="#151B26",

        legend=dict(
            font=dict(
                color="#E5E7EB"
            )
        ),

        legend_title=dict(
            font=dict(
                color="#FFFFFF"
            )
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#273244",
        zerolinecolor="#374151",
        color="#D1D5DB"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#273244",
        zerolinecolor="#374151",
        color="#D1D5DB"
    )

    return fig

# ============================================================
# CUSTOM DARK THEME
# ============================================================

st.markdown(
    """
<style>

    /* ==============================
       MAIN APPLICATION
       ============================== */

    .stApp {
        background-color: #0E1117;
        color: #F5F7FA;
    }

    .main {
        background-color: #0E1117;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==============================
       TOP HEADER
       ============================== */

    header[data-testid="stHeader"] {
        background-color: #0E1117;
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #273244;
    }

    section[data-testid="stSidebar"] * {
        color: #F5F7FA !important;
    }

    section[data-testid="stSidebar"] .stMultiSelect,
    section[data-testid="stSidebar"] .stSlider {
        color: #FFFFFF;
    }


    /* ==============================
       HEADINGS
       ============================== */

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p {
        color: #D1D5DB;
    }

    label {
        color: #E5E7EB !important;
    }


    /* ==============================
       HERO SECTION
       ============================== */

    .hero {
        background:
            linear-gradient(
                135deg,
                #071A3D 0%,
                #123A78 50%,
                #071A3D 100%
            );

        border: 1px solid #315A9B;

        color: #FFFFFF;

        padding: 2rem 2.2rem;

        border-radius: 18px;

        margin-bottom: 1.5rem;

        margin-top: 1.5rem;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.35);
    }

    .hero h1 {
        color: #FFFFFF !important;

        margin: 0 0 0.6rem 0;

        font-size: 2.2rem;

        font-weight: 700;
    }

    .hero p {
        color: #DCE7F8 !important;

        margin: 0;

        font-size: 1.05rem;

        line-height: 1.6;
    }


    /* ==============================
       METRICS
       ============================== */

    div[data-testid="stMetric"] {
        background-color: #151B26;

        border: 1px solid #273244;

        border-radius: 12px;

        padding: 1rem;

        box-shadow:
            0 4px 15px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stMetricLabel"] {
        color: #9CA3AF !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #C4A35A !important;
    }


    /* ==============================
       TABS
       ============================== */

    button[data-baseweb="tab"] {
        color: #9CA3AF !important;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #C4A35A !important;
    }


    /* ==============================
       INPUT BOXES
       ============================== */

    div[data-baseweb="input"] {
        background-color: #151B26 !important;

        border: 1px solid #374151 !important;

        border-radius: 8px !important;
    }

    div[data-baseweb="input"] input {
        color: #FFFFFF !important;

        background-color: #151B26 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #6B7280 !important;
    }


    /* ==============================
       SELECTBOX / MULTISELECT
       ============================== */

    div[data-baseweb="select"] > div {
        background-color: #151B26 !important;

        border-color: #374151 !important;

        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }

    div[data-baseweb="popover"] {
        background-color: #151B26 !important;
    }

    li[role="option"] {
        background-color: #151B26 !important;

        color: #FFFFFF !important;
    }

    li[role="option"]:hover {
        background-color: #24344D !important;
    }


    /* ==============================
       SLIDER
       ============================== */

    div[data-testid="stSlider"] label {
        color: #E5E7EB !important;
    }


    /* ==============================
       DATAFRAMES
       ============================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #273244;

        border-radius: 10px;

        overflow: hidden;
    }


    /* ==============================
       INFO / SUCCESS / WARNING
       ============================== */

    div[data-testid="stAlert"] {
        background-color: #151B26;

        color: #E5E7EB;

        border: 1px solid #374151;
    }


    /* ==============================
       INSIGHT CARDS
       ============================== */

    .insight {
        background-color: #151B26;

        border-left: 4px solid #C4A35A;

        border-top: 1px solid #273244;

        border-right: 1px solid #273244;

        border-bottom: 1px solid #273244;

        padding: 1rem 1.1rem;

        border-radius: 10px;

        margin-bottom: 0.8rem;

        color: #D1D5DB;

        line-height: 1.7;

        box-shadow:
            0 4px 15px rgba(0, 0, 0, 0.15);
    }

    .insight b {
        color: #FFFFFF;
    }


    /* ==============================
       TEAM CARD
       ============================== */

    .team-card {
        background:
            linear-gradient(
                135deg,
                #151B26,
                #1B2638
            );

        padding: 1.4rem;

        border-radius: 14px;

        border: 1px solid #334155;

        margin-bottom: 1rem;

        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.2);
    }

    .team-card h2 {
        color: #FFFFFF !important;

        margin-bottom: 0.4rem;
    }

    .team-card p {
        color: #9CA3AF !important;
    }


    /* ==============================
       CAPTIONS
       ============================== */

    .stCaption,
    div[data-testid="stCaptionContainer"] {
        color: #9CA3AF !important;
    }


    /* ==============================
       DIVIDERS
       ============================== */

    hr {
        border-color: #273244 !important;
    }


    /* ==============================
       BUTTONS
       ============================== */

    button[kind="secondary"] {
        background-color: #151B26 !important;

        color: #FFFFFF !important;

        border: 1px solid #374151 !important;
    }

</style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

raw = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Dashboard Filters")

all_seasons = sorted(
    raw["season"].unique().tolist()
)

selected_seasons = st.sidebar.multiselect(
    "Select Season",
    options=all_seasons,
    default=all_seasons
)


# Minimum matches for win percentage
min_matches = st.sidebar.slider(
    "Minimum Matches for Win %",
    min_value=1,
    max_value=50,
    value=10,
    help="Prevents teams with very few matches from dominating the win-rate ranking."
)


# Apply filters
df = apply_filters(
    raw,
    selected_seasons
)


if df.empty:

    st.warning(
        "No matches available for the selected seasons."
    )

    st.stop()


# ============================================================
# GLOBAL CALCULATIONS
# ============================================================

n_matches = len(df)

n_seasons = df["season"].nunique()

n_teams = unique_teams(df).size

n_goals = int(
    df["total_goals"].sum()
)

avg_goals = df["total_goals"].mean()

result_counts = (
    df["result"]
    .value_counts()
)

home_wins = int(
    result_counts.get("H", 0)
)

away_wins = int(
    result_counts.get("A", 0)
)

draws = int(
    result_counts.get("D", 0)
)

home_win_pct = (
    home_wins * 100 / n_matches
)

away_win_pct = (
    away_wins * 100 / n_matches
)

draw_pct = (
    draws * 100 / n_matches
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
<div class="hero">
    <h1>⚽ UEFA Champions League Analytics</h1>
    <p>
        Historical match outcomes, team performance,
        goal trends and interactive club analysis.
    </p>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Matches",
    f"{n_matches:,}"
)

c2.metric(
    "Seasons",
    n_seasons
)

c3.metric(
    "Teams",
    n_teams
)

c4.metric(
    "Total Goals",
    f"{n_goals:,}"
)

c5.metric(
    "Avg Goals / Match",
    f"{avg_goals:.2f}"
)

c6.metric(
    "Home Win %",
    f"{home_win_pct:.1f}%"
)


# ============================================================
# TABS
# ============================================================

(
    tab_overview,
    tab_outcomes,
    tab_teams,
    tab_goals,
    tab_high,
    tab_data
) = st.tabs(
    [
        "📊 Overview",
        "🏠 Match Outcomes",
        "🏆 Team Performance",
        "⚽ Goal Trends",
        "🔥 High-Scoring Games",
        "🔎 Match Explorer"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab_overview:

    st.subheader(
        "UCL Dataset Overview"
    )

    col1, col2 = st.columns(
        [1, 1],
        gap="large"
    )


    # --------------------------------------------------------
    # RESULT DISTRIBUTION
    # --------------------------------------------------------

    with col1:

        st.markdown("### Match Result Distribution")

        outcome_df = pd.DataFrame(
            {
                "Outcome": [
                    "Home Win",
                    "Away Win",
                    "Draw"
                ],

                "Matches": [
                    home_wins,
                    away_wins,
                    draws
                ],

                "Percentage": [
                    home_win_pct,
                    away_win_pct,
                    draw_pct
                ]
            }
        )

        fig = px.bar(
            outcome_df,
            x="Outcome",
            y="Matches",
            color="Outcome",
            text_auto=True,
            title="Match Result Distribution"
        )

        st.plotly_chart(
            style_fig(fig, 430),
            use_container_width=True
        )


    # --------------------------------------------------------
    # RESULT TABLE
    # --------------------------------------------------------

    with col2:

        st.markdown(
            "### Result Breakdown"
        )

        display_outcomes = (
            outcome_df
            .copy()
        )

        display_outcomes["Percentage"] = (
            display_outcomes["Percentage"]
            .round(2)
        )

        st.dataframe(
            display_outcomes,
            hide_index=True,
            use_container_width=True
        )

        st.markdown(
            f"""
            <div class="insight" style="line-height:1.46">

            🏠 Home teams win
            <b>{home_win_pct:.2f}%</b> of matches.

            <br>

            ✈️ Away teams win
            <b>{away_win_pct:.2f}%</b>.

            <br>

            🤝 Draws account for
            <b>{draw_pct:.2f}%</b>.

            <br>

            ⚽ Average goals per match:
            <b>{avg_goals:.2f}</b>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # GOALS PER SEASON
    # --------------------------------------------------------

    st.subheader(
        "Goals Scored by Season"
    )

    goals_per_season = (
        df.groupby("season")["total_goals"]
        .sum()
        .reset_index()
    )

    goals_per_season.columns = [
        "Season",
        "Goals"
    ]

    fig = px.line(
        goals_per_season,
        x="Season",
        y="Goals",
        markers=True,
        title="Total Goals per Season"
    )

    fig.update_traces(
        line_color=UCL_BLUE,
        marker_color=UCL_GOLD
    )

    st.plotly_chart(
        style_fig(fig, 380),
        use_container_width=True
    )


    # --------------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "💡 Key Insights"
    )

    peak = goals_per_season.loc[
        goals_per_season["Goals"].idxmax()
    ]

    team_goals = (
        team_goals_scored(df)
        .sort_values(
            ascending=False
        )
    )

    top_team = team_goals.index[0]

    top_team_goals = int(
        team_goals.iloc[0]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="insight">

            <b>🏠 Home Advantage</b>

            <br>

            Home teams win
            <b>{home_win_pct:.1f}%</b>
            of matches.

            </div>

            <div class="insight">

            <b>⚽ Highest Goal Output</b>

            <br>

            <b>{top_team}</b>
            scored the most goals in
            the selected dataset:
            <b>{top_team_goals:,}</b>.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="insight">

            <b>🔥 Highest-Scoring Season</b>

            <br>

            <b>{int(peak["Season"])}</b>
            had 
            <b>{int(peak["Goals"]):,}</b>
            goals.

            </div>

            <div class="insight">

            <b>📊 Total Dataset</b>

            <br>

            <b>{n_matches:,}</b>
            matches across
            <b>{n_seasons}</b>
            seasons.

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TAB 2 — MATCH OUTCOMES
# ============================================================

with tab_outcomes:

    st.subheader(
        "🏠 Home vs Away Performance"
    )


    # --------------------------------------------------------
    # HOME WIN PERCENTAGE BY SEASON
    # --------------------------------------------------------

    matches_per_season = (
        df.groupby("season")
        .size()
    )

    home_wins_per_season = (
        df[df["result"] == "H"]
        .groupby("season")
        .size()
    )

    home_win_by_season = (
        home_wins_per_season
        .mul(100)
        .div(matches_per_season)
        .fillna(0)
        .reset_index()
    )

    home_win_by_season.columns = [
        "Season",
        "Home Win %"
    ]

    home_win_by_season["Home Win %"] = (
        home_win_by_season["Home Win %"]
        .round(2)
    )


    fig = px.bar(
        home_win_by_season,
        x="Season",
        y="Home Win %",
        text="Home Win %",
        title="Home Win Percentage by Season"
    )

    st.plotly_chart(
        style_fig(fig),
        use_container_width=True
    )


    # --------------------------------------------------------
    # RESULT PIE
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        pie = px.pie(
            outcome_df,
            names="Outcome",
            values="Matches",
            hole=0.45,
            title="Overall Result Mix"
        )

        st.plotly_chart(
            style_fig(pie, 400),
            use_container_width=True
        )


    # --------------------------------------------------------
    # HOME VS AWAY GOALS
    # --------------------------------------------------------

    with col2:

        side_goals = pd.DataFrame(
            {
                "Side": [
                    "Home",
                    "Away"
                ],

                "Goals": [
                    int(
                        df["home_goals"].sum()
                    ),
                    int(
                        df["away_goals"].sum()
                    )
                ]
            }
        )

        fig = px.bar(
            side_goals,
            x="Side",
            y="Goals",
            color="Side",
            text_auto=True,
            title="Home vs Away Goals"
        )

        st.plotly_chart(
            style_fig(fig, 400),
            use_container_width=True
        )


    # --------------------------------------------------------
    # HOME VS AWAY SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "Home vs Away Summary"
    )

    comparison = pd.DataFrame(
        {
            "Metric": [
                "Wins",
                "Win Percentage",
                "Goals"
            ],

            "Home": [
                home_wins,
                round(home_win_pct, 2),
                int(
                    df["home_goals"].sum()
                )
            ],

            "Away": [
                away_wins,
                round(away_win_pct, 2),
                int(
                    df["away_goals"].sum()
                )
            ]
        }
    )

    st.dataframe(
        comparison,
        hide_index=True,
        use_container_width=True
    )


# ============================================================
# TAB 3 — TEAM PERFORMANCE
# ============================================================

with tab_teams:

    st.subheader(
        "🏆 Team Performance"
    )


    # ========================================================
    # BUILD TEAM STATISTICS
    # ========================================================

    matches = team_matches(df)

    wins = team_wins(df)

    draws_team = team_draws(df)

    losses = team_losses(df)

    goals_for = team_goals_scored(df)

    goals_against = team_goals_conceded(df)


    team_stats = pd.DataFrame(
        {
            "Matches": matches,
            "Wins": wins,
            "Draws": draws_team,
            "Losses": losses,
            "Goals Scored": goals_for,
            "Goals Conceded": goals_against
        }
    ).fillna(0)


    team_stats["Goal Difference"] = (
        team_stats["Goals Scored"] -
        team_stats["Goals Conceded"]
    )

    team_stats["Win %"] = (
        team_stats["Wins"] /
        team_stats["Matches"] *
        100
    )

    team_stats["Win %"] = (
        team_stats["Win %"]
        .fillna(0)
        .round(2)
    )


    # ========================================================
    # TOP 10 TEAMS
    # ========================================================

    st.markdown(
        "### 🥇 Top 10 Teams by Total Wins"
    )

    top10 = (
        team_stats
        .sort_values(
            by=[
                "Wins",
                "Goal Difference",
                "Goals Scored"
            ],
            ascending=False
        )
        .head(10)
        .copy()
    )

    top10.insert(
        0,
        "Team",
        top10.index
    )

    top10 = top10.reset_index(drop=True)


    # --------------------------------------------------------
    # TOP 10 TABLE
    # --------------------------------------------------------

    st.dataframe(
        top10[
            [
                "Team",
                "Matches",
                "Wins",
                "Draws",
                "Losses",
                "Goals Scored",
                "Goals Conceded",
                "Goal Difference",
                "Win %"
            ]
        ],
        hide_index=True,
        use_container_width=True
    )


    # ========================================================
    # TOP 10 WINS CHART
    # ========================================================

    fig = px.bar(
        top10.sort_values(
            "Wins",
            ascending=True
        ),
        x="Wins",
        y="Team",
        orientation="h",
        text="Wins",
        title="Top 10 Teams by Total Wins"
    )

    st.plotly_chart(
        style_fig(fig, 450),
        use_container_width=True
    )


    # ========================================================
    # TOP 10 GOALS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        top_goals = (
            team_stats
            .sort_values(
                "Goals Scored",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        top_goals.columns = [
            "Team",
            "Matches",
            "Wins",
            "Draws",
            "Losses",
            "Goals Scored",
            "Goals Conceded",
            "Goal Difference",
            "Win %"
        ]

        fig = px.bar(
            top_goals.sort_values(
                "Goals Scored",
                ascending=True
            ),
            x="Goals Scored",
            y="Team",
            orientation="h",
            text="Goals Scored",
            title="Top 10 Teams by Goals Scored"
        )

        st.plotly_chart(
            style_fig(fig),
            use_container_width=True
        )


    # ========================================================
    # TOP 10 WIN %
    # ========================================================

    with col2:

        eligible = (
            team_stats[
                team_stats["Matches"] >= min_matches
            ]
            .sort_values(
                "Win %",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        eligible.columns = [
            "Team",
            "Matches",
            "Wins",
            "Draws",
            "Losses",
            "Goals Scored",
            "Goals Conceded",
            "Goal Difference",
            "Win %"
        ]

        fig = px.bar(
            eligible.sort_values(
                "Win %",
                ascending=True
            ),
            x="Win %",
            y="Team",
            orientation="h",
            text="Win %",
            title=f"Top 10 Win % (Minimum {min_matches} Matches)"
        )

        st.plotly_chart(
            style_fig(fig),
            use_container_width=True
        )



# ========================================================
# TEAM SEARCH
# ========================================================

st.markdown("---")

st.markdown(
    "### 🔎 Search Team"
)

st.caption(
    "Type a team name and select the club from the matching results."
)

# --------------------------------------------------------
# SEARCH BOX
# --------------------------------------------------------

selected_team = st.selectbox(
    "Search",
    sorted(team_stats.index.to_list()),
    index=None,
    placeholder="Type to search for a club..."
)


# --------------------------------------------------------
# FIND MATCHING CLUBS
# --------------------------------------------------------


# --------------------------------------------------------
# CLUB DROPDOWN
# --------------------------------------------------------

if selected_team is not None:

    stats = team_stats.loc[selected_team]

    # ====================================================
    # SELECTED TEAM STATISTICS
    # ====================================================


    # ----------------------------------------------------
    # TEAM HEADER
    # ----------------------------------------------------

    st.markdown(
        f"""
<div class="team-card">
    <h2>⚽ {selected_team}</h2>
    <p>
        Complete performance across the selected seasons.
    </p>
</div>
""",
        unsafe_allow_html=True
    )


    # ----------------------------------------------------
    # TEAM KPIs
    # ----------------------------------------------------

    t1, t2, t3, t4, t5, t6 = st.columns(6)

    t1.metric(
        "Matches",
        int(stats["Matches"])
    )

    t2.metric(
        "Wins",
        int(stats["Wins"])
    )

    t3.metric(
        "Draws",
        int(stats["Draws"])
    )

    t4.metric(
        "Losses",
        int(stats["Losses"])
    )

    t5.metric(
        "Win %",
        f"{stats['Win %']:.2f}%"
    )

    t6.metric(
        "Goal Difference",
        int(stats["Goal Difference"])
    )


    # ----------------------------------------------------
    # GOALS
    # ----------------------------------------------------

    g1, g2 = st.columns(2)

    with g1:

        st.metric(
            "Goals Scored",
            int(stats["Goals Scored"])
        )

    with g2:

        st.metric(
            "Goals Conceded",
            int(stats["Goals Conceded"])
        )


    # ----------------------------------------------------
    # TEAM RESULT DISTRIBUTION
    # ----------------------------------------------------

    team_result_df = pd.DataFrame(
        {
            "Result": [
                "Wins",
                "Draws",
                "Losses"
            ],

            "Matches": [
                int(stats["Wins"]),
                int(stats["Draws"]),
                int(stats["Losses"])
            ]
        }
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            team_result_df,
            x="Result",
            y="Matches",
            color="Result",
            text_auto=True,
            title=f"{selected_team} — Results"
        )

        st.plotly_chart(
            style_fig(fig, 380),
            use_container_width=True
        )


    # ----------------------------------------------------
    # TEAM GOALS
    # ----------------------------------------------------

    with col2:

        goal_df = pd.DataFrame(
            {
                "Metric": [
                    "Goals Scored",
                    "Goals Conceded"
                ],

                "Goals": [
                    int(stats["Goals Scored"]),
                    int(stats["Goals Conceded"])
                ]
            }
        )


        fig = px.bar(
            goal_df,
            x="Metric",
            y="Goals",
            color="Metric",
            text_auto=True,
            title=f"{selected_team} — Goal Record"
        )

        st.plotly_chart(
            style_fig(fig, 380),
            use_container_width=True
        )


    # ----------------------------------------------------
    # TEAM MATCH HISTORY
    # ----------------------------------------------------

    st.markdown(
        "### 📋 Match History"
    )

    team_matches_df = df[
        (df["home_team"] == selected_team)
        |
        (df["away_team"] == selected_team)
    ].copy()


    # Remove exact duplicate match records
    team_matches_df = (
        team_matches_df
        .drop_duplicates(
            subset=[
                "season",
                "home_team",
                "away_team",
                "home_goals",
                "away_goals",
                "result"
            ]
        )
        .sort_values(
            "season",
            ascending=False
        )
    )


    # ----------------------------------------------------
    # TEAM RESULT
    # ----------------------------------------------------

    def get_team_result(row):

        if row["home_team"] == selected_team:

            if row["result"] == "H":
                return "Win"

            elif row["result"] == "D":
                return "Draw"

            else:
                return "Loss"

        else:

            if row["result"] == "A":
                return "Win"

            elif row["result"] == "D":
                return "Draw"

            else:
                return "Loss"


    team_matches_df["Team Result"] = (
        team_matches_df.apply(
            get_team_result,
            axis=1
        )
    )


    st.dataframe(
        team_matches_df[
            [
                "season",
                "home_team",
                "home_goals",
                "away_goals",
                "away_team",
                "Team Result"
            ]
        ],
        hide_index=True,
        use_container_width=True,
        height=400
    )


# --------------------------------------------------------
# NO MATCHING TEAM
# --------------------------------------------------------

else:

    st.info(
        "👆 Start typing a team name to search for a club."
    )





# ============================================================
# TAB 4 — GOAL TRENDS
# ============================================================

with tab_goals:

    st.subheader(
        "⚽ Goal Analysis"
    )


    # --------------------------------------------------------
    # GOALS PER SEASON
    # --------------------------------------------------------

    goals_per_season = (
        df.groupby("season")["total_goals"]
        .sum()
        .reset_index()
    )

    goals_per_season.columns = [
        "Season",
        "Goals"
    ]


    fig = px.line(
        goals_per_season,
        x="Season",
        y="Goals",
        markers=True,
        title="Total Goals per Season"
    )

    fig.update_traces(
        line_color=UCL_BLUE,
        marker_color=UCL_GOLD
    )

    st.plotly_chart(
        style_fig(fig),
        use_container_width=True
    )


    # --------------------------------------------------------
    # AVERAGE GOALS PER MATCH
    # --------------------------------------------------------

    avg_goals_season = (
        df.groupby("season")
        .agg(
            Matches=("season", "size"),
            Goals=("total_goals", "sum")
        )
        .reset_index()
    )


    avg_goals_season["Average Goals"] = (
        avg_goals_season["Goals"] /
        avg_goals_season["Matches"]
    ).round(2)


    fig = px.line(
        avg_goals_season,
        x="season",
        y="Average Goals",
        markers=True,
        title="Average Goals per Match by Season"
    )

    st.plotly_chart(
        style_fig(fig),
        use_container_width=True
    )


    # --------------------------------------------------------
    # HOME VS AWAY GOALS BY SEASON
    # --------------------------------------------------------

    home_away_goals = (
        df.groupby("season")[
            [
                "home_goals",
                "away_goals"
            ]
        ]
        .sum()
        .reset_index()
    )


    home_away_goals = (
        home_away_goals.rename(
            columns={
                "season": "Season",
                "home_goals": "Home",
                "away_goals": "Away"
            }
        )
    )


    melted = home_away_goals.melt(
        id_vars="Season",
        var_name="Side",
        value_name="Goals"
    )


    fig = px.bar(
        melted,
        x="Season",
        y="Goals",
        color="Side",
        barmode="group",
        title="Home vs Away Goals by Season"
    )


    st.plotly_chart(
        style_fig(fig),
        use_container_width=True
    )


    # --------------------------------------------------------
    # GOAL DISTRIBUTION
    # --------------------------------------------------------

    st.subheader(
        "Goal Distribution per Match"
    )


    goal_distribution = (
        df["total_goals"]
        .value_counts()
        .sort_index()
        .reset_index()
    )


    goal_distribution.columns = [
        "Goals",
        "Matches"
    ]


    fig = px.bar(
        goal_distribution,
        x="Goals",
        y="Matches",
        text_auto=True,
        title="Number of Matches by Total Goals"
    )


    st.plotly_chart(
        style_fig(fig),
        use_container_width=True
    )


    # --------------------------------------------------------
    # HIGHEST SCORING SEASON
    # --------------------------------------------------------

    highest = (
        goals_per_season
        .loc[
            goals_per_season["Goals"].idxmax()
        ]
    )


    st.success(
        f"🔥 Highest-scoring season: "
        f"**{int(highest['Season'])}** "
        f"with **{int(highest['Goals']):,} goals**."
    )


# ============================================================
# TAB 5 — HIGH SCORING GAMES
# ============================================================

with tab_high:

    st.subheader(
        "🔥 High-Scoring Matches"
    )


    threshold = st.slider(
        "Minimum total goals",
        min_value=3,
        max_value=10,
        value=5
    )


    high = (
        df[
            df["total_goals"] >= threshold
        ]
        .sort_values(
            "total_goals",
            ascending=False
        )
    )


    st.metric(
        f"Matches with {threshold}+ goals",
        len(high)
    )


    st.dataframe(
        high[
            [
                "season",
                "home_team",
                "home_goals",
                "away_goals",
                "away_team",
                "result",
                "total_goals"
            ]
        ],
        hide_index=True,
        use_container_width=True,
        height=350
    )


    # --------------------------------------------------------
    # TEAMS SCORING 5+
    # --------------------------------------------------------

    home_high = (
        df[
            df["home_goals"] >= 5
        ]
        .groupby("home_team")
        .size()
    )


    away_high = (
        df[
            df["away_goals"] >= 5
        ]
        .groupby("away_team")
        .size()
    )


    most_high_scoring = (
        home_high
        .add(
            away_high,
            fill_value=0
        )
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )


    most_high_scoring.columns = [
        "Team",
        "5+ Goal Matches"
    ]


    fig = px.bar(
        most_high_scoring.sort_values(
            "5+ Goal Matches",
            ascending=True
        ),
        x="5+ Goal Matches",
        y="Team",
        orientation="h",
        text="5+ Goal Matches",
        title="Teams Scoring 5+ Goals Most Often"
    )


    st.plotly_chart(
        style_fig(fig, 450),
        use_container_width=True
    )


# ============================================================
# TAB 6 — MATCH EXPLORER
# ============================================================

with tab_data:

    st.subheader(
        "🔎 Match Explorer"
    )


    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        explorer_team = st.selectbox(
            "Club",
            [
                "All Clubs"
            ]
            +
            sorted(
                unique_teams(df).tolist()
            )
        )


    with col2:

        explorer_result = st.selectbox(
            "Result",
            [
                "All Results",
                "Home Win",
                "Away Win",
                "Draw"
            ]
        )


    with col3:

        explorer_season = st.selectbox(
            "Season",
            [
                "All Seasons"
            ]
            +
            sorted(
                df["season"]
                .unique()
                .tolist()
            )
        )


    view = df.copy()


    # Team filter

    if explorer_team != "All Clubs":

        view = view[
            (
                view["home_team"]
                == explorer_team
            )
            |
            (
                view["away_team"]
                == explorer_team
            )
        ]


    # Result filter

    if explorer_result == "Home Win":

        view = view[
            view["result"] == "H"
        ]

    elif explorer_result == "Away Win":

        view = view[
            view["result"] == "A"
        ]

    elif explorer_result == "Draw":

        view = view[
            view["result"] == "D"
        ]


    # Season filter

    if explorer_season != "All Seasons":

        view = view[
            view["season"]
            == explorer_season
        ]


    st.caption(
        f"{len(view):,} matches found"
    )


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    st.dataframe(
        view[
            [
                "season",
                "home_team",
                "home_goals",
                "away_goals",
                "away_team",
                "result",
                "total_goals"
            ]
        ]
        .sort_values(
            [
                "season",
                "home_team"
            ]
        ),
        hide_index=True,
        use_container_width=True,
        height=500
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Source: ucl.csv • UEFA Champions League Historical Match Analysis • No Machine Learning"
)
