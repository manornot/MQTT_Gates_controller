class garage_gates_FSM:
       
    def __init__(self):
        #CL OP K G T
        self.truth_table={'00110':0,'10110':1,'00010':2,'01110':3,'00101':4}
        #self.stt_mthd()
        self.motor = 0 # -1 - closing, 0 - stoped, 1 - opening
        #self.motorM2 = 0 # -1 - closing, 0 - stoped, 1 - opening
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
        logic = 0
        return self.transitions[logic]
    
    def all_states(self):
        return self.transitions()
    
    def unknown_state(self,read_pins): #state - -1
        self.msg = ''
        logic = self.truth_table.get(str(read_pins),-1)
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def stop_state(self,read_pins): #state - 0
        self.msg = ''
        logic = self.truth_table.get(str(read_pins),-1)
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def close_state(self,read_pins): #state - 1
        self.msg = ''
        logic = self.truth_table.get(str(read_pins),-1)
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def opening_state(self,read_pins): #state - 2
        self.msg = ''
        logic = self.truth_table.get(str(read_pins),-1)
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def open_state(self,read_pins): #state - 3
        self.msg = ''
        logic = self.truth_table.get(str(read_pins),-1)
        self.state = self.states[logic]
        return self.transitions[logic]
    
    def closing_state(self,read_pins): #state - 4
        self.msg = ''
        logic = self.truth_table.get(str(read_pins),-1)
        self.state = self.states[logic]
        return self.transitions[logic]
