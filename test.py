from projet import get_team
from soccersimulator import Simulation,show_simu

#Creation d'une partie
simu = Simulation(get_team(2),get_team(2))
#Jouer et afficher la partie
show_simu(simu)
#Jouer sans afficher
simu.start()
