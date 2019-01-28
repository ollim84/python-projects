# -*- coding: iso8859-15 -*-
import sys



###############Funktioiden ja muuttujien määrittely##################




#-------------Komentoriviargumenttien prosessointi----------------------------

#Käytin mallina seuraavan linkin esimerkkiä: http://docs.python.org/library/optparse.html

def process_args():
    from optparse import OptionParser
    parser = OptionParser()
    #Luodaan komentoriviparametri "-f" tai "--file", joka tallettaa arvon opts.file kohteeseen
    parser.add_option("-f", "--file", action="store", dest="file",
                      help="Read a game situation from FILE.")

    #Luodaan komentoriviparametri "-n" tai "--new", joka tallettaa arvon opts.new kohteeseen
    #Argumenttien määrän täytyy olla 3.
    parser.add_option("-n", "--new", action="store", dest="new", nargs = 3,
                      help="Start a new game")

    #Luodaan komentoriviparametri "-i" tai "--interactive", joka tallettaa arvon opts.interactive kohteeseen.
    #Kyseessä on boolean-muuttuja, jolla on 2 eri arvoa (True tai False).
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive",
                      help="Play game in interactive mode.")
    return parser.parse_args()

(opts, args) = process_args()

if opts.interactive == True:
    interactive = True
else:
    interactive = False

#Laskuri laudalle syötettyjen merkkien määrästä     
count = 0

#Boolean-muuttuja pelin loppumiselle
error = False

#Boolean-muuttuja tiedoston virheelle
FileError = False

#Boolean-muuttuja virheelliselle voittonumeron arvolle
winNumberError = False

#Boolean-muuttuja X:n voitolle
winX = False

#Boolean-muuttuja 0:n voitolle
win0 = False

#Boolean-muuttuja yleiselle voitolle
win = False


#-------------Tiedostosta lukeminen----------------------------

def read_board(tiedosto):

    #Käydään tiedosto läpi ensimmäisen kerran, jolloin otetaan talteen rivien ja sarakkeiden lukumäärä    
    tiedosto1 = open('%s.txt' %tiedosto, 'r') # avataan tiedosto lukemista varten

    #Laskuri tiedoston rivien määrälle
    count1 = 0

    while True:
        rivi = tiedosto1.readline() # luetaan tiedostosta rivi
        count1 = count1 + 1    
        if count1 == 1:
            sarakkeet1 = rivi.strip()
            sarakkeet2 = sarakkeet1.split(' ')
            cols = len(sarakkeet2)
        if len(rivi) == 0: # jos rivin pituus on 0, ollaan lopussa
            count1 = count1 - 1
            break       
    tiedosto1.close() # suljetaan tiedosto

    #Pelilaudan rivien määrä saadaan vähentämällä tiedoston rivien määrästä 1.
    #Tiedostossa viimeinen rivi kertoo voittoon tarvittavien peräkkäisten merkkien määrän.    
    rows = count1 - 1

    
    #Käydään tiedosto läpi toisen kerran ja lisätään board_list - listaan tiedoston alkiot
    #eli X:n ja 0:n sijoittumiset pelilaudalla. Lisäksi otetaan talteen tarvittava voittonumero.
    
    tiedosto2 = open('%s.txt' %tiedosto, 'r') # avataan tiedosto lukemista varten
    count2 = 0
    board_list = []

    while True:
        rivi = tiedosto2.readline() # luetaan tiedostosta rivi
        count2 = count2 + 1
        if ((len(rivi) != 0) & (count2 <= rows)):
            rivi2 = rivi.strip()
            rivi3 = rivi2.split(' ')
            board_list.append(rivi3)
        if count2 == count1:
            a = rivi.strip()
            b = a.split('#')
            winNro = int(b[1])
        if len(rivi) == 0: # jos rivin pituus on 0, ollaan lopussa
            count2 = count2 - 1
            break
                   
    tiedosto2.close() # suljetaan tiedosto

    #Palautetaan board_list, rivien ja sarakkeiden lukumäärä ja voittonumero
    return board_list, rows, cols, winNro

