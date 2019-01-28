# -*- coding: iso8859-15 -*-
import sys



###############Funktioiden ja muuttujien m��rittely##################




#-------------Komentoriviargumenttien prosessointi----------------------------

#K�ytin mallina seuraavan linkin esimerkki�: http://docs.python.org/library/optparse.html

def process_args():
    from optparse import OptionParser
    parser = OptionParser()
    #Luodaan komentoriviparametri "-f" tai "--file", joka tallettaa arvon opts.file kohteeseen
    parser.add_option("-f", "--file", action="store", dest="file",
                      help="Read a game situation from FILE.")

    #Luodaan komentoriviparametri "-n" tai "--new", joka tallettaa arvon opts.new kohteeseen
    #Argumenttien m��r�n t�ytyy olla 3.
    parser.add_option("-n", "--new", action="store", dest="new", nargs = 3,
                      help="Start a new game")

    #Luodaan komentoriviparametri "-i" tai "--interactive", joka tallettaa arvon opts.interactive kohteeseen.
    #Kyseess� on boolean-muuttuja, jolla on 2 eri arvoa (True tai False).
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive",
                      help="Play game in interactive mode.")
    return parser.parse_args()

(opts, args) = process_args()

if opts.interactive == True:
    interactive = True
else:
    interactive = False

#Laskuri laudalle sy�tettyjen merkkien m��r�st�     
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

    #K�yd��n tiedosto l�pi ensimm�isen kerran, jolloin otetaan talteen rivien ja sarakkeiden lukum��r�    
    tiedosto1 = open('%s.txt' %tiedosto, 'r') # avataan tiedosto lukemista varten

    #Laskuri tiedoston rivien m��r�lle
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

    #Pelilaudan rivien m��r� saadaan v�hent�m�ll� tiedoston rivien m��r�st� 1.
    #Tiedostossa viimeinen rivi kertoo voittoon tarvittavien per�kk�isten merkkien m��r�n.    
    rows = count1 - 1

    
    #K�yd��n tiedosto l�pi toisen kerran ja lis�t��n board_list - listaan tiedoston alkiot
    #eli X:n ja 0:n sijoittumiset pelilaudalla. Lis�ksi otetaan talteen tarvittava voittonumero.
    
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

    #Palautetaan board_list, rivien ja sarakkeiden lukum��r� ja voittonumero
    return board_list, rows, cols, winNro

#-------------Tiedostoon kirjoittaminen----------------------------    

#T�m�n funktion tarkoituksena on kirjoittaa pelilaudan tilanne tiedostoon.
#Sen parametreina on board_list - lista, joka sis�lt�� pelilaudan tilanteen,
#ja tiedosto mihin pelitilanne halutaan kirjoittaa.

def write_board(board_list, tied):

    #Avataan tiedosto kirjoitusta varten
    f = open("%s.txt" %tied, 'w')

    #Kirjoitetaan riveitt�in ja sarakkeittain tiedostoon board_list:n alkiot
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


#-------------Voittoyhdistelm�n tarkistus----------------------------

