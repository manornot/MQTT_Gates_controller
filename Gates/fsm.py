class gates_FSM:
       
    def __init__(self):
        #self.stt_mthd()
        self.motorM1 = 0 # -1 - closing, 0 - stoped, 1 - opening
        self.motorM2 = 0 # -1 - closing, 0 - stoped, 1 - opening
        self.limit_switchL1 = 0 # 1 - The gates are open, 0 - not open
        self.limit_switchL2 = 0 # 1 - The gates are closed, 0 - not closed
        self.states = ['stop','close','opening','open','closing','unknown']
        self.transitions = [self.stop_state,
                            self.close_state,
                            self.opening_state,
                            self.open_state,
                            self.closing_state,
                            self.unknown_state]
        self.state = self.states[-1]
        self.msg = ''
        self.prev_state = self.states[-1]
        
    def transition(self,read_pins):
        self.check_pins(read_pins)
        logic = 0
        return self.transitions[logic]
    
    def all_states(self):
        return self.transitions()
    
    def unknown_state(self,read_pins): #state - -1
        self.msg = ''
        self.check_pins(read_pins)
        if self.motorM1 == self.motorM2:
            if self.motorM1 == 1:
                logic = 2
            elif self.motorM1 == -1:
                logic = 4
            else:
                logic = 0
        else:
            logic = -1
            self.msg = 'Motor Error'
        if self.limit_switchL1 == 1 and self.limit_switchL2 == 1:
            logic = -1
            self.msg = 'Limit Switch Error'
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def stop_state(self,read_pins): #state - 0
        self.check_pins(read_pins)
        self.msg = ''
        if self.motorM1 != self.motorM2:
            logic = -1
            self.msg = 'Motor Error'
        
        elif self.motorM1 == 0 and self.limit_switchL2 == 1 and self.limit_switchL1 == 0:
            logic = 1
        elif self.motorM1 == 0 and self.limit_switchL1 == 1 and self.limit_switchL2 == 0:
            logic = 3
        
        elif self.motorM1 == 0 and self.limit_switchL1 == 1 and self.limit_switchL2 == 1:
            logic = 0
            self.msg = 'Limit switch error'
            self.state = self.states[logic]
            return self.transitions[logic]
        
        elif self.motorM1 == 0 and self.limit_switchL1 == 0 and self.limit_switchL2 == 0:
            logic = 0
        elif self.motorM1 == 1:
            self.prev_state = self.states[0]
            logic = 2
        elif self.motorM1 == -1:
            self.prev_state = self.states[0]
            logic = 4
        else:
            logic = -1
            self.msg = 'i have no fucking idea what is going on!'
            self.state = self.states[logic]
            return self.transitions[logic]
        
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def close_state(self,read_pins): #state - 1
        #could possibly return 3 states: logic = 1, logic = 2, logic = -1
        self.check_pins(read_pins)
        self.msg = ''
        if self.motorM1 != self.motorM2:
            logic = -1
            self.msg = 'Motor Error'
            return self.transitions[logic]
        elif self.motorM1 < 0:
            logic = -1
            self.msg = 'Gates are closed, but motors are active'
            return self.transitions[logic]
        elif self.motorM1 == 0 and self.limit_switchL2 == 1:
            logic = 1
        elif self.motorM1 == 1:
            if self.limit_switchL2 == 0:
                self.msg = 'opening started'
            else:
                self.msg = 'opening'
            logic = 2
        else:
            logic = -1
            self.msg = 'i have no fucking idea what is going on!'
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def opening_state(self,read_pins): #state - 2
        self.check_pins(read_pins)
        self.msg = ''
        if self.motorM1 != self.motorM2:
            logic = -1
            self.msg = 'Motor Error'
            return self.transitions[logic]
        
        elif self.motorM1 < 0:
            logic = -1
            self.msg = 'Gates are closing'
            return self.transitions[logic]
        
        elif self.motorM1 == 0 and self.limit_switchL2 == 1:
            self.prev_state = self.states[2]
            logic = 3
            
        elif self.motorM1 == 1:
            if self.limit_switchL2 == 0:
                self.msg = 'opening'
                logic = 2
            else:
                self.msg = 'open'
                self.prev_state = self.states[2]
                logic = 3
                
        elif self.motorM1 == 0 and self.limit_switchL1 == 0 and self.limit_switchL2 == 0:
            self.prev_state = self.states[2]
            logic = 0
            
        else:
            logic = -1
            self.msg = 'i have no fucking idea what is going on!'
        
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def open_state(self,read_pins): #state - 3
        self.check_pins(read_pins)
        self.msg = ''
        if self.motorM1 != self.motorM2:
            logic = -1
            self.msg = 'Motor Error'
            return self.transitions[logic]
        
        elif self.motorM1 > 0:
            logic = -1
            self.msg = 'Gates are open, but motors are active'
            return self.transitions[logic]
        
        elif self.motorM1 == 0 and self.limit_switchL1 == 1:
            logic = 3
            
        elif self.motorM1 == -1:
            if self.limit_switchL1 == 1:
                self.msg = 'closing started'
            else:
                self.msg = 'closing'
            self.prev_state = self.states[3]
            logic = 4
         
        else:
            logic = -1
            self.msg = 'i have no fucking idea what is going on!'
        
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def closing_state(self,read_pins): #state - 4
        self.check_pins(read_pins)
        self.msg = ''
        if self.motorM1 != self.motorM2:
            logic = -1
            self.msg = 'Motor Error'
            return self.transitions[logic]
        
        elif self.motorM1 > 0:
            logic = -1
            self.msg = 'Gates are opening?'
            return self.transitions[logic]
        
        elif self.motorM1 == 0 and self.limit_switchL2 == 1:
            self.prev_state = self.states[3]
            logic = 1
        elif self.motorM1 == -1:
            if self.limit_switchL2 == 0:
                self.msg = 'closing'
                logic = 4
            else:
                self.msg = 'close'
                logic = 1
                self.prev_state = self.states[4]
            
        elif self.motorM1 == 0 and self.limit_switchL1 == 0 and self.limit_switchL2 == 0:
            self.prev_state = self.states[4]
            logic = 0
        else:
            logic = -1
            self.msg = 'i have no fucking idea what is going on!'
        
        self.state = self.states[logic]
        return self.transitions[logic]
    

       
    def check_pins(self,pins):
        if pins[0] == 1 and pins[1] == 0:
            self.motorM1 = 1
        elif pins[0] == 0 and pins[1] == 1:
            self.motorM1 = -1
        elif pins[0] == 0 and pins[1] == 0:
            self.motorM1 = 0
        elif pins[0] == 1 and pins[1] == 1:
            self.motorM1 = -2
            
        if pins[2] == 1 and pins[3] == 0:
            self.motorM2 = 1
        elif pins[2] == 0 and pins[3] == 1:
            self.motorM2 = -1
        elif pins[2] == 0 and pins[3] == 0:
            self.motorM2 = 0 
        elif pins[2] == 1 and pins[3] == 1:
            self.motorM2 = -2
        
        self.limit_switchL1 = 1 - pins[4]
        self.limit_switchL2 = 1 - pins[5]
