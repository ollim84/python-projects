# -*- coding: iso-8859-1 -*-
# tiedosto hangman.py

import sys
import random

#kesken = False
guessCount = 0
guess1 = 0
guess2 = 0
guess3 = 0
guess4 = 0
guess5 = 0
count = 0
#sananro = 1
word2 = ''
nimi = sys.argv[1]
try:
    tiedosto = open(nimi, 'r')  # avataan tiedosto lukemista varten
    A = len(tiedosto.readlines())
    sananro = random.randint(1,A)
    tiedosto.close()

    tiedosto = open(nimi, 'r')  # avataan tiedosto lukemista varten

    while True:
        rivi = tiedosto.readline() # luetaan tiedostosta rivi
        count = count + 1;
        if count == sananro:
            sana = rivi
            sana = sana.strip()
        if len(rivi) == 0: # jos rivin pituus on 0, ollaan lopussa
            break
        #print rivi,    
    tiedosto.close() # suljetaan tiedosto
    #print sana



    print "Welcome to Hangman"
    if sananro == 1:
        word = "_ _ _ _ _"
        print "_____"  
    elif sananro == 2:
        word = "_ _ _ _ _"
        print "_____"
    elif sananro == 3:
        word = "_ _ _ _ _ _"
        print "______"
    elif sananro == 4:
        word = "_ _ _ _"
        print "____"

        
    word = word.split(' ')
    #print word

    while ((guessCount < 5) & (word2!= sana)) :
        guess = raw_input("Your guess: ")

        if sananro == 1:
            if ((guess == "k") & (guess1 == 0)):               
                print "Success!"
                word[0] = word[0].replace('_', 'k')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                word2 = word2.strip()
                if word2 != sana:
                    print word2
                guess1 = 1
            elif ((guess == "i") & (guess2 == 0)):
                print "Success!"
                word[1] = word[1].replace('_', 'i')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess2 = 1
            elif ((guess == "s") & (guess3 == 0)):
                print "Success!"
                word[2] = word[2].replace('_', 's')
                word[3] = word[3].replace('_', 's')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess3= 1
            elif ((guess == "a") & (guess4 == 0)):
                print "Success!"
                word[4] = word[4].replace('_', 'a')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess4 = 1
            else:
                guessCount = guessCount + 1
                print "Failure! You have tried tried %i times!" %(guessCount)
                if guessCount < 5:
                    print word2
                    

        elif sananro == 2:
            if ((guess == "k") & (guess1 == 0)):
                print "Success!"
                word[0] = word[0].replace('_', 'k')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess1 = 1
            elif ((guess == "o") & (guess2 == 0)):
                print "Success!"
                word[1] = word[1].replace('_', 'o')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess2 = 1
            elif ((guess == "i") & (guess3 == 0)):
                print "Success!"
                word[2] = word[2].replace('_', 'i')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess3 = 1
            elif ((guess == "r") & (guess4 == 0)):
                print "Success!"
                word[3] = word[3].replace('_', 'r')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess4 = 1
            elif ((guess == "a") & (guess5 == 0)):
                print "Success!"
                word[4] = word[4].replace('_', 'a')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]
                if word2 != sana:
                    print word2
                guess5 = 1
            else:
                guessCount = guessCount + 1
                print "Failure! You have tried tried %i times!" %(guessCount)
                if guessCount < 5:
                    print word2

        elif sananro == 3:
            if ((guess == "k") & (guess1 == 0)):
                print "Success!"
                word[0] = word[0].replace('_', 'k')
                word[2] = word[2].replace('_', 'k')
                word[3] = word[3].replace('_', 'k')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]+word[5]
                if word2 != sana:
                    print word2
                guess1 = 1
            elif ((guess == "e") & (guess2 == 0)):
                print "Success!"
                word[1] = word[1].replace('_', 'e')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]+word[5]
                if word2 != sana:
                    print word2
                guess2 = 1
            elif ((guess == "i") & (guess3 == 0)):
                print "Success!"
                word[4] = word[4].replace('_', 'i')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]+word[5]
                if word2 != sana:
                    print word2
                guess3 = 1
            elif ((guess == "s") & (guess4 == 0)):
                print "Success!"
                word[5] = word[5].replace('_', 's')
                word2 = word[0]+word[1]+word[2]+word[3]+word[4]+word[5]
                if word2 != sana:
                    print word2
                guess4 = 1
            else:
                guessCount = guessCount + 1
                print "Failure! You have tried tried %i times!" %(guessCount)
                if guessCount < 5:
                    print word2
            
        elif sananro == 4:
            if ((guess == "p") & (guess1 == 0)):
                print "Success!"
                word[0] = word[0].replace('_', 'p')
                word[3] = word[3].replace('_', 'p')
                word2 = word[0]+word[1]+word[2]+word[3]
                if word2 != sana:
                    print word2
                guess1 = 1
            elif ((guess == "l") & (guess2 == 0)):
                print "Success!"
                word[1] = word[1].replace('_', 'l')
                word2 = word[0]+word[1]+word[2]+word[3]
                if word2 != sana:
                    print word2
                guess2 = 1
            elif ((guess == "o") & (guess3 == 0)):
                print "Success!"
                word[2] = word[2].replace('_', 'o')
                word2 = word[0]+word[1]+word[2]+word[3]
                if word2 != sana:
                    print word2
                guess3 = 1
            else:
                guessCount = guessCount + 1
                print "Failure! You have tried tried %i times!" %(guessCount)
                if guessCount < 5:
                    print word2
    if(word2 == sana):
        print "You win!"
        print "Goodbye"
    else:
        print "Game over! you lose!"
        print "The word was %s" %(sana)
        print "Goodbye"

except IOError:
    print "[Errno 2] No such file or directory: '%s'" %(nimi)