#Funktio tarkistaa onko laudalla tarvittava m��r� merkkej� per�kk�in
#voittoa varten.

        
def check_win(board_list, winX, win0):

    #Luodaan X:lle ja 0:lle voittoon tarvittavat listat ja alustetaan kaikki alkiot ykk�siksi.

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
    #oikeaan yl�nurkkaan menevien merkkien tarkistuslistat
        
    #Xwin_listCross2 ja Owin_listCross2 ovat viistoon oikeasta alanurkasta
    #vasempaan yl�nurkkaan menevien merkkien tarkituslistat
    
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
        
    #K�yd��n board_list l�pi riveitt�in ja sarakkeittain
    for i in range(rows):
        for j in range(cols):
            if j != 0:
                
                #Tarkistetaan pystyrivien per�kk�iset merkit
                if board_list[i][j] == board_list[i][j-1] == "x":
                    Xwin_listHor[i]= Xwin_listHor[i] + 1
                elif board_list[i][j] == board_list[i][j-1] == "o":
                    Owin_listHor[i]= Owin_listHor[i] + 1
                              
            if i != 0:

                #Tarkistetaan vaakarivien per�kk�iset merkit
                if board_list[i][j] == board_list[i-1][j] == "x":
                    Xwin_listVer[j] = Xwin_listVer[j] + 1
                elif board_list[i][j] == board_list[i-1][j] == "o":
                    Owin_listVer[j] = Owin_listVer[j] + 1
                    
            # Tarkistetaan viistoon vasen alanurkka -> oikea yl�nurkka menev�t per�kk�iset merkit
            for k in range(cols-1):
                m = k + 1
                if ((i > k) & (j < (cols-m))):

                    #Jos vierekk�in on kaksi samanlaista x-merkki� kasvatetaan laskuria yhdell�
                    if ((board_list[i][j] == "x") & (board_list[i-m][j+m] == "x")):
                        Xwin_listCross1[i][j] = Xwin_listCross1[i][j] + 1

                    #Muussa tapauksessa hyp�t��n pois silmukasta eik� jatketa laskurin kasvattamista
                    else:
                        if ((board_list[i][j] == "x") & (board_list[i-m][j+m] == "o")):
                            break
                        elif ((board_list[i][j] == "x") & (board_list[i-m][j+m] == "_")):
                            break
                        
                    #Jos vierekk�in on kaksi samanlaista o-merkki� kasvatetaan laskuria yhdell�    
                    if ((board_list[i][j] == "o") & (board_list[i-m][j+m] == "o")):
                        Owin_listCross1[i][j] = Owin_listCross1[i][j] + 1

                    #Muussa tapauksessa hyp�t��n pois silmukasta eik� jatketa laskurin kasvattamista
                    else:
                        if ((board_list[i][j] == "o") & (board_list[i-m][j+m] == "x")):
                            break
                        elif ((board_list[i][j] == "o") & (board_list[i-m][j+m] == "_")):
                            break

                        
            # Tarkistetaan viistoon Oikea alanurkka -> vasen yl�nurkka menev�t per�kk�iset merkit          
            for w in range(cols-1):
                n = w + 1
                if((i > w) & (j > w)):

                    #Jos vierekk�in on kaksi samanlaista x-merkki� kasvatetaan laskuria yhdell�
                    if ((board_list[i][j] == "x") & (board_list[i-n][j-n] == "x")):
                        Xwin_listCross2[i][j] = Xwin_listCross2[i][j] + 1

                    #Muussa tapauksessa hyp�t��n pois silmukasta eik� jatketa laskurin kasvattamista
                    else:
                        if ((board_list[i][j] == "x") & (board_list[i-n][j-n] == "o")):
                            break
                        elif((board_list[i][j] == "x") & (board_list[i-n][j-n] == "_")):
                            break
                        
                    #Jos vierekk�in on kaksi samanlaista o-merkki� kasvatetaan laskuria yhdell�      
                    if ((board_list[i][j] == "o") & (board_list[i-n][j-n] == "o")):
                        Owin_listCross2[i][j] = Owin_listCross2[i][j] + 1
            
                    #Muussa tapauksessa hyp�t��n pois silmukasta eik� jatketa laskurin kasvattamista    
                    else:
                        if ((board_list[i][j] == "o") & (board_list[i-n][j-n] == "x")):
                            break
                        elif((board_list[i][j] == "o") & (board_list[i-n][j-n] == "_")):
                            break
                             
      
    #K�yd��n l�pi tarkistuslistat.
    #Jos alkion m��r� = voittonumero, asetetaan vastaava X:n tai 0:n
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
    #Muussa tapauksessa asetetaan yleinen voitto ep�todeksi.
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

