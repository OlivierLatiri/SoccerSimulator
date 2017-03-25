from soccersimulator import SoccerTeam, Simulation, Strategy, show_simu, Vector2D, SoccerAction
from soccersimulator.settings import GAME_HEIGHT, GAME_WIDTH
import numpy as np
import logging
import toolbox

logger = logging.getLogger("simuExpe")
"""
Controleur de simulation pour le test d'une liste de parametres
Exemple sur le tir
"""

def cont2discret(x,y,size):
	# 0 -> GAME_WIDTH, 0 -> GAME_HEIGHT
	stepx = GAME_WIDTH*1./size
	stepy = GAME_HEIGHT*1./size
	return int(x/stepx)+ int(y/stepy)*size
	#return Vector2D(int(x/stepx)*size + stepx/2, int(y/stepy)*size + stepy/2)
	
def discret2cont(no,size):
	i = no % size
	j = int(no /size)
	stepx = GAME_WIDTH*1./size
	stepy = GAME_HEIGHT*1./size
	#return i*stepx,j*stepy
	return Vector2D(i*stepx + stepx/2, j*stepy + stepy/2)
	
def limite_retion(no,size):
	i = no % size
	j = int(no /size)
	stepx = GAME_WIDTH*1./size
	stepy = GAME_HEIGHT*1./size
	return (i*stepx,  i*stepx+stepx, j*stepy, j*stepy+stepy)


class ShootSearch(object):
    """ nombre d'iterations maximales jusqu'a l'arret d'un round
        discr_step  : pas de discretisation du parametre
        nb_essais : nombre d'essais par parametre
    """
    MAX_STEP = 120
    def __init__(self):
        self.strat=ShootExpe() 
        team1 = SoccerTeam("test")
        team1.add("Expe",self.strat)
        team2 = SoccerTeam("test2")
        team2.add("Nothing",Strategy())
        self.simu = Simulation(team1,team2,max_steps=1000000)
        self.simu.listeners+=self
        self.discr_step = 20
        self.nb_essais = 1
    def start(self,visu=True):
        """ demarre la visualisation avec ou sans affichage"""
        if visu :
            show_simu(self.simu)
        else:
            self.simu.start()
    def begin_match(self,team1,team2,state):
        """ initialise le debut d'une simulation
            res : dictionnaire des Resultats
            last : step du dernier round pour calculer le round de fin avec MAX_STEP
            but : nombre de but pour ce parametre
            cpt : nombre d'essais pour ce parametre
            params : liste des parametres a tester
            idx : identifiant du parametre courant
        """
        self.res = dict()
        self.last = 0
        self.but = 0
        self.cpt = 0
        #self.params = [x for x in  np.linspace(1,settings.maxPlayerShoot,self.discr_step)]
        self.params = [0,1,2]
        self.idx=0

    def begin_round(self,team1,team2,state):
        """ engagement : position random du joueur et de la balle """ 
        iposition=5
        iposition1=43
        lxi, lxs, lyi, lys = limite_retion(iposition, 10) 
        lxi1, lxs1, lyi1, lys1 = limite_retion(iposition1, 10) 
        position = Vector2D(np.random.random()*(lxs-lxi)+lxi,
        	np.random.random()*(lys-lyi)+lyi)
        position1 = Vector2D(np.random.random()*(lxs1-lxi1)+lxi1,
        	np.random.random()*(lys1-lyi1)+lyi1)
        vitesse1= Vector2D(45,10)
        self.simu.state.states[(1,0)].position = position.copy()
        self.simu.state.states[(1,0)].vitesse = Vector2D()
        self.simu.state.ball.position = position1.copy()
        self.simu.state.ball.vitesse = vitesse1.copy()
        self.strat.istrat =self.params[self.idx]
        self.last = self.simu.step
        #self.iposition = iposition
    def update_round(self,team1,team2,state):
        """ si pas maximal atteint, fin du tour"""
        if state.step>self.last+self.MAX_STEP:
            self.simu.end_round()
    def end_round(self,team1,team2,state):
        if state.goal>0:
            self.but+=1
        self.cpt+=1
        if self.cpt>=self.nb_essais:
            self.res[self.params[self.idx]] = self.but*1./self.cpt
            logger.debug("parametre %s : %f" %((str(self.params[self.idx]),self.res[self.params[self.idx]])))
            self.idx+=1
            self.but=0
            self.cpt=0
        """ si plus de parametre, fin du match"""
        if self.idx>=len(self.params):
            self.simu.end_match()


class ShootExpe(Strategy):
    def __init__(self,shoot=None):
        self.name = "simple action"
    def compute_strategy(self,state,id_team,id_player):
        mystate = toolbox.MyState(state, id_team, id_player)
        zone = toolbox.Zone(mystate)
        action = toolbox.Action(zone)
        technique=toolbox.Techniques(action)
        if self.istrat == 0:
            return technique.aller_vers_ball_1(mystate.ball_position())+action.tirer_moyen(mystate.but_position())
        elif self.istrat == 1:
            return technique.aller_vers_ball_2(mystate.ball_position())+action.tirer_moyen(mystate.but_position())
        else:
            return technique.aller_vers_ball_3(mystate.ball_position())+action.tirer_moyen(mystate.but_position())
        

expe = ShootSearch()
expe.start()
#print(expe.res)
