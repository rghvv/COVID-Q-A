VALID_KEYS = ['start_conf','end_conf','avg_conf']

class answer:
    def __init__(self,answer,start_index,end_index,start_conf,end_conf):
        self.answer = answer
        self.start_index = start_index
        self.end_index = end_index
        self.start_conf = start_conf
        self.end_conf = end_conf

        self.avg_conf = (self.start_conf+self.end_conf)/2

    def value_from_key(self,the_key):
        if the_key == 'start_conf':
            return self.start_conf
        elif the_key == 'end_conf':
            return self.end_conf
        elif the_key == 'avg_conf':
            return self.avg_conf
        else:
            return None
        
        