#Funktio tarkistaa onko k�ytt�j�n sy�tt�mien koordinaattien paikalla jo merkki.
#Jos paikalla ei ole merkki�, lis�t��n siihen "x" tai "o" riippuen pelaajan vuorosta.
    
#Funktion sis��ntuloina ovat koordinaatit (v1, v2), pelaajien boolean-muuttujat (p1,p2),
#boolean tyyppinen flag-lista, joka kertoo onko koordinaatin paikalla jo merkki sek� laskuri c
#jo sy�tettyjen merkkien m��r�� varten.

#Boolean-muuttujat p1 (x) ja p2 (o) kertovat kumman merkin vuoro on.
    
def check_mark(v1, v2, p1, p2, flag, c):
    try:
        x = v1
        y = v2

        #Jos paikalla ei ole viel� merkki�
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
                
                #Lis�t��n laskuria yhdell�
                c = c + 1

                #Palautetaan p��ohjelmalle board_list, p1, p2 ja laskuri c
                return board_list, p1, p2, c
            
            #Jos on o:n vuoro
            elif p2 == True:
                board_list[x][y] = "o"

                #Asetetaan vuoro x:lle
                p1 = True
                p2 = False
                
                #Asetetaan flag-listaan arvo True eli paikka on varattu
                flag[x][y] = True
                
                #Lis�t��n laskuria yhdell�
                c = c + 1

                #Palautetaan p��ohjelmalle board_list, p1, p2 ja laskuri c
                return board_list, p1, p2, c
            
        #Jos paikalla on jo merkki, tulostetaan virheilmoitus
        else:
            print "That square is already taken."
            return board_list, p1, p2, c
        
    #Jos k�ytt�j� sy�tti jotain muuta kuin numeroita, tulostetaan virheilmoitus
    except ValueError:
        print "Wrong format for the coordinates!"
        return board_list, p1, p2, c
    
    #Jos k�ytt�j�n sy�tt�m�t koordinaatit menev�t pelilaudan ulkopuolelle, tulostetaan virheilmoitus
    except IndexError:
        print "Your selection goes out of range!"
        return board_list, p1, p2, c
    

###############P��ohjelma##################


