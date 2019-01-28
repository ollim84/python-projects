# -*- coding: iso8859-15 -*-
from math import sqrt

#Number input
def readnumber():
    print "Give two numbers"
    n1 = input('first ')
    n2 = input('second ')
    return n1, n2

#Addition
def addition(a1, a2):
    summa = float(a1 + a2)
    return summa

#Subtraction
def subtraction (b1, b2):
    erotus = float(b1 - b2)
    return erotus
    
#Division
def division (c1, c2):
    jako = float(c1)/float(c2)
    return jako
   
#Multiplication
def multiply (d1, d2):
    kerto = float(number1)*float(number2)
    return kerto

#Area of a circle
def circleArea(p):
    pi = 3.1415926535897931
    r = float(p) / 2
    area = float(pi * r**2)
    return area

#Length of the hypotenuse of a right triangle
def hypotenuseLength(s1, s2):  
    H = float(sqrt((s1**2) + (s2**2)))
    return H

# Menu
def menu():
    print "\nGive a selection"
    print "1. Addition"
    print "2. Subtraction"
    print "3. Division"
    print "4. Multiplication"
    print "5. Area of a circle"
    print "6. Length of the hypotenuse of a right triangle"
    print "Anything else quits"
    valinta = input("your selection: ")
    return valinta

kesken = True

print "I am a calculator. How may I help you"

try:
    selection = menu()

    
    while(kesken):
       
        if(selection == 1):       
            (number1, number2) = readnumber()   
            tulos1 = addition(number1, number2)
            print "Solution is %.2f." %(tulos1)
            selection = menu()
            
              
        elif(selection == 2):
            (number1, number2) = readnumber()
            tulos2 = subtraction(number1, number2)
            print "Solution is %.2f." %(tulos2)
            selection = menu()
         
        elif(selection == 3):
            (number1, number2) = readnumber()
            try:
                tulos3 = division(number1, number2)
                print "Solution is %.2f." %(tulos3)
            except ZeroDivisionError:
                print "Zero division error"
            selection = menu()
         
        elif(selection == 4):
            (number1, number2) = readnumber()
            tulos4 = multiply(number1, number2)
            print "Solution is %.2f." %(tulos4)
            selection = menu()

        elif(selection == 5):
            halk = input("Give the diameter of the circle: ")
            tulos5 = circleArea(halk)
            print "Solution is %.2f." %(tulos5)
            selection = menu()
                
        elif(selection == 6):
            print "Give the length of the legs of the right triangle"
            sivu1 = input("first ")
            sivu2 = input("second ")
            tulos6 = hypotenuseLength(sivu1, sivu2)
            print "Solution is %.2f." %(tulos6)
            selection = menu()
            
        else:
            print "Goodbye!"
            kesken = False
except NameError:
    print "Goodbye!"
except SyntaxError:
    print "Goodbye!"
        
   

