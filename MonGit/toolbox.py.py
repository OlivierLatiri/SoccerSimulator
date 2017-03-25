import math
from soccersimulator import SoccerAction, SoccerState, PlayerState
from soccersimulator import Vector2D
from soccersimulator.settings import GAME_HEIGHT, GAME_WIDTH, PLAYER_RADIUS, BALL_RADIUS
import random



RAYON_DES_CAGES = 30
#temps_de_shoot = 0

def cont2discret(x,y,size):
	# 0 -> GAME_WIDTH, 0 -> GAME_HEIGHT
	stepx = GAME_WIDTH*1./size
	stepy = GAME_HEIGHT*1./size
	return int(x/stepx)+ int(y/stepy)*size
	#return Vector2D(int(x/stepx)*size + stepx/2, int(y/stepy)*size + stepy/2)
	

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
		if ( self.dist_ball() ).norm >= PLAYER_RADIUS + BALL_RADIUS:
			return False
		return True

	def coequipier_position(self, p):
		return p.my_position 
        
	def temps_shoot(self):
		temps_de_shoot = self.state.step
		return temps_de_shoot
        
class Zone (object):
	def __init__(self,mystate):
		self.MyState = mystate    
           
    
	def attaque_zone(self):
		if (self.key[0]==2):
			if (self.state.ball.position.x < 30 and self.state.ball.position.y < 70 and self.state.ball.position.y > 20):
 				return True
			return False
		if (self.key[0]==1):
			if (self.state.ball.position.x > GAME_WIDTH-30 and self.state.ball.position.y < 70 and self.state.ball.position.y > 20):
				return True        
			return False
	
	def zone_tire_faible(self):
		x=cont2discret(self.my_position().x,self.my_position().y,10)
		if (self.key[0]==1):
			if x in [29, 39, 49, 59, 69, 79]:
				return True
			else: return False
		if (self.key[0]==2):
			if x in [20, 30, 40, 50, 60, 70] :
				return True
			else: return False
			
	def zone_tire_moyen(self):
		X=cont2discret(self.my_position().x,self.my_position().y,10)
		if (self.key[0]==1):
			if X in [28, 37, 38, 47, 48, 57, 58, 67, 68, 78]:
				return True
			else: return False		
		if (self.key[0]==2):
			if X in [21, 31, 32, 41, 42, 51, 52, 61, 62, 71]:
				return True
			else: return False
			
	def zone_autre(self):
		if (self.key[0]==1):
			if zone_tire_moyen == False and zone_tire_faible == False :
				return True
			return False
		if (self.key[0]==1):
			if zone_tire_moyen == False and zone_tire_faible == False :
				return True
			return False
				
	
	
   	 #def mini_zone(self,p):
		
                
	def ball_zone(self):
		if (self.state.player_state(self.key[0], self.key[1]).position.x< self.state.ball.position.x+10 and
        self.state.player_state(self.key[0], self.key[1]).position.x> self.state.ball.position.x-10 and 
        self.state.player_state(self.key[0], self.key[1]).position.y< self.state.ball.position.y+10 and
        self.state.player_state(self.key[0], self.key[1]).position.y> self.state.ball.position.y-10 ):

			return True 
		return False
        
	def cases(self,nucase):
		k=1
		while(k<=10):
			if (nucase>=1+(k-1)*10 and nucase<=k*10):
				j=k
			k+=1
		k=1
		while (k<=10):
			if ((nucase-k)%10==0):
				i=k
			k+=1
		if (self.state.player_state(self.key[0],self.key[1]).position.x<15*i and
		self.state.player_state(self.key[0],self.key[1]).position.x>=15(i-1) and
		self.state.player_state(self.key[0],self.key[1]).position.y<9*j and
		self.state.player_state(self.key[0],self.key[1]).position.y>=9*(j-1)):
			return True
		return False
	
	def defense_zone(self):
		if (self.key[0]==1):
			if (self.state.ball.position.x < 40):
				return True
			return False
		if (self.key[0]==2):
			if (self.state.ball.position.x > GAME_WIDTH-40):
				return True        
			return False
            
	def __getattr__(self, name):
		return getattr(self.MyState, name)
		            

