from datetime import datetime
import hashlib
from baseObject import baseObject

class reservation(baseObject):
    
    def __init__(self):
        self.setup()
        self.payment_methods = [{'value':'Credit/Debit Card','text':'Credit/Debit Card'},{'value':'Cash','text':'Cash'}]

    def verify_new(self,n=0):
        self.errors = []

       # Convert check-in and check-out dates from string to datetime for comparison
        try:
            check_in_date = datetime.strptime(self.data[n]['check_in_date'], '%Y-%m-%d')
            check_out_date = datetime.strptime(self.data[n]['check_out_date'], '%Y-%m-%d')

            # Check if check-out date is before check-in date
            if check_out_date <= check_in_date:
                self.errors.append("Check-out date must be after check-in date.")
        except ValueError:
            self.errors.append("Invalid date format for check-in or check-out date.")


        try:
            check_in_date = datetime.strptime(self.data[n]['check_in_date'], '%Y-%m-%d')
            payment_date = datetime.strptime(self.data[n]['payment_date'], '%Y-%m-%d')

            # Check if payment date is after check-in date
            if payment_date > check_in_date:
                self.errors.append("Payment date can not be after check-in date.")
        except ValueError:
            self.errors.append("Invalid date format for check-in or payment date.")
 
        # Verify payment method
        pm = []
        for method in self.payment_methods:
            pm.append(method['value'])
        if self.data[n]['payment_method'] not in pm:
            self.errors.append(f'Method must be one of {pm}')
        
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
        
    def verify_update(self,n=0):
        self.errors = []

         # Convert check-in and check-out dates from string to datetime for comparison
        try:
            check_in_date = datetime.strptime(self.data[n]['check_in_date'], '%Y-%m-%d')
            check_out_date = datetime.strptime(self.data[n]['check_out_date'], '%Y-%m-%d')
            
            # Check if check-out date is before check-in date
            if check_out_date <= check_in_date:
                self.errors.append("Check-out date must be after check-in date.")
        except ValueError:
            self.errors.append("Invalid date format for check-in or check-out date.")


        try:
            check_in_date = datetime.strptime(self.data[n]['check_in_date'], '%Y-%m-%d')
            payment_date = datetime.strptime(self.data[n]['payment_date'], '%Y-%m-%d')

            # Check if payment date is after check-in date
            if payment_date > check_in_date:
                self.errors.append("Payment date can not be after check-in date.")
        except ValueError:
            self.errors.append("Invalid date format for check-in or payment date.")

        # Verify payment method
        pm = []
        for method in self.payment_methods:
            pm.append(method['value'])
        if self.data[n]['payment_method'] not in pm:
            self.errors.append(f'Method must be one of {pm}')
    
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
        

