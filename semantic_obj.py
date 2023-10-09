class semantic_command:
    def __init__(self, command, type) -> None:
        self.command = command
        self.type = type
        
CLEFS = ("C1", "C2", "C3", "C4", "C5", "F3", "F4", "F5", "G1", "G2")
class semantic_clef(semantic_command):
    def __init__(self, command) -> None:
        super().__init__(command, "clef")
        self.clef = None        
        #find the clef in the command
        for clef in CLEFS:
            if clef in command:
                self.clef = clef
                break
        if self.clef == None:
            raise Exception("Clef value not found: " + command)
        
LENGTHS = ("hundred_twenty_eighth", "sixty_fourth", "thirty_second", "sixteenth", "eighth", "quarter", "half", "whole", "double_whole", "quadruple_whole")
class semantic_rest(semantic_command):
    def __init__(self, command, type="note") -> None:
        super().__init__(command, type)
        self.length = None
        self.dot = None
        self.fermata = None
        
        #find the length in the command
        for length in LENGTHS:
            if length in command:
                self.length = length
                break
        if self.length == None:
            raise Exception("Length value not found: " + command)
        
        #find instance of fermata
        if "fermata" in command:
            self.fermata = True
        else:
            self.fermata = False
        
        #find instance of dot dot
        if ".." in command:
            self.dot = "double"
        elif "." in command:
            self.dot = "single"
        else:
            self.dot = "none"
        if self.dot == None:
            raise Exception("Illegal value for dot: " + command)
        
class semantic_note(semantic_rest):
    def __init__(self, command) -> None:
        super().__init__(command, "rest")
        
        #find instance of grace note
        if "gracenote" in command:
            self.grace = True
        else:
            self.grace = False
            
        #find the pitch command
        #grab the substring after the first '-' and before the first '_'
        self.pitch = command[command.find('-') + 1:command.find('_')]
        
class semantic_multirest(semantic_command):
    def __init__(self, command) -> None:
        super().__init__(command, "multirest")
        self.length = None
        
        #the length is after the first '-'
        self.length = command[command.find('-') + 1:]
        
    
TIME_SIGNATURES = ("11/4", "1/2", "12/16", "12/4", "12/8", "1/4", "2/1", "2/2", "2/3", "2/4", "24/16", "2/48", "2/8", "3/1", "3/2", "3/4", "3/6", "3/8", "4/1", "4/2", "4/4", "4/8", "5/4", "5/8", "6/16", "6/2", "6/4", "6/8", "7/4", "8/12", "8/16", "8/2", "8/4", "8/8", "9/16", "9/4", "9/8", "C/", "C")   
class semantic_time_signature(semantic_command):
    def __init__(self, command) -> None:
        super().__init__(command, "time_signature")
        self.time_signature = None
        
        #find the time signature in the command
        for time_signature in TIME_SIGNATURES:
            if time_signature in command:
                self.time_signature = time_signature
                break
        if self.time_signature == None:
            raise Exception("Time signature value not found: " + command)
        
        
#TODO: add support for ties
class semantic_tie(semantic_command):
    def __init__(self, command) -> None:
        super().__init__(command, "tie")
        self.type = None
        
        #find the tie type in the command
        if "start" in command:
            self.type = "start"
        elif "stop" in command:
            self.type = "stop"
        else:
            raise Exception("Invalid tie type: " + command)