class Action(object):

	def __init__(self,zone):
		self.Zone =zone
        
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
	#differents tires :
	def tirer_max(self, p):
		return SoccerAction(Vector2D(),p-self.my_position())
        
	def tirer_max_moyen(self, p):
		return SoccerAction(Vector2D(),(p/5)-(self.my_position()/5))

	def tirer_moyen(self, p):
		return SoccerAction(Vector2D(),(p/10)-(self.my_position()/10))
        
	def tirer_moyen_faible(self, p):
 		return SoccerAction(Vector2D(),(p/12)-(self.my_position()/12))
	
	def tirer_faible(self, p):
		return SoccerAction(Vector2D(),(p/13)-(self.my_position()/13))
	
	def __getattr__(self, name):
		return getattr(self.Zone, name)
        
        
class Techniques(object):
    
	def __init__(self, action):
		self.Action = action
        
    #differentes manieres d'aller vers la balle 
    
	def aller_vers_ball_1(self, ball_position):
		return self.aller_vers(self.ball_position()+self.state.ball.vitesse)

	def aller_vers_ball_2(self, ball_position):
		return self.aller_vers(self.ball_position()+self.state.ball.vitesse*5)
        
	def aller_vers_ball_3(self, ball_position):
		return self.aller_vers(self.ball_position()+self.state.ball.vitesse*10)
        
	def aller_vers_ball_def(self, ball_position):
#        if(self.ball_zone()):
#            return self.marcher_vers(self.ball_position()+self.state.ball.vitesse*7)
		return self.aller_vers(self.ball_position()+self.state.ball.vitesse*5)


	def positionner_joueur(self,nucase):
		k=1
		while(k<=10):
			if (nucase>=1+(k-1)*10 and nucase<=k*10):
				j=k
			k+=1
		k=1
		while (k<=10):
			if ((nucase-k)%10==0):
				i=k
			k+=1
			
		self.state.player_state(self.key[0], self.key[1]).position.x=random.randint(15*i,15*(i-1))
		self.state.player_state(self.key[0], self.key[1]).position.y=random.randint(9*j,9*(j-1))
		return self.my_position()
		
        
	def aller_vers_ball_att(self, ball_position):
		if(self.defense_zone() and self.state.nb_players(self.key[0])!=1):
			return self.immobile()
        #if(self.ball_zone()):
         #   return self.marcher_vers(self.ball_position())
		return self.aller_vers(self.ball_position()+self.state.ball.vitesse*5)   
    

        
	def shoot_att(self, but_position):
		if(self.peut_tirer()):
			return self.tirer_moyen(self.but_position())
		return self.aller_vers_ball_att(self.ball_position)
    
            
	def shoot_def(self, but_position):
		if(self.peut_tirer()):
			return self.tirer_vers(self.but_position())
		return self.aller_vers_ball_att(self.ball_position)
            
	def drible(self, but_position):
		if(self.peut_tirer()):            
			return self.petite_passe(self.but_position())
		return self.aller_vers_ball_att(self.ball_position)
    
	def attaque_strategy(self):
		if(self.attaque_zone()):
			return self.shoot_att(self.but_position())
		return self.drible(self.but_position())
	
	def tirer(self):
		if self.zone_tire_faible():
			return self.tirer_moyen_faible(self.but_position())
		elif self.zone_tire_moyen():
			return self.tirer_moyen(self.but_position())
		else: 
			return self.drible(self.but_position())
            
	def defense_position(self):
		if(self.key[0]==1):
			if(self.defense_zone()):
				return self.aller_vers_ball_def(self.ball_position()) + self.shoot_def(self.but_position())                
			else:
				return self.aller_vers(Vector2D(30,self.state.ball.position.y)) 
		else:
			if(self.defense_zone()):
				return self.aller_vers_ball_def(self.ball_position()) + self.shoot_def(self.but_position())              
			else:
				return self.aller_vers(Vector2D(GAME_WIDTH-30,self.state.ball.position.y))

	def __getattr__(self, name):
return getattr(self.Action, name