try:
    #-------------Komentorivimoodi----------------------------

    if interactive == False:
        
        # Luodaan uusi peli m��r�ttyyn tiedostoon
        
        if ((opts.file is not None) & (opts.new is not None)):
            tiedosto = opts.file

            try:

                #Muunnetaan k�ytt�j�n sy�tt�m�t merkkijonot integer-muuttujiksi
                rows = int(opts.new[0])
                cols = int(opts.new[1])
                winNumber = int(opts.new[2])

                #Jos rivien tai sarakkeiden m��r� on negatiivinen, aiheutetaan keskeytys
                if ((rows < 0) | (cols < 0)):
                    raise ValueError

                #Jos voittonumero on v��r�nlainen, aiheutetaan keskeytys
                #Voittonumeron t�ytyy olla suurempi tai yht�suuri kuin 1 tai suurempi kuin rivien ja sarakkeiden lukum��r�
                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError
                
                #Luodaan board_list-lista, joka pit�� sis�ll��n laudan merkit. Alussa asetetaan jokaiselle paikalle "_".
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
                
            
        # Tehd��n haluttu siirto tiedostossa olevaan peliin
            
        elif ((opts.file is not None) & (opts.new is None)):
                      
            tiedosto = opts.file
            board_list = list()
            try:

                #Luetaan tiedostosta board_list, rivien ja sarakkeiden lkm sek� voittonumeron arvon
                [board_list, rows, cols, winNumber] = read_board(tiedosto)

                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError

                #Laudan koko
                board_size = rows * cols

                #Laskuri laudalle sy�tettyjen merkkien m��r�st�  
                count = 0

                #Laskuri laudalle sy�tettyjen "x"-merkkien m��r�st�  
                Xcount = 0

                #Laskuri laudalle sy�tettyjen "o"-merkkien m��r�st�  
                Ocount = 0

                #Luodaan flag_list-lista, joka kertoo onko laudan paikka jo k�yt�ss�
                flag_list = list()
                for i in range(rows):
                    line = list()
                    for j in range(cols):
                        line.append(False)
                    flag_list.append(line)
                      
                #K�yd��n l�pi tiedostosta haettu board_list
                for i in range(rows):
                    for j in range(cols):

                        #Jos paikalla on "x" tai "o" asetetaan koordinaattien flag_list arvo todeksi (True) ja
                        #kasvatetaan laskuria yhdell�.
                        if (board_list[i][j] != "_"):
                            flag_list[i][j] = True
                            count = count + 1
                            
                        #Jos paikassa on "x" kasvatetaan x:n laskuria yhdell�
                        if (board_list[i][j] == "x"):
                            Xcount = Xcount + 1
                            
                        #Jos paikassa on "o" kasvatetaan o:n laskuria yhdell�
                        if (board_list[i][j] == "o"):
                            Ocount = Ocount + 1

                        #Jos paikassa on jotain muuta, asetetaan FileError-muuttuja todeksi.
                        if ((board_list[i][j] != "o") & (board_list[i][j] != "x") & (board_list[i][j] != "_")):
                            FileError = True

                #Jos x:n merkkien m��r� > (o:n merkkien m��r� + 1) tai jos o:n merkkien m��r� > x:n merkkien m��r�
                #Ohjelmassa oletetaan aina, ett� x aloittaa jokaisen pelin ensimm�isen�
                if ((Xcount > (Ocount +1)) | (Ocount > Xcount)):
                    FileError = True;

                #Suoritetaan tarvittavat toimenpiteet, jos tiedostosta ei l�ytynyt virheit�            
                if FileError == False:

                    #M��ritet��n kumman pelaajan vuoro on
                    if Xcount == Ocount:
                        player1 = True
                        player2 = False
                    elif Xcount > Ocount:
                        player2 = True
                        player1 = False

                    #Tarkistetaan onko peli p��ttynyt jo aiemmin   
                    [win, winX, win0] = check_win(board_list, winX, win0)

                    #Jos peli ei ole viel� loppunut tai lauta ei ole viel� t�ynn�    
                    if ((count < board_size) & (winX == False) & (win0 == False)):

                        #Kun halutaan tarkastaa pelin tilanne tekem�tt� siirtoa
                        if (len(args) == 0):    
                            print_board(board_list)
                            if player1 == True:
                                print "It's x's turn"
                            else:
                                print "It's o's turn"

                        #Kun tehd��n haluttu siirto
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

                                #Tarkistetaan tuliko viel� voitto
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
                        
                    #Muussa tapauksessa peli on jo p��ttynyt   
                    else:
                        print "The game has ended. Start a new game if you like.\n"
                        print_board(board_list)

                #Tiedostosta l�ytyi virhe, tulostetaan virheilmoitus
                else:
                    print "Error reading file: %s" %tiedosto

            #Tulostetaan virheilmoitus, kun tiedostoa ei ole olemassa
            except IOError:
                print "I/O error: no such file '%s'" %tiedosto

            #Tulostetaan virheilmoitukset v��r�nlaisille rivien, sarakkeiden ja voittonumeron argumenteille
            except ValueError:
                print "Wrong format for the commandline parameters."
                if ((rows < 0) | (cols < 0)):
                    print "You inserted negative integer values for rows or columns."             
                if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                    print "Incorrect win number. The win number must be larger than 1 and smaller than rows or columns."
                    
        #Tulostetaan virheilmoitus v��r�nlaisille komentoriviparametreille        
        else:
            print "Wrong format for the commandline parameters."
                

    #-------------Interaktiivinen moodi----------------------------
            
    elif ((interactive == True) & (opts.new is not None) | ((interactive == True) & (opts.new is None) & (opts.file is not None))):

        try:

            # Aloitetaan t�ysin uusi peli
            if (opts.new is not None):

                #Muunnetaan k�ytt�j�n sy�tt�m�t merkkijonot integer-muuttujiksi
                rows = int(opts.new[0])
                cols = int(opts.new[1])
                winNumber = int(opts.new[2])

                #Laudan koko
                board_size = rows * cols

                #Jos rivien tai sarakkeiden m��r� on negatiivinen, aiheutetaan keskeytys
                if ((rows < 0) | (cols < 0)):
                    raise ValueError

                #Jos voittonumero on v��r�nlainen, aiheutetaan keskeytys
                #Voittonumeron t�ytyy olla suurempi tai yht�suuri kuin 1 tai suurempi kuin rivien ja sarakkeiden lukum��r�
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

                        
            #Jatketaan tiedostossa olevaa peli� interaktiivisena    
            elif ((opts.new is None) & (opts.file is not None)):

                #Laskurit siirtojen m��rille
                Xcount = 0
                Ocount = 0
                count = 0
                
                tiedosto = opts.file

                #Luetaan tarvittavat muuttujat tiedostosta
                [board_list, rows, cols, winNumber] = read_board(tiedosto)
                board_size = rows * cols

                #Jos voittonumero on v��r�nlainen, aiheutetaan keskeytys
                if ((winNumber == 0) | (winNumber == 1) | ((winNumber > rows) & (winNumber > cols))):
                    raise ValueError

                #Luodaan flag_list - lista kuten edell�
                flag_list = list()
                for i in range(rows):
                    line = list()
                    for j in range(cols):
                        line.append(False)
                    flag_list.append(line)

                #K�yd��n tiedostosta l�pi kuten aiemmin ja tarkastetaan onko siin� virheit�
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

                #Jos virheit� ei l�ytynyt            
                if FileError == False:                   

                    #Jos siirtoja on yht� paljon kuin laudassa paikkoja, asetetaan error todeksi
                    if (count == board_size):
                        error = True

                    #Tarkistetaan onko peli jo p��ttynyt    
                    [win, winX, win0] = check_win(board_list, winX, win0)

                    #Jos peli ei viel� p��ttynyt
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
                                                                  
            #Jos peli ei ole viel� p��ttynyt ja tiedostossa ei ollut virheit�
            if ((error == False) & (winX == False) & (win0 == False) & (FileError == False)):
                print_board(board_list)

                #Kysyt��n k�ytt�jilt� siirtoja niin kauan kunnes jompi kumpi voittaa tai lauta tulee t�yteen
                while( (count < board_size) & (win == False)):

                    #Pyydet��n k�ytt�j�lt� koordinaatteja
                    vastaus = raw_input("select coordinates: ")

                    #Hajotetaan k�ytt�j�n sy�te
                    temp = vastaus.split(' ')
                    
                    try:

                        #Muunnetaan k�ytt�j�n sy�tteet integer-muuttujiksi
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

                    #Tulostetaan virheilmoitus, jos koordinaatit olivat v��r�nlaisia    
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

            #Muussa tapauksessa peli oli jo p��ttynyt                  
            else:
                print "The game has ended. Start a new game if you like.\n"
                print_board(board_list)
                
        #Tulostetaan virheilmoitukset v��r�nlaisille riveille, sarakkeille tai voittonumerolle        
        except ValueError:
            
            print "Wrong format for the commandline parameters."           
            if ((rows < 0) | (cols < 0)):
                print "You inserted negative integer values for rows or columns."              
            if ((winNumber <= 1) | ((winNumber > rows) & (winNumber > cols))):
                print "Incorrect win number. The win number must be larger than 1 and smaller than rows or columns."
    else:
        print "Wrong format for the commandline parameters."
        
#Jos k�ytt�j� keskeytt�� pelin painamalla CTRL + C
except KeyboardInterrupt:
    print "\nYou stopped the game."





