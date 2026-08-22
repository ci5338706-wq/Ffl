import json
from datetime import datetime
from typing import List, Dict, Any
import random

class LeagueManager:
    def __init__(self):
        self.league_data = {
            "league_name": "Fantasy Football League",
            "season": 2024,
            "max_teams": 12,
            "draft_round": 0,
            "draft_order": list(range(12)),
            "league_chat": [],
            "trades": [],
            "waivers": [],
        }
        self.teams = self._initialize_teams()
        self.players = self._initialize_players()
        self.schedule = self._initialize_schedule()
        self.draft_picks = []

    def _initialize_teams(self) -> List[Dict]:
        """Initialize 12 teams - all can be human or AI"""
        ai_personalities = ["elite_qb", "elite_te", "elite_rb", "sleeper_hunter", "balanced"]
        
        teams = []
        for i in range(12):
            is_ai = random.choice([True, False])
            personality = random.choice(ai_personalities)
            
            default_names = [
                "Mahomes' Madness", "Josh's Legends", "Lamar's Lightning",
                "Patrick's Picks", "Buffalo Bills Gang", "Philly Eagles",
                "KC Chiefs Nation", "Ravens Revenge", "Cincinnati Bengals",
                "Miami Dolphins", "New York Giants", "San Francisco 49ers"
            ]
            
            teams.append({
                "id": i,
                "name": default_names[i],
                "owner": f"Team {i+1}",
                "is_ai": is_ai,
                "wins": 0,
                "losses": 0,
                "points_for": 0.0,
                "points_against": 0.0,
                "roster": [],
                "bench": [],
                "faab_budget": 100,
                "trades_made": 0,
                "draft_personality": personality
            })
        
        return teams

    def _initialize_players(self) -> List[Dict]:
        """Initialize NFL players from major positions"""
        players_data = {
            "QB": [
                {"name": "Patrick Mahomes", "nfl_team": "KC", "position": "QB", "adp": 1, "projected_points": 28.5},
                {"name": "Josh Allen", "nfl_team": "BUF", "position": "QB", "adp": 2, "projected_points": 27.8},
                {"name": "Lamar Jackson", "nfl_team": "BAL", "position": "QB", "adp": 3, "projected_points": 27.2},
                {"name": "Jalen Hurts", "nfl_team": "PHI", "position": "QB", "adp": 4, "projected_points": 26.5},
                {"name": "Joe Burrow", "nfl_team": "CIN", "position": "QB", "adp": 5, "projected_points": 25.8},
                {"name": "Dak Prescott", "nfl_team": "DAL", "position": "QB", "adp": 25, "projected_points": 25.2},
                {"name": "Kirk Cousins", "nfl_team": "ATL", "position": "QB", "adp": 50, "projected_points": 24.5},
                {"name": "Tua Tagovailoa", "nfl_team": "MIA", "position": "QB", "adp": 60, "projected_points": 24.0},
            ],
            "RB": [
                {"name": "Christian McCaffrey", "nfl_team": "SF", "position": "RB", "adp": 6, "projected_points": 31.2},
                {"name": "Derrick Henry", "nfl_team": "BAL", "position": "RB", "adp": 7, "projected_points": 28.5},
                {"name": "Saquon Barkley", "nfl_team": "PHI", "position": "RB", "adp": 8, "projected_points": 27.8},
                {"name": "Josh Jacobs", "nfl_team": "LV", "position": "RB", "adp": 9, "projected_points": 24.5},
                {"name": "Tony Pollard", "nfl_team": "DAL", "position": "RB", "adp": 10, "projected_points": 23.8},
                {"name": "Ezekiel Elliott", "nfl_team": "DAL", "position": "RB", "adp": 35, "projected_points": 21.5},
                {"name": "Aaron Jones", "nfl_team": "GB", "position": "RB", "adp": 45, "projected_points": 20.8},
                {"name": "David Montgomery", "nfl_team": "CHI", "position": "RB", "adp": 55, "projected_points": 20.0},
            ],
            "WR": [
                {"name": "Tyreek Hill", "nfl_team": "MIA", "position": "WR", "adp": 11, "projected_points": 29.5},
                {"name": "Davante Adams", "nfl_team": "LV", "position": "WR", "adp": 12, "projected_points": 28.2},
                {"name": "CeeDee Lamb", "nfl_team": "DAL", "position": "WR", "adp": 13, "projected_points": 27.5},
                {"name": "Justin Jefferson", "nfl_team": "MIN", "position": "WR", "adp": 14, "projected_points": 26.8},
                {"name": "Stefon Diggs", "nfl_team": "BUF", "position": "WR", "adp": 15, "projected_points": 26.2},
                {"name": "Mike Evans", "nfl_team": "TB", "position": "WR", "adp": 40, "projected_points": 23.5},
                {"name": "Rashod Bateman", "nfl_team": "BAL", "position": "WR", "adp": 65, "projected_points": 21.0},
                {"name": "Brandon Aiyuk", "nfl_team": "SF", "position": "WR", "adp": 75, "projected_points": 20.2},
            ],
            "TE": [
                {"name": "Travis Kelce", "nfl_team": "KC", "position": "TE", "adp": 16, "projected_points": 25.5},
                {"name": "Mark Andrews", "nfl_team": "BAL", "position": "TE", "adp": 17, "projected_points": 22.8},
                {"name": "Darren Waller", "nfl_team": "NYG", "position": "TE", "adp": 18, "projected_points": 20.5},
                {"name": "Kyle Pitts", "nfl_team": "ATL", "position": "TE", "adp": 19, "projected_points": 19.8},
                {"name": "Evan Engram", "nfl_team": "JAX", "position": "TE", "adp": 20, "projected_points": 18.5},
                {"name": "Dallas Goedert", "nfl_team": "PHI", "position": "TE", "adp": 70, "projected_points": 17.2},
                {"name": "George Kittle", "nfl_team": "SF", "position": "TE", "adp": 85, "projected_points": 16.5},
                {"name": "Pat Freiermuth", "nfl_team": "PIT", "position": "TE", "adp": 95, "projected_points": 15.8},
            ]
        }
        
        players = []
        player_id = 0
        for position, player_list in players_data.items():
            for player in player_list:
                player["id"] = player_id
                player["bye_week"] = random.randint(4, 11)
                player["injury_status"] = "Healthy"
                player["drafted"] = False
                players.append(player)
                player_id += 1
        
        return players

    def _initialize_schedule(self) -> Dict:
        """Initialize 18-week schedule"""
        schedule = {}
        for week in range(1, 19):
            schedule[f"week_{week}"] = {
                "week": week,
                "matchups": [],
                "completed": False
            }
        return schedule

    def get_all_teams(self) -> List[Dict]:
        return self.teams

    def get_team(self, team_id: int) -> Dict:
        return self.teams[team_id]

    def update_team_name(self, team_id: int, new_name: str):
        if team_id < len(self.teams):
            self.teams[team_id]["name"] = new_name

    def update_team_owner(self, team_id: int, owner_name: str):
        if team_id < len(self.teams):
            self.teams[team_id]["owner"] = owner_name

    def get_standings(self) -> List[Dict]:
        standings = []
        for team in self.teams:
            standings.append({
                "rank": 0,
                "name": team["name"],
                "owner": team["owner"],
                "wins": team["wins"],
                "losses": team["losses"],
                "points_for": team["points_for"],
                "points_against": team["points_against"],
                "id": team["id"],
                "is_ai": team["is_ai"]
            })
        
        standings.sort(key=lambda x: (x["wins"], x["points_for"]), reverse=True)
        for i, team in enumerate(standings):
            team["rank"] = i + 1
        
        return standings

    def get_available_players(self) -> List[Dict]:
        return [p for p in self.players if not p["drafted"]]

    def draft_player(self, team_id: int, player_id: int):
        player = next((p for p in self.players if p["id"] == player_id), None)
        team = self.teams[team_id]
        
        if player and not player["drafted"]:
            player["drafted"] = True
            team["roster"].append(player_id)
            self.draft_picks.append({
                "team_id": team_id,
                "player_id": player_id,
                "round": len(self.draft_picks) // 12 + 1,
                "pick": len(self.draft_picks) % 12 + 1
            })

    def get_team_roster(self, team_id: int) -> List[Dict]:
        team = self.teams[team_id]
        roster = []
        for player_id in team["roster"]:
            player = next((p for p in self.players if p["id"] == player_id), None)
            if player:
                roster.append(player)
        return roster

    def add_league_chat_message(self, team_id: int, message: str):
        team = self.teams[team_id]
        self.league_data["league_chat"].append({
            "timestamp": datetime.now().isoformat(),
            "team_name": team["name"],
            "owner": team["owner"],
            "message": message,
            "team_id": team_id
        })

    def get_league_chat(self, limit: int = 50) -> List[Dict]:
        return self.league_data["league_chat"][-limit:]

    def propose_trade(self, from_team_id: int, to_team_id: int, from_players: List[int], to_players: List[int]):
        self.league_data["trades"].append({
            "id": len(self.league_data["trades"]),
            "from_team_id": from_team_id,
            "to_team_id": to_team_id,
            "from_players": from_players,
            "to_players": to_players,
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        })

    def get_available_waiver_wire(self) -> List[Dict]:
        return [p for p in self.players if not p["drafted"]]

    def submit_waiver_claim(self, team_id: int, player_id: int, bid: int):
        team = self.teams[team_id]
        if team["faab_budget"] >= bid:
            self.league_data["waivers"].append({
                "team_id": team_id,
                "player_id": player_id,
                "bid": bid,
                "timestamp": datetime.now().isoformat(),
                "status": "pending"
            })

    def get_team_matchup(self, team_id: int, week: int) -> Dict:
        opponent_id = (team_id + 1) % 12
        return {
            "week": week,
            "home_team": self.teams[team_id],
            "away_team": self.teams[opponent_id],
            "home_score": None,
            "away_score": None,
            "status": "upcoming"
        }

    def get_personality_description(self, personality: str) -> str:
        descriptions = {
            "elite_qb": "🎯 Elite QB Hunter - Prioritizes elite quarterbacks early",
            "elite_te": "🏈 Elite TE Specialist - Invests heavily in tight end position",
            "elite_rb": "⚡ Elite RB Prioritizer - Focuses on running back depth",
            "sleeper_hunter": "🔍 Sleeper Hunter - Finds hidden gems and value picks",
            "balanced": "⚖️ Balanced - Takes best available player approach"
        }
        return descriptions.get(personality, personality)
