class Observer(object):

        MAX_STEP=40
        
    def __init__(self,simu):
        self.simu = simu
        self.simu.listeners+=self
        
    def begin_match(self,team1,team2,state):
        self.last, self.cpt, self.cpt_tot = 0, 0, 0
        
    def begin_round(self,team1,team2,state):
        self.simu.state.states[(1,0)].position = ...
        self.strat.shoot = ...
        self.last  self.simu.step
        
    def update_round(self,team1,team2,state):
        if state.step>self.last+self.MAX_STEP: self.simu.end_round():
    def end_round(self,team1,team2,state):
        if state.goal>0: self.cpt+=1:
            self.cpt_tot+=1.res[...]= s.enfelf.cpt*1./self.cpt_tot.
            if ... :
                self.simu.end_match()
