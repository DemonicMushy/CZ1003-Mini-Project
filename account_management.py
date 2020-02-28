from string import punctuation
from operator import itemgetter
import pickle

def password_checker(password, username):
    """(string, string) -> (boolean, string)

    Returns True if input password meets criterias:
    Length more than 8, at least one uppercase, at least one lowercase, at least one digit, at least one punctuation, and does not contain username.
    Otherwise return False and prints the failed criteria.
    """
    criterias = {"length":False, "uppercase":False, "lowercase":False, "digit":False, "symbol":False, "username":True}

    if len(username) == 0:
        #print("Username cannot be empty")
        return False, "Username cannot be empty."
    if len(password) > 8:           #check for length of more than 8
        criterias["length"] = True
    for letter in password:
        if letter.isupper():        #check for upper case letter
            criterias["uppercase"] = True
            continue
        if letter.islower():        #check for lower case letter
            criterias["lowercase"] = True
            continue
        if letter.isdigit():        #check for digit
            criterias["digit"] = True
            continue
        if letter in punctuation:   #check for punctuation
            criterias["symbol"] = True
            continue
    if username in password:        #check if username in password
        criterias["username"] = False
    for i in criterias.keys():
        if criterias[i] == False:
            #print("Password failed {0} criteria.".format(i))
            return False, "Password failed {0} criteria.".format(i)
    return True,
    

def date_of_birth_checker(dob):
    """ (string) -> (boolean, string)

    checks if date of birth is in valid DDMMYYYY format
    """

    try:                                                            #Check if date of birth is purely numeric
        int(dob)
        month = int(dob[2:4])
        day = int(dob[0:2])
        year = int(dob[4:])
    except Exception:
        return False, "Please enter in DDMMYYYY format."
    else:
        if len(dob) != 8:
            #print("Please enter in DDMMYYYY format.")
            return False, "Please enter in DDMMYYYY format."
        elif year > 2018 or year < 1919:                                #Check if year is valid
            #print("Year is invalid.")
            return False, "Year is invalid."
        elif month > 12 or month <= 0:                                  #Check if month is valid
            #print("Month is invalid.")
            return False, "Month is invalid."
        elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:  #Months with 31 days
            if day > 31 or day <=0:
                #print("Day cannot be more than 31.")
                return False, "Day cannot be more than 31."
        elif month == 4 or month == 6 or month == 9 or month == 11:     #Months with 30 days
            if day > 30 or day <= 0:
                #print("Day is invalid.")
                return False, "Day is invalid."
        elif month == 2:                                                #Feburary
            if ((year%4 == 0 and not year%100 == 0) or year%400 == 0):  #Leap years
                if day > 29 or day <=0:
                    #print("Day is invalid.")
                    return False, "Day is invalid."
            elif day > 28 or day <= 0:                                              #Non leap years
                #print("Day is invalid.")
                return False, "Day is invalid."
        return True, "Account created"

def store_account(username, password, dob):
    """(string, string, string) -> boolean

    check if username already present in file
    store details into a dictionary and pickle into a file
    """
    accounts = {}
    try:
        with open("accounts.txt", "rb") as file:
            accounts = pickle.load(file)
            for details in list(accounts.keys()):
                if username == details[0]:
                    return False
            with open("accounts.txt", "wb") as file:
                accounts[(username, dob)] = [password, 0]
                pickle.dump(accounts, file)
                return True
    except Exception as ex:
        accounts[(username, dob)] = [password, 0]
        with open("accounts.txt", "wb") as file:
            pickle.dump(accounts, file)
        return True

def log_in(username, password):
    """(string, string) -> (boolean, string)

    checks if password matches with username account
    """
    accounts = {}
    try:
        with open("accounts.txt", "rb") as file:
            accounts = pickle.load(file)
            for details in list(accounts.keys()):
                if username == details[0]:
                    if accounts[details][1] >= 3:
                        #account locked
                        return False, "Account locked"
                    if password == accounts[details][0]:
                        #successful log in
                        return True, "Log in successful"
                    else:
                        with open("accounts.txt", "wb") as file:
                            for details in list(accounts.keys()):
                                if username == details[0]:
                                    accounts[details][1] += 1
                            pickle.dump(accounts, file)
                        return False, "Incorrect password"
        #username not found, try again
        return False, "Username not found"
    except Exception as ex:
        #no account present = username not found
        return False, "Username not found"

def reactivate_account(username, dob):
    """(string, string) -> (boolean, string)

    checks if password matches with username account
    """
    state = False
    try:
        with open("accounts.txt", "rb") as file:
            accounts = pickle.load(file)
            for details in list(accounts.keys()):
                if username == details[0]:
                    if dob == details[1]:
                        #successful reset
                        with open("accounts.txt", "wb") as file:
                            for details in list(accounts.keys()):
                                if username == details[0]:
                                    accounts[details][1] = 0
                            pickle.dump(accounts, file)
                        return True, "Account re-activated"
                    else:
                        #dob wrong
                        return False, "Incorrect date of birth"
        #username not found, try again
        return False, "Username not found"
    except Exception as ex:
        #no account present = username not found
        return False, "Username not found"
    
def create_account():
    """asks for user input and store details in file

    checks if password and date of birth are valid
    """

    username = input("Username: ")
    password = input("Password: ")
    dob = input("Date Of Birth, DDMMYYY: ")
    if not password_checker(password, username):
        print("Password does not meet requirements. Please try again.")
        create_account()
    elif date_of_birth_checker(dob):
        print("Date of birth is invalid. Please try again.")
        create_account()
    else:
        if store_account(username,password,dob):
            pass
        else:
            create_account()


if __name__ == "__main__":
    password_checker("Ab1!zzzz.", "python")
    password_checker("password12345","python")
    password_checker("python12345", "python")
    date_of_birth_checker("29022000")
    create_account()

