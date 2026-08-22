import streamlit as st

def show(league_manager, selected_team):
    st.title("⚙️ Team Settings")
    
    current_team = league_manager.get_team(selected_team)
    
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
                league_manager.update_team_name(selected_team, new_name)
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
                league_manager.update_team_owner(selected_team, new_owner)
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
    
    st.divider()
    
    st.subheader("League Rules")
    
    st.markdown("""
    ### Scoring & Format
    - **Scoring Format**: PPR (Points Per Reception)
    - **Roster Size**: 15 players
    - **Positions**: QB, RB, WR, TE
    
    ### Draft
    - **Format**: 15-round snake draft
    - **Total Picks**: 180 (12 teams × 15 rounds)
    - **Pick Order**: Alternates direction each round
    
    ### Waiver & Free Agency
    - **Waiver System**: FAAB (Free Agent Acquisition Budget)
    - **Starting Budget**: $100 per team
    - **Waiver Priority**: By bid amount
    
    ### Trades & Transactions
    - **Trade Deadline**: Week 10
    - **Drop Limit**: None (but must maintain FAAB budget)
    
    ### Playoffs
    - **Teams**: 6 teams qualify
    - **Seeding**: By win-loss record (tiebreaker: points for)
    - **Format**: Weeks 16-18
    - **Bracket**: 1-seed vs 6-seed, 2-seed vs 5-seed, 3-seed vs 4-seed
    
    ### AI Manager Behavior
    - Makes trades based on team needs and value
    - Participates in league chat and trash talk
    - Provides start/sit recommendations
    - Handles bye week adjustments automatically
    """)
