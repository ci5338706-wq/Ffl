import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fantasy Football League",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.user_teams = []
    st.session_state.selected_team = None
    
    # Initialize teams
    st.session_state.teams = []
    ai_personalities = ["elite_qb", "elite_te", "elite_rb", "sleeper_hunter", "balanced"]
    default_names = [
        "Mahomes' Madness", "Josh's Legends", "Lamar's Lightning",
        "Patrick's Picks", "Buffalo Bills Gang", "Philly Eagles",
        "KC Chiefs Nation", "Ravens Revenge", "Cincinnati Bengals",
        "Miami Dolphins", "New York Giants", "San Francisco 49ers"
    ]
    
    for i in range(12):
        st.session_state.teams.append({
            "id": i,
            "name": default_names[i],
            "owner": f"Team {i+1}",
            "is_ai": random.choice([True, False]),
            "wins": 0,
            "losses": 0,
            "points_for": 0.0,
            "points_against": 0.0,
            "roster": [],
            "faab_budget": 100,
            "draft_personality": random.choice(ai_personalities),
            "trades_made": 0
        })

def get_personality_description(personality: str) -> str:
    descriptions = {
        "elite_qb": "🎯 Elite QB Hunter - Prioritizes elite quarterbacks early",
        "elite_te": "🏈 Elite TE Specialist - Invests heavily in tight end position",
        "elite_rb": "⚡ Elite RB Prioritizer - Focuses on running back depth",
        "sleeper_hunter": "🔍 Sleeper Hunter - Finds hidden gems and value picks",
        "balanced": "⚖️ Balanced - Takes best available player approach"
    }
    return descriptions.get(personality, personality)

# Sidebar
st.sidebar.title("🏈 Fantasy Football League")
st.sidebar.subheader("📋 Team Setup")

if not st.session_state.user_teams:
    st.sidebar.info("You haven't joined any teams yet!")
    if st.sidebar.button("➕ Join a Team"):
        st.session_state.show_join = True

if st.session_state.get('show_join', False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Available Teams to Join")
    
    for team in st.session_state.teams:
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.write(f"**{team['name']}** ({team['owner']})")
            if team['is_ai']:
                personality = get_personality_description(team['draft_personality'])
                st.caption(f"🤖 {personality}")
            else:
                st.caption("👤 Human-Managed")
        with col2:
            if st.button("Join", key=f"join_{team['id']}"):
                st.session_state.user_teams.append(team['id'])
                st.session_state.selected_team = team['id']
                st.session_state.show_join = False
                st.rerun()

if st.session_state.user_teams:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Your Teams")
    
    team_displays = [f"{st.session_state.teams[tid]['name']} ({st.session_state.teams[tid]['owner']})" 
                     for tid in st.session_state.user_teams]
    
    selected = st.sidebar.selectbox("Select Team", team_displays)
    st.session_state.selected_team = st.session_state.user_teams[team_displays.index(selected)]

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["🏠 Home/Standings", "⚙️ Settings"])

# Main content
if not st.session_state.user_teams:
    st.warning("⚠️ Please join a team first!")
    st.info("""
    Welcome to Fantasy Football League!
    
    👈 Click "➕ Join a Team" in the sidebar to get started!
    """)
else:
    if page == "🏠 Home/Standings":
        current_team = st.session_state.teams[st.session_state.selected_team]
        st.title("🏠 Home / Standings")
        
        # Standings table
        standings_data = []
        for i, team in enumerate(st.session_state.teams):
            standings_data.append({
                "Rank": i + 1,
                "Team": team["name"],
                "Owner": team["owner"],
                "Wins": team["wins"],
                "Losses": team["losses"],
                "PF": f"{team['points_for']:.1f}"
            })
        
        standings_df = pd.DataFrame(standings_data)
        st.subheader("League Standings")
        st.dataframe(standings_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Current team info
        st.subheader(f"📊 {current_team['name']} - Overview")
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
            **League Info**
            - League: Fantasy Football League
            - Season: 2024
            - Teams: 12
            """)
        with col2:
            status = "🤖 AI-Managed" if current_team['is_ai'] else "👤 Human-Managed"
            personality = get_personality_description(current_team['draft_personality'])
            st.success(f"""
            **Your Team**
            - Status: {status}
            - Strategy: {personality}
            - Roster: {len(current_team['roster'])} players
            """)
    
    elif page == "⚙️ Settings":
        current_team = st.session_state.teams[st.session_state.selected_team]
        st.title("⚙️ Team Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Rename Your Team")
            new_name = st.text_input("Team Name", value=current_team['name'])
            if st.button("Update Team Name"):
                if new_name and new_name != current_team['name']:
                    current_team['name'] = new_name
                    st.success(f"✅ Team renamed to {new_name}!")
                    st.rerun()
        
        with col2:
            st.markdown("### Update Owner Name")
            new_owner = st.text_input("Owner Name", value=current_team['owner'])
            if st.button("Update Owner Name"):
                if new_owner and new_owner != current_team['owner']:
                    current_team['owner'] = new_owner
                    st.success(f"✅ Owner updated to {new_owner}!")
                    st.rerun()
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            status = "🤖 AI-Managed" if current_team['is_ai'] else "👤 Human-Managed"
            st.info(f"""
            **Team Info**
            - Status: {status}
            - Record: {current_team['wins']}-{current_team['losses']}
            - Points For: {current_team['points_for']:.1f}
            """)
        with col2:
            personality = get_personality_description(current_team['draft_personality'])
            st.info(f"""
            **Strategy**
            {personality}
            
            FAAB Budget: ${current_team['faab_budget']}
            Trades Made: {current_team['trades_made']}
            """)

st.sidebar.markdown("---")
st.sidebar.markdown("*Built with Streamlit & ❤️*")