#-------------Tiedostoon kirjoittaminen----------------------------    

#Tämän funktion tarkoituksena on kirjoittaa pelilaudan tilanne tiedostoon.
#Sen parametreina on board_list - lista, joka sisältää pelilaudan tilanteen,
#ja tiedosto mihin pelitilanne halutaan kirjoittaa.

def write_board(board_list, tied):

    #Avataan tiedosto kirjoitusta varten
    f = open("%s.txt" %tied, 'w')

    #Kirjoitetaan riveittäin ja sarakkeittain tiedostoon board_list:n alkiot
    for k in range(rows):
        rivi = ""
        for j in range(cols):
            rivi = rivi + " " +("%s" % (board_list[k][j]))
            rivi = rivi.strip()
        f.write(rivi)
        f.write("\n")
    #Kirjoitetaan voittonumero tiedoston viimeiselle riville.
    f.write("#%d" %winNumber)

    #Suljetaan tiedosto
    f.close()

#-------------Laudan tulostus----------------------------

#Funktion tarkoituksena on tulostaa pelitilanne ruudulle.
#Sen parametrina on board_list - lista.
    
def print_board(board_list):
    rivi2 = "   0"
    for j in range (cols):
        if j!=0:
            rivi2 = rivi2 + " " + "%d" %j     
    print rivi2
    for i in range(rows):
        rivi = "%d:" % i
        for j in range(cols):
            rivi = rivi + " "+ ("%s" % (board_list[i][j]))
        print "%s" % rivi


#-------------Voittoyhdistelmän tarkistus----------------------------

