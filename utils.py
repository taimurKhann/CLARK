from datetime import date

def get_age(birthDate): 
    days_in_year = 365    
    age = int((date.today() - birthDate).days / days_in_year) 
    return age
