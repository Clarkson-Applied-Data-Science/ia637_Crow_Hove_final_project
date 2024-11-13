import hashlib
from baseObject import baseObject
class room(baseObject):
    
    def __init__(self):
        self.setup()
        self.room_types = [{'value':'Standard','text':'Standard'},{'value':'Exclusive','text':'Exclusive'}]

    def verify_new(self,n=0):
        self.errors = []
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
        
    def verify_update(self,n=0):
        self.errors = []

        rt = []
        for room in self.room_types:
            rt.append(room['value'])
        if self.data[n]['room_type'] not in rt:
            self.errors.append(f'Room Type must be one of {rt}')
    
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
        