#Funktio tarkistaa onko laudalla tarvittava määrä merkkejä peräkkäin
#voittoa varten.

        
def check_win(board_list, winX, win0):

    #Luodaan X:lle ja 0:lle voittoon tarvittavat listat ja alustetaan kaikki alkiot ykkösiksi.

    #Xwin_listHor, Xwin_listVer, Owin_listHor  ja Owin_listVer ovat pysty ja vaakarivien voittolistoja
    
    Xwin_listHor = list ()
    for i in range(rows):
        Xwin_listHor.append(1)

    Xwin_listVer = list ()
    for i in range(cols):
        Xwin_listVer.append(1)

    Owin_listHor = list ()
    for i in range(rows):
        Owin_listHor.append(1)

    Owin_listVer = list ()
    for i in range(cols):
        Owin_listVer.append(1)       


    #Xwin_listCross1 ja Owin_listCross1 ovat viistoon vasemmasta alanurkasta
    #oikeaan ylänurkkaan menevien merkkien tarkistuslistat
        
    #Xwin_listCross2 ja Owin_listCross2 ovat viistoon oikeasta alanurkasta
    #vasempaan ylänurkkaan menevien merkkien tarkituslistat
    
    Xwin_listCross1 = list()
    for i in range(rows):
        row = list()
        for j in range(cols):
            row.append(1)
        Xwin_listCross1.append(row)

    Xwin_listCross2 = list()
    for i in range(rows):
        row = list()
        for j in range(cols):
            row.append(1)
        Xwin_listCross2.append(row)

    Owin_listCross1 = list()
    for i in range(rows):
        row = list()
        for j in range(cols):
            row.append(1)
        Owin_listCross1.append(row)

    Owin_listCross2 = list()
    for i in range(rows):
        row = list()
        for j in range(cols):
            row.append(1)
        Owin_listCross2.append(row)
        
    #Käydään board_list läpi riveittäin ja sarakkeittain
    for i in range(rows):
        for j in range(cols):
            if j != 0:
                
                #Tarkistetaan pystyrivien peräkkäiset merkit
                if board_list[i][j] == board_list[i][j-1] == "x":
                    Xwin_listHor[i]= Xwin_listHor[i] + 1
                elif board_list[i][j] == board_list[i][j-1] == "o":
                    Owin_listHor[i]= Owin_listHor[i] + 1
                              
            if i != 0:

                #Tarkistetaan vaakarivien peräkkäiset merkit
                if board_list[i][j] == board_list[i-1][j] == "x":
                    Xwin_listVer[j] = Xwin_listVer[j] + 1
                elif board_list[i][j] == board_list[i-1][j] == "o":
                    Owin_listVer[j] = Owin_listVer[j] + 1
                    
            # Tarkistetaan viistoon vasen alanurkka -> oikea ylänurkka menevät peräkkäiset merkit
            for k in range(cols-1):
                m = k + 1
                if ((i > k) & (j < (cols-m))):

                    #Jos vierekkäin on kaksi samanlaista x-merkkiä kasvatetaan laskuria yhdellä
                    if ((board_list[i][j] == "x") & (board_list[i-m][j+m] == "x")):
                        Xwin_listCross1[i][j] = Xwin_listCross1[i][j] + 1

                    #Muussa tapauksessa hypätään pois silmukasta eikä jatketa laskurin kasvattamista
                    else:
                        if ((board_list[i][j] == "x") & (board_list[i-m][j+m] == "o")):
                            break
                        elif ((board_list[i][j] == "x") & (board_list[i-m][j+m] == "_")):
                            break
                        
                    #Jos vierekkäin on kaksi samanlaista o-merkkiä kasvatetaan laskuria yhdellä    
                    if ((board_list[i][j] == "o") & (board_list[i-m][j+m] == "o")):
                        Owin_listCross1[i][j] = Owin_listCross1[i][j] + 1

                    #Muussa tapauksessa hypätään pois silmukasta eikä jatketa laskurin kasvattamista
                    else:
                        if ((board_list[i][j] == "o") & (board_list[i-m][j+m] == "x")):
                            break
                        elif ((board_list[i][j] == "o") & (board_list[i-m][j+m] == "_")):
                            break

                        
            # Tarkistetaan viistoon Oikea alanurkka -> vasen ylänurkka menevät peräkkäiset merkit          
            for w in range(cols-1):
                n = w + 1
                if((i > w) & (j > w)):

                    #Jos vierekkäin on kaksi samanlaista x-merkkiä kasvatetaan laskuria yhdellä
                    if ((board_list[i][j] == "x") & (board_list[i-n][j-n] == "x")):
                        Xwin_listCross2[i][j] = Xwin_listCross2[i][j] + 1

                    #Muussa tapauksessa hypätään pois silmukasta eikä jatketa laskurin kasvattamista
                    else:
                        if ((board_list[i][j] == "x") & (board_list[i-n][j-n] == "o")):
                            break
                        elif((board_list[i][j] == "x") & (board_list[i-n][j-n] == "_")):
                            break
                        
                    #Jos vierekkäin on kaksi samanlaista o-merkkiä kasvatetaan laskuria yhdellä      
                    if ((board_list[i][j] == "o") & (board_list[i-n][j-n] == "o")):
                        Owin_listCross2[i][j] = Owin_listCross2[i][j] + 1
            
                    #Muussa tapauksessa hypätään pois silmukasta eikä jatketa laskurin kasvattamista    
                    else:
                        if ((board_list[i][j] == "o") & (board_list[i-n][j-n] == "x")):
                            break
                        elif((board_list[i][j] == "o") & (board_list[i-n][j-n] == "_")):
                            break
                             
      
    #Käydään läpi tarkistuslistat.
    #Jos alkion määrä = voittonumero, asetetaan vastaava X:n tai 0:n
    #voittoa kuvaava boolean muuttuja todeksi (True).
    for i in range(rows):
        for j in range(cols):
            if Xwin_listHor[i] == winNumber:
                winX = True
            elif Xwin_listVer[j] == winNumber:
                winX = True
            elif Xwin_listCross1[i][j] == winNumber:
                winX = True
            elif Xwin_listCross2[i][j] == winNumber:
                winX = True
            elif Owin_listHor[i] == winNumber:
                win0 = True
            elif Owin_listVer[j] == winNumber:
                win0 = True
            elif Owin_listCross1[i][j] == winNumber:
                win0 = True
            elif Owin_listCross2[i][j] == winNumber:
                win0 = True
                
    #Jos X:n tai 0:n voittomuuttuja on tosi, asetetaan yleinen voitto todeksi.
    #Muussa tapauksessa asetetaan yleinen voitto epätodeksi.
    if winX == True:
        win = True
        return win, winX, win0
    elif win0 == True:
        win = True
        return win, winX, win0
    else:
        win = False
        return win, winX, win0

