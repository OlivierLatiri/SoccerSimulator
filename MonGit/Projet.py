from soccersimulator.strategies  import Strategy
from soccersimulator.mdpsoccer import SoccerTeam, Simulation, SoccerAction
from soccersimulator.gui import show_state,show_simu
from soccersimulator.utils import Vector2D
from soccersimulator.settings import GAME_HEIGHT, GAME_WIDTH
import tools

class Fonceur (Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
    def compute_strategy (self, state, id_team, id_player):
        mystate = toolbox.MyState(state, id_team, id_player)
        action = toolbox.Action(mystate)
        technique = toolbox.Techniques(action)
        return technique.aller_vers_ball_att(mystate.ball_position()) + technique.shoot(mystate.ball_position())
        

class Defenseur (Strategy):
    def __init__(Self):
        Strategy.__init__(Self, "Defenseur")
    def compute_strategy (self, state, id_team, id_player):
        mystate = toolbox.MyState(state, id_team, id_player)
        action = toolbox.Action(mystate)
        technique = toolbox.Techniques(action)
        return technique.defense_position()
            
            
if __name__ == "__main__":
    ## Creation d'une equipe
    team1 = SoccerTeam(name="team1",login="etu1")
    team2 = SoccerTeam(name="team2",login="etu2")
    team1.add("John",Fonceur()) 
    team1.add("Yasmine",Defenseur())
    team2.add("Paul",Fonceur())  
    team2.add("Olivier",Defenseur())

    #Creation d'une partie
    simu = Simulation(team1,team2)
    #Jouer et afficher la partie
    show_simu(simu)
    #Jouer sans afficher
    simu.start()
