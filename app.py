import streamlit as st
from league_manager import LeagueManager

# Page configuration
st.set_page_config(
    page_title="Fantasy Football League",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'league_manager' not in st.session_state:
    st.session_state.league_manager = LeagueManager()
    st.session_state.selected_team = 0
    st.session_state.user_teams = []

st.sidebar.title("🏈 Fantasy Football League")

league_manager = st.session_state.league_manager
teams = league_manager.get_all_teams()

# Setup: Let user join/create teams
st.sidebar.subheader("📋 Team Setup")

if not st.session_state.user_teams:
    st.sidebar.info("You haven't joined any teams yet!")
    
    if st.sidebar.button("➕ Join a Team"):
        st.session_state.show_join_modal = True

if st.session_state.get('show_join_modal', False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Available Teams to Join")
    
    for team in teams:
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.write(f"**{team['name']}** ({team['owner']})")
            if team['is_ai']:
                personality = league_manager.get_personality_description(team['draft_personality'])
                st.caption(f"🤖 {personality}")
            else:
                st.caption("👤 Human-Managed")
        with col2:
            if st.button("Join", key=f"join_{team['id']}"):
                st.session_state.user_teams.append(team['id'])
                st.session_state.selected_team = team['id']
                st.session_state.show_join_modal = False
                st.rerun()
    
    st.sidebar.markdown("---")

if st.session_state.user_teams:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Your Teams")
    
    team_displays = []
    for team_id in st.session_state.user_teams:
        team = league_manager.get_team(team_id)
        team_displays.append(f"{team['name']} ({team['owner']})")
    
    selected_team_display = st.sidebar.selectbox(
        "Select Team to Manage",
        team_displays,
        key="team_selector"
    )
    
    team_idx = st.session_state.user_teams[team_displays.index(selected_team_display)]
    st.session_state.selected_team = team_idx

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home/Standings",
        "⚙️ Settings"
    ]
)

if not st.session_state.user_teams:
    st.warning("⚠️ Please join a team first from the sidebar to get started!")
    st.info("""Welcome to Fantasy Football League!
    
    Click "➕ Join a Team" in the sidebar to:
    1. Browse all available teams
    2. See which teams are AI-managed and their draft strategies
    3. Join the team of your choice
    4. Customize your team name and owner name
    5. Start managing your fantasy team!
    """)
else:
    if page == "🏠 Home/Standings":
        current_team = league_manager.get_team(st.session_state.selected_team)
        st.title("🏠 Home / Standings")
        
        import pandas as pd
        
        standings = league_manager.get_standings()
        standings_df = pd.DataFrame(standings)
        standings_df = standings_df[["rank", "name", "owner", "wins", "losses", "points_for", "points_against"]]
        standings_df.columns = ["Rank", "Team Name", "Owner", "Wins", "Losses", "Points For", "Points Against"]
        
        st.subheader("League Standings")
        st.dataframe(standings_df, use_container_width=True, hide_index=True)
        
        st.subheader(f"📊 {current_team['name']} - Season Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Wins", current_team["wins"])
        with col2:
            st.metric("Losses", current_team["losses"])
        with col3:
            st.metric("Points For", f"{current_team['points_for']:.1f}")
        with col4:
            st.metric("FAAB Budget", f"${current_team['faab_budget']}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"""
            **League Information**
            - League: {league_manager.league_data['league_name']}
            - Season: {league_manager.league_data['season']}
            - Teams: {len(league_manager.get_all_teams())}
            """)
        
        with col2:
            status = "🤖 AI-Managed" if current_team['is_ai'] else "👤 Human-Managed"
            personality = league_manager.get_personality_description(current_team['draft_personality'])
            st.success(f"""
            **Your Team Stats**
            - Team: {current_team['name']}
            - Owner: {current_team['owner']}
            - Status: {status}
            - Strategy: {personality}
            """)
    
    elif page == "⚙️ Settings":
        current_team = league_manager.get_team(st.session_state.selected_team)
        st.title("⚙️ Team Settings")
        
        st.subheader(f"Customize {current_team['name']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Rename Your Team")
            new_name = st.text_input(
                "New Team Name",
                value=current_team['name'],
                placeholder="Enter new team name",
                label_visibility="collapsed"
            )
            
            if st.button("Update Team Name", use_container_width=True):
                if new_name and new_name != current_team['name']:
                    league_manager.update_team_name(st.session_state.selected_team, new_name)
                    st.success(f"✅ Team renamed to {new_name}!")
                    st.rerun()
                elif new_name == current_team['name']:
                    st.info("Name is already set to this value.")
                else:
                    st.warning("Please enter a valid team name.")
        
        with col2:
            st.markdown("### Update Owner Name")
            new_owner = st.text_input(
                "Owner Name",
                value=current_team['owner'],
                placeholder="Enter your name",
                label_visibility="collapsed"
            )
            
            if st.button("Update Owner Name", use_container_width=True):
                if new_owner and new_owner != current_team['owner']:
                    league_manager.update_team_owner(st.session_state.selected_team, new_owner)
                    st.success(f"✅ Owner name updated to {new_owner}!")
                    st.rerun()
                elif new_owner == current_team['owner']:
                    st.info("Owner name is already set.")
                else:
                    st.warning("Please enter a valid owner name.")
        
        st.divider()
        
        st.subheader("Team Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            status = "🤖 AI-Managed" if current_team['is_ai'] else "👤 Human-Managed"
            st.info(f"""
            **Team Status**: {status}
            **Team ID**: {current_team['id']}
            **Current Record**: {current_team['wins']}-{current_team['losses']}
            **Points For**: {current_team['points_for']:.1f}
            """)
        
        with col2:
            personality_desc = league_manager.get_personality_description(current_team['draft_personality'])
            st.info(f"""
            **Draft Strategy**: {personality_desc}
            **FAAB Budget Left**: ${current_team['faab_budget']}
            **Trades Made**: {current_team['trades_made']}
            **Roster Size**: {len(current_team['roster'])}
            """)

st.sidebar.markdown("---")
st.sidebar.markdown("*Built with Streamlit & ❤️*")
st.sidebar.markdown("*Fantasy Football League v1.0*")