#-------------Merkin tarkistus----------------------------

#Funktio tarkistaa onko käyttäjän syöttämien koordinaattien paikalla jo merkki.
#Jos paikalla ei ole merkkiä, lisätään siihen "x" tai "o" riippuen pelaajan vuorosta.
    
#Funktion sisääntuloina ovat koordinaatit (v1, v2), pelaajien boolean-muuttujat (p1,p2),
#boolean tyyppinen flag-lista, joka kertoo onko koordinaatin paikalla jo merkki sekä laskuri c
#jo syötettyjen merkkien määrää varten.

#Boolean-muuttujat p1 (x) ja p2 (o) kertovat kumman merkin vuoro on.
    
def check_mark(v1, v2, p1, p2, flag, c):
    try:
        x = v1
        y = v2

        #Jos paikalla ei ole vielä merkkiä
        if flag[x][y] == False:

            #Jos on x:n vuoro
            if p1 == True:
                #Asetetaan board-list listaan koordinaattien paikalle "x"
                board_list[x][y] = "x"

                #Asetetaan vuoro o:lle
                p1 = False
                p2 = True
                
                #Asetetaan flag-listaan arvo True eli paikka on varattu
                flag[x][y] = True
                
                #Lisätään laskuria yhdellä
                c = c + 1

                #Palautetaan pääohjelmalle board_list, p1, p2 ja laskuri c
                return board_list, p1, p2, c
            
            #Jos on o:n vuoro
            elif p2 == True:
                board_list[x][y] = "o"

                #Asetetaan vuoro x:lle
                p1 = True
                p2 = False
                
                #Asetetaan flag-listaan arvo True eli paikka on varattu
                flag[x][y] = True
                
                #Lisätään laskuria yhdellä
                c = c + 1

                #Palautetaan pääohjelmalle board_list, p1, p2 ja laskuri c
                return board_list, p1, p2, c
            
        #Jos paikalla on jo merkki, tulostetaan virheilmoitus
        else:
            print "That square is already taken."
            return board_list, p1, p2, c
        
    #Jos käyttäjä syötti jotain muuta kuin numeroita, tulostetaan virheilmoitus
    except ValueError:
        print "Wrong format for the coordinates!"
        return board_list, p1, p2, c
    
    #Jos käyttäjän syöttämät koordinaatit menevät pelilaudan ulkopuolelle, tulostetaan virheilmoitus
    except IndexError:
        print "Your selection goes out of range!"
        return board_list, p1, p2, c
    

###############Pääohjelma##################


