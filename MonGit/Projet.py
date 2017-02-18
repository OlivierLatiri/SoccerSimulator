from soccersimulator import Strategy
from soccersimulator import SoccerTeam, SoccerAction
import toolbox


class Fonceur (Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
    def compute_strategy (self, state, id_team, id_player):
        mystate = toolbox.MyState(state, id_team, id_player)
        action = toolbox.Action(mystate)
        technique = toolbox.Techniques(action)
        return technique.aller_vers_ball_att(mystate.ball_position()) + technique.attaque_strategy()
        

class Defenseur (Strategy):
    def __init__(Self):
        Strategy.__init__(Self, "Defenseur")
    def compute_strategy (self, state, id_team, id_player):
        mystate = toolbox.MyState(state, id_team, id_player)
        action = toolbox.Action(mystate)
        technique = toolbox.Techniques(action)
        return technique.defense_position()
            
def get_team(i):
    s=SoccerTeam(name="CityHunter")
    if (i==1):
        s.add("Mamouth",Fonceur())
    if (i==2):
        s.add("NickyLarson",Fonceur())
        s.add("Laura",Defenseur())
return s
