from soccersimulator.mdpsoccer import SoccerAction
from soccersimulator.utils import Vector2D
from soccersimulator.settings import GAME_HEIGHT, GAME_WIDTH, PLAYER_RADIUS, BALL_RADIUS

RAYON_DES_CAGES = 30

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
        
    def defense_zone(self):
        if (self.key[0]==1):
            if (self.state.ball.position.x < 30 and self.state.ball.position.y < 65 and self.state.ball.position.y > 25):
                return True
            return False
        if (self.key[0]==2):
            if (self.state.ball.position.x > GAME_WIDTH-30 and self.state.ball.position.y < 65 and self.state.ball.position.y > 25):
                return True        
            return False
    
    def coequipier_position(self, p):
        return p.my_position 
            

class Action(object):
    def __init__(self,mystate):
        self.MyState = mystate
        
    def aller_vers(self, p):
        return SoccerAction(p-self.my_position(),Vector2D())
        
    def immobile(self):
        return SoccerAction(Vector2D(), Vector2D())
        
    def marcher(self, p):
        return SoccerAction((p-self.my_position())/2,Vector2D())
        
    def tirer_vers(self,p):
        return SoccerAction(Vector2D(),p-self.my_position())
        
    def passe(self):
        return SoccerAction(Vector2D(), (self.coequipier_position()-self.state.my_position())/2)

            
    def __getattr__(self, name):
        return getattr(self.MyState, name)
        
        
class Techniques(object):
    
    def __init__(self, action):
        self.Action = action
    
    def aller_vers_ball_def(self, ball_position):
        return self.aller_vers(self.ball_position())
        
    def aller_vers_ball_att(self, ball_position):
        if(self.defense_zone()):
            return self.immobile()
        return self.aller_vers(self.ball_position())       
    
        
    def shoot(self, but_position):
        return self.tirer_vers(self.but_position())
            
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