try:
    #-------------Komentorivimoodi----------------------------

    if interactive == False:
        
        # Luodaan uusi peli määrättyyn tiedostoon
        
        if ((opts.file is not None) & (opts.new is not None)):
            tiedosto = opts.file

            try:

                #Muunnetaan käyttäjän syöttämät merkkijonot integer-muuttujiksi
                rows = int(opts.new[0])
                cols = int(opts.new[1])
                winNumber = int(opts.new[2])

                #Jos rivien tai sarakkeiden määrä on negatiivinen, aiheutetaan keskeytys
                if ((rows < 0) | (cols < 0)):
                    raise ValueError

                #Jos voittonumero on vääränlainen, aiheutetaan keskeytys
                #Voittonumeron täytyy olla suurempi tai yhtäsuuri kuin 1 tai suurempi kuin rivien ja sarakkeiden lukumäärä
                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError
                
                #Luodaan board_list-lista, joka pitää sisällään laudan merkit. Alussa asetetaan jokaiselle paikalle "_".
                board_list = list()
                for i in range(rows):
                    rivi = list()
                    for j in range(cols):
                        rivi.append("_")
                    board_list.append(rivi)
                    
                #Kirjoitetaan lauta tiedostoon    
                write_board(board_list, tiedosto)

            #Tulostetaan virheilmoitukset keskeytyksille   
            except ValueError:
                print "Wrong format for the commandline parameters."
                if ((rows < 0) | (cols < 0)):
                    print "You inserted negative integer values for rows or columns."
                
                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    print "Incorrect win number. The win number must be larger than 1 and smaller than rows or columns."
                
            
        # Tehdään haluttu siirto tiedostossa olevaan peliin
            
        elif ((opts.file is not None) & (opts.new is None)):
                      
            tiedosto = opts.file
            board_list = list()
            try:

                #Luetaan tiedostosta board_list, rivien ja sarakkeiden lkm sekä voittonumeron arvon
                [board_list, rows, cols, winNumber] = read_board(tiedosto)

                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError

                #Laudan koko
                board_size = rows * cols

                #Laskuri laudalle syötettyjen merkkien määrästä  
                count = 0

                #Laskuri laudalle syötettyjen "x"-merkkien määrästä  
                Xcount = 0

                #Laskuri laudalle syötettyjen "o"-merkkien määrästä  
                Ocount = 0

                #Luodaan flag_list-lista, joka kertoo onko laudan paikka jo käytössä
                flag_list = list()
                for i in range(rows):
                    line = list()
                    for j in range(cols):
                        line.append(False)
                    flag_list.append(line)
                      
                #Käydään läpi tiedostosta haettu board_list
                for i in range(rows):
                    for j in range(cols):

                        #Jos paikalla on "x" tai "o" asetetaan koordinaattien flag_list arvo todeksi (True) ja
                        #kasvatetaan laskuria yhdellä.
                        if (board_list[i][j] != "_"):
                            flag_list[i][j] = True
                            count = count + 1
                            
                        #Jos paikassa on "x" kasvatetaan x:n laskuria yhdellä
                        if (board_list[i][j] == "x"):
                            Xcount = Xcount + 1
                            
                        #Jos paikassa on "o" kasvatetaan o:n laskuria yhdellä
                        if (board_list[i][j] == "o"):
                            Ocount = Ocount + 1

                        #Jos paikassa on jotain muuta, asetetaan FileError-muuttuja todeksi.
                        if ((board_list[i][j] != "o") & (board_list[i][j] != "x") & (board_list[i][j] != "_")):
                            FileError = True

                #Jos x:n merkkien määrä > (o:n merkkien määrä + 1) tai jos o:n merkkien määrä > x:n merkkien määrä
                #Ohjelmassa oletetaan aina, että x aloittaa jokaisen pelin ensimmäisenä
                if ((Xcount > (Ocount +1)) | (Ocount > Xcount)):
                    FileError = True;

                #Suoritetaan tarvittavat toimenpiteet, jos tiedostosta ei löytynyt virheitä            
                if FileError == False:

                    #Määritetään kumman pelaajan vuoro on
                    if Xcount == Ocount:
                        player1 = True
                        player2 = False
                    elif Xcount > Ocount:
                        player2 = True
                        player1 = False

                    #Tarkistetaan onko peli päättynyt jo aiemmin   
                    [win, winX, win0] = check_win(board_list, winX, win0)

                    #Jos peli ei ole vielä loppunut tai lauta ei ole vielä täynnä    
                    if ((count < board_size) & (winX == False) & (win0 == False)):

                        #Kun halutaan tarkastaa pelin tilanne tekemättä siirtoa
                        if (len(args) == 0):    
                            print_board(board_list)
                            if player1 == True:
                                print "It's x's turn"
                            else:
                                print "It's o's turn"

                        #Kun tehdään haluttu siirto
                        if len(args) != 0:
                            try:
                                coordinate1 = int(args[0])
                                coordinate2 = int(args[1])
                                if ((coordinate1 < 0) | (coordinate2 < 0)):
                                    raise ValueError

                                #Tarkastetaan onko merkki jo laudalla
                                [board_list, player1, player2, count] = check_mark(coordinate1, coordinate2, player1, player2, flag_list, count)

                                #Tulostetaan lauta ruudulle
                                print_board(board_list)

                                #Kirjoitetaan lauta tiedostoon
                                write_board(board_list, tiedosto)

                                #Tarkistetaan tuliko vielä voitto
                                [win, winX, win0] = check_win(board_list, winX, win0)

                            #Tulostetaan virheilmoitukset keskeytyksille    
                            except ValueError:
                                print "Wrong format for the coordinates!\n"
                                print_board(board_list)
                            except IndexError:
                                print "Wrong format for the coordinates!\n"
                                print_board(board_list)

                        #Jos kumpikaan ei voittanut
                        if ((win == False) & (count == board_size)):
                            print "It's a draw! Game over."

                        #Jos jompikumpi pelaaja voitti
                        else:
                            if(winX == True):
                                print "X wins!"
                            elif(win0 == True):
                                print "0 wins!"
                        
                    #Muussa tapauksessa peli on jo päättynyt   
                    else:
                        print "The game has ended. Start a new game if you like.\n"
                        print_board(board_list)

                #Tiedostosta löytyi virhe, tulostetaan virheilmoitus
                else:
                    print "Error reading file: %s" %tiedosto

            #Tulostetaan virheilmoitus, kun tiedostoa ei ole olemassa
            except IOError:
                print "I/O error: no such file '%s'" %tiedosto

            #Tulostetaan virheilmoitukset vääränlaisille rivien, sarakkeiden ja voittonumeron argumenteille
            except ValueError:
                print "Wrong format for the commandline parameters."
                if ((rows < 0) | (cols < 0)):
                    print "You inserted negative integer values for rows or columns."             
                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    print "Incorrect win number. The win number must be larger than 1 and smaller than rows or columns."
                    
        #Tulostetaan virheilmoitus vääränlaisille komentoriviparametreille        
        else:
            print "Wrong format for the commandline parameters."
                

    #-------------Interaktiivinen moodi----------------------------
            
    elif ((interactive == True) & (opts.new is not None) | ((interactive == True) & (opts.new is None) & (opts.file is not None))):

        try:

            # Aloitetaan täysin uusi peli
            if (opts.new is not None):

                #Muunnetaan käyttäjän syöttämät merkkijonot integer-muuttujiksi
                rows = int(opts.new[0])
                cols = int(opts.new[1])
                winNumber = int(opts.new[2])

                #Laudan koko
                board_size = rows * cols

                #Jos rivien tai sarakkeiden määrä on negatiivinen, aiheutetaan keskeytys
                if ((rows < 0) | (cols < 0)):
                    raise ValueError

                #Jos voittonumero on vääränlainen, aiheutetaan keskeytys
                #Voittonumeron täytyy olla suurempi tai yhtäsuuri kuin 1 tai suurempi kuin rivien ja sarakkeiden lukumäärä
                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError

                tiedosto = opts.file

                #Luodaan board_list ja flag_list - listat kuten aiemmin rivien ja sarakkeiden perusteella         
                board_list = list()
                for i in range(rows):
                    rivi = list()
                    for j in range(cols):
                        rivi.append("_")
                    board_list.append(rivi)

                flag_list = list()
                for i in range(rows):
                    line = list()
                    for j in range(cols):
                        line.append(False)
                    flag_list.append(line)

                print "Welcome to tic-tac-toe."

                #Asetetaan x aloittamaan peli
                player1 = True
                player2 = False

                        
            #Jatketaan tiedostossa olevaa peliä interaktiivisena    
            elif ((opts.new is None) & (opts.file is not None)):

                #Laskurit siirtojen määrille
                Xcount = 0
                Ocount = 0
                count = 0
                
                tiedosto = opts.file

                #Luetaan tarvittavat muuttujat tiedostosta
                [board_list, rows, cols, winNumber] = read_board(tiedosto)
                board_size = rows * cols

                #Jos voittonumero on vääränlainen, aiheutetaan keskeytys
                if ((winNumber == 0) | (winNumber == 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError

                #Luodaan flag_list - lista kuten edellä
                flag_list = list()
                for i in range(rows):
                    line = list()
                    for j in range(cols):
                        line.append(False)
                    flag_list.append(line)

                #Käydään tiedostosta läpi kuten aiemmin ja tarkastetaan onko siinä virheitä
                for i in range(rows):
                    for j in range(cols):
                        if (board_list[i][j] != "_"):
                            flag_list[i][j] = True
                            count = count + 1
                        if (board_list[i][j] == "x"):
                            Xcount = Xcount + 1
                        if (board_list[i][j] == "o"):
                            Ocount = Ocount + 1
                        if ((board_list[i][j] != "o") & (board_list[i][j] != "x") & (board_list[i][j] != "_")):
                            FileError = True

                #Jos virheitä ei löytynyt            
                if FileError == False:                   

                    #Jos siirtoja on yhtä paljon kuin laudassa paikkoja, asetetaan error todeksi
                    if (count == board_size):
                        error = True

                    #Tarkistetaan onko peli jo päättynyt    
                    [win, winX, win0] = check_win(board_list, winX, win0)

                    #Jos peli ei vielä päättynyt
                    if ((win == False) & (error == False)):
                        print "Welcome to tic-tac-toe."

                        #Tarkistetaan pelaajien vuorot
                        if Xcount == Ocount:
                            player1 = True
                            player2 = False
                            if win == False:
                                print "It's x's turn\n"
                        elif Xcount > Ocount:
                            player2 = True
                            player1 = False
                            if win == False:
                                print "It's o's turn\n"
                                                                  
            #Jos peli ei ole vielä päättynyt ja tiedostossa ei ollut virheitä
            if ((error == False) & (winX == False) & (win0 == False) & (FileError == False)):
                print_board(board_list)

                #Kysytään käyttäjiltä siirtoja niin kauan kunnes jompi kumpi voittaa tai lauta tulee täyteen
                while( (count < board_size) & (win == False)):

                    #Pyydetään käyttäjältä koordinaatteja
                    vastaus = raw_input("select coordinates: ")

                    #Hajotetaan käyttäjän syöte
                    temp = vastaus.split(' ')
                    
                    try:

                        #Muunnetaan käyttäjän syötteet integer-muuttujiksi
                        v1 = int(temp[0])
                        v2 = int(temp[1])

                        #Jos koordinaatit ovat negatiivisia, aiheutetaan keskeytys
                        if ((v1 < 0) | (v2 < 0)):
                            raise ValueError
                        
                        [board_list, player1, player2, count] = check_mark(v1, v2, player1, player2, flag_list, count)

                        #Tulostetaan lauta ruudulle
                        print_board(board_list)

                        #Jos haluttiin kirjoittaa peli tiedostoon
                        if opts.file is not None:
                            write_board(board_list, tiedosto)

                        #Tarkistetaan tuliko voitto
                        [win, winX, win0] = check_win(board_list, winX, win0)

                    #Tulostetaan virheilmoitus, jos koordinaatit olivat vääränlaisia    
                    except ValueError:
                        print "Wrong format for the coordinates!"
                        print_board(board_list)
                    except IndexError:
                        print "Wrong format for the coordinates!"
                        print_board(board_list)

                #Jos kumpikaan ei voittanut
                if win == False:
                    print "It's a draw! Game over."

                
                else:

                    #Jos x voitti
                    if(winX == True):
                        print "X wins!"

                    #Jos o voitti
                    else:
                        print "0 wins!"

            #Jos tiedostossa ilmeni virhe            
            elif FileError == True:
                print "Error reading file: %s" %tiedosto

            #Muussa tapauksessa peli oli jo päättynyt                  
            else:
                print "The game has ended. Start a new game if you like.\n"
                print_board(board_list)
                
        #Tulostetaan virheilmoitukset vääränlaisille riveille, sarakkeille tai voittonumerolle        
        except ValueError:
            
            print "Wrong format for the commandline parameters."           
            if ((rows < 0) | (cols < 0)):
                print "You inserted negative integer values for rows or columns."              
            if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                print "Incorrect win number. The win number must be larger than 1 and smaller than rows or columns."
    else:
        print "Wrong format for the commandline parameters."
        
#Jos käyttäjä keskeyttää pelin painamalla CTRL + C
except KeyboardInterrupt:
    print "\nYou stopped the game."





