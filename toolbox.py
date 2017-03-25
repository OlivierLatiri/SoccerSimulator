import math
from soccersimulator import SoccerAction, SoccerState, PlayerState
from soccersimulator import Vector2D
from soccersimulator.settings import GAME_HEIGHT, GAME_WIDTH, PLAYER_RADIUS, BALL_RADIUS

RAYON_DES_CAGES = 30
#temps_de_shoot = 0

class MyState(object):
    
    def __init__(self,state,idteam,idplayer):   
        self.state = state
        self.key = (idteam,idplayer)
        
    def my_position(self):
        return self.state.player_state(self.key[0], self.key[1]).position
    
    def ball_position(self):
        return self.state.ball.position
        
    def dist_ball(self):
        return self.ball_position()-self.my_position()

    def but_position(self):
        if (self.key[0]==1):
            return Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        return Vector2D(0,GAME_HEIGHT/2.)
        
    def peut_tirer(self):
        return self.state.player_state(self.key[0], self.key[1]).can_shoot()
        
    def defense_zone(self):
        if (self.key[0]==1):
            if (self.state.ball.position.x < 40 and self.state.ball.position.y < 80 and self.state.ball.position.y > 10):
                return True
            return False
        if (self.key[0]==2):
            if (self.state.ball.position.x > GAME_WIDTH-40 and self.state.ball.position.y < 80 and self.state.ball.position.y > 10):
                return True        
            return False
            
    def attaque_zone(self):
        if (self.key[0]==2):
            if (self.state.ball.position.x < 30 and self.state.ball.position.y < 70 and self.state.ball.position.y > 20):
                return True
            return False
        if (self.key[0]==1):
            if (self.state.ball.position.x > GAME_WIDTH-30 and self.state.ball.position.y < 70 and self.state.ball.position.y > 20):
                return True        
            return False
                
    def ball_zone(self):
        if (self.state.player_state(self.key[0], self.key[1]).position.x< self.state.ball.position.x+10 and
        self.state.player_state(self.key[0], self.key[1]).position.x> self.state.ball.position.x-10 and 
        self.state.player_state(self.key[0], self.key[1]).position.y< self.state.ball.position.y+10 and
        self.state.player_state(self.key[0], self.key[1]).position.y> self.state.ball.position.y-10 ):
            return True 
        return False 
    
    def coequipier_position(self, p):
        return p.my_position 
        
    def temps_shoot(self):
        temps_de_shoot = self.state.step
        return temps_de_shoot
            

class Action(object):
    def __init__(self,mystate):
        self.MyState = mystate
        
    def aller_vers(self, p):
        return SoccerAction(p-self.my_position(),Vector2D())

    def immobile(self):
        return SoccerAction(Vector2D(), Vector2D())
        
    def marcher_vers(self, p):
        return SoccerAction((p/30)-(self.my_position()/30),Vector2D())
        
    def tirer_vers(self,p):
        return SoccerAction(Vector2D(),p-self.my_position())
        
    def passe(self):
        return SoccerAction(Vector2D(), (self.coequipier_position()-self.state.my_position()))
        
    def petite_passe(self, p):
        return SoccerAction(Vector2D(),(p/50)-(self.my_position()/50))

            
    def __getattr__(self, name):
        return getattr(self.MyState, name)
        
        
class Techniques(object):
    
    def __init__(self, action):
        self.Action = action
        
    def norm(self,b,j):
        return math.sqrt(((self.state.b.x-self.state.j.x)*(self.state.b.x-self.state.j.x))+((self.state.b.y-self.state.j.y)*(self.state.b.y-self.state.j.y)))
    
    def aller_vers_ball_def(self, ball_position):
#        if(self.ball_zone()):
#            return self.marcher_vers(self.ball_position()+self.state.ball.vitesse*7)
        return self.aller_vers(self.ball_position()+self.state.ball.vitesse*7)
        
    def aller_vers_ball_att(self, ball_position):
        if(self.defense_zone() and self.state.nb_players(self.key[0])!=1):
            return self.immobile()
        #if(self.ball_zone()):
         #   return self.marcher_vers(self.ball_position())
        return self.aller_vers(self.ball_position()+self.state.ball.vitesse*7)   
    
        
    def shoot(self, but_position):
        if(self.peut_tirer()):
            return self.tirer_vers(self.but_position())
        return self.aller_vers_ball_att(self.ball_position)
            
    def drible(self, but_position):
        if(self.peut_tirer()):            
            return self.petite_passe(self.but_position())
        return self.aller_vers_ball_att(self.ball_position)
    
    def attaque_strategy(self):
        if(self.attaque_zone()):
            return self.shoot(self.but_position())
        return self.drible(self.but_position())
            
    def defense_position(self):
        if(self.key[0]==1):
            if(self.defense_zone()):
                return self.aller_vers_ball_def(self.ball_position()) + self.shoot(self.but_position())                
            else:
                return self.aller_vers(Vector2D(10,GAME_HEIGHT/2.)) 
        else:
            if(self.defense_zone()):
                return self.aller_vers_ball_def(self.ball_position()) + self.shoot(self.but_position())              
            else:
                return self.aller_vers(Vector2D(GAME_WIDTH-10,GAME_HEIGHT/2.))

                
    def __getattr__(self, name):
return getattr(self.Action, name)
