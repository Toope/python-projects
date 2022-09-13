#By Tiia Leinonen, in fall 2017
#run: ipython miinaharava.py
#pick a (start new game), t (statistics) or q (quit)
#then pick the width, height and number of mines - in that order - and you're good to go

import haravasto    #haravasto by teacher Mika Oja
import random
import time

tila = {
    "kentta": None,
    "vuorot": None,
    "alku_aika": None,
    "loppu_aika": None,
    "ajankohta": None,
    "tulos": None, 
    "leveys": None,
    "korkeus": None,
    "miinat": None
    }

def kasittele_hiiri(x, y, nappi, muokkausnapit): 
    """Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä. Avaa ruudun/merkkaa ruudun lipulla."""
    try: 
        x = int(int(x) / 40)      #coordinates
        y = int(int(y) / 40)
        nappi = int(nappi)
        muokkausnapit = int(muokkausnapit)
        kentta = tila["kentta"]
        if nappi == haravasto.HIIRI_OIKEA:   #falg/flag off
            if kayttajan_kentta[y][x] == " ":  
                if tila["vuorot"] == 0: 
                    tila["alku_aika"] = time.time()   
                    tila["ajankohta"] = time.strftime("%d.%m.%Y - klo.%H.%M.%S", time.localtime())
                kayttajan_kentta[y][x] = "f"
                tila["vuorot"] += 1
            elif kayttajan_kentta[y][x] == "f": 
                if tila["vuorot"] == 0:
                    tila["alku_aika"] = time.time() 
                    tila["ajankohta"] = time.strftime("%d.%m.%Y - klo.%H.%M.%S", time.localtime())
                kayttajan_kentta[y][x] = " "
                tila["vuorot"] += 1
        elif nappi == haravasto.HIIRI_VASEN:  #open
            if tila["vuorot"] == 0:
                tila["alku_aika"] = time.time()
                tila["ajankohta"] = time.strftime("%d.%m.%Y - klo.%H.%M.%S", time.localtime())
            tila["vuorot"] += 1
            tulva = tulvataytto(kayttajan_kentta, x, y)  
        #winning the game
        tyhjat = 0
        for rivi in kayttajan_kentta:
            tyhjat += rivi.count(" ") + rivi.count("f")
        if tyhjat == tila["miinat"]:
            tila["tulos"] = "Voitto"
            tila["loppu_aika"] = time.time() 
            kirjoita_tiedostoon("miinaharava_tilastot", tilasto_lista())
            print("Voitit pelin!")  
            haravasto.lopeta()  

    except IndexError:   #for clicking the black area
        print("Tämä ei ole ruutu, tiedäthän?")
                           
def miinoita(kentta, jaljella, miinat):
    """Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin."""
    koordinaattiparit = random.sample(jaljella, miinat)
    for x, y in koordinaattiparit:
        kentta[y][x] = "x" 
   
def piirra_():
    """Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää ruudun näkymän päivitystä."""
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for indeksi_1, arvo in enumerate(kayttajan_kentta):
        for indeksi_2, avain in enumerate(arvo):
            x = indeksi_2 * 40
            y = indeksi_1 * 40
            haravasto.lisaa_piirrettava_ruutu(avain, x, y)
    haravasto.piirra_ruudut()
  
def tulvataytto(kayttajan_kentta, alku_x, alku_y):
    """Jos ruutu on tyhjä, tulvatäyttö. Jos ei, avaa yhden ruudun."""
    alku_x = int(alku_x)
    alku_y = int(alku_y)
    lista = [(alku_x, alku_y)]
    kentta = tila["kentta"]
    while not lista == []:
        koordinaatti = lista.pop() 
        x, y = koordinaatti
        if kayttajan_kentta[y][x] == "f": 
            return
        if kentta[y][x] == "x":    #mine, losing the game
            kayttajan_kentta[y][x] = kentta[y][x]
            tila["tulos"] = "Häviö"
            tila["loppu_aika"] = time.time() 
            kirjoita_tiedostoon("miinaharava_tilastot", tilasto_lista())
            print("Hävisit!")  
            haravasto.lopeta()
        elif kayttajan_kentta[y][x] == " " and kentta[y][x] == 0:   #flooding
            kayttajan_kentta[y][x] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        if x + i < 0 or y + j < 0 or( x + i == x and y + j == y):
                            continue
                        else:
                            if kentta[y + j][x + i] == 0:                
                                lista.append((x + i, y + j))
                            elif kentta[y][x] != "x" and kayttajan_kentta[y][x] != "f":  #you can't open flag or mine by flooding
                                kayttajan_kentta[y + j][x + i] = kentta[y + j][x + i]
                    except IndexError:
                        pass              
        else:  #number
            kayttajan_kentta[y][x] = kentta[y][x]

def main(kentta): 
    """Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen käsittelijät."""
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(len(kentta[0]) * 40,len(kentta) * 40)
    haravasto.aseta_piirto_kasittelija(piirra_)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()

def laske_miinat(x, y, kentta):
    """Laskee yhden ruudun ympärillä olevat miinat ja palauttaa niiden lukumäärän. Funktio toimii sillä oletuksella, että valitussa ruudussa ei ole miinaa - jos on, sekin lasketaan mukaan."""
    miinat = 0
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                if x + i < 0 or y + j < 0 or( x + i == x and y + j == y):
                    continue
                else:
                    if kentta[y + j][x + i] == "x":
                        miinat += 1
            except IndexError:
                pass
    return(miinat)
    
def kysy_kentta_basics():
    """ Tämä funktio kysyy pelaajalta pelin alussa kentän koon ja miinojen lukumäärän ja tarkistaa syötteen oikeellisuuden. Palauttaa arvot. """
    while True: #ask width and length 
        try:
            leveys = int(input("Anna kentän leveys: "))
            korkeus = int(input("Anna kentän korkeus: "))
            
            if leveys < 1 or korkeus < 1:
                print("Liian pieni kenttä, kokeile isompaa!")
            elif leveys > 100 or korkeus > 100:    #limits for the field
                print("Kokeile jotakin pienempää, kiitos!")
            elif leveys >= 1 and korkeus >= 1:  
                miinat = int(input("Anna miinojen lukumäärä: "))
                if miinat >= (leveys * korkeus):
                    print("Miinoja on enemmän kuin ruutuja! Kokeile uudestaan!")
                elif miinat <= 0:
                    print("Enemmän miinoja, kiitos.")
                else:
                    break
        except ValueError:
            print("Anna vastaukset kokonaislukuina.")
    tila["leveys"] = leveys
    tila["korkeus"] = korkeus
    tila["miinat"] = miinat
    return(leveys, korkeus, miinat)
    
def luo_kentta(leveys, korkeus, miinat):
    """Luo "taustalle" kentän."""
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
    jaljella = []
    for y in range(korkeus):
        for x in range(leveys):
            jaljella.append((x, y))  
    miinoita(kentta, jaljella, miinat)  #mines
    for y in range(korkeus):  #numbers
        for x in range(leveys):
            if kentta[y][x] == " ":
                kentta[y][x] = laske_miinat(x, y, kentta)
    tila["kentta"] = kentta           
    
#save the information
def tilasto_lista():
    """Listaa kaikki tilastoon menevät tiedot."""
    lista = []
    ajankohta = tila["ajankohta"] 
    kesto_min = int((tila["loppu_aika"] - tila["alku_aika"]) / 60)
    vuorot = tila["vuorot"]
    tulos = tila["tulos"]
    leveys = tila["leveys"]
    korkeus = tila["korkeus"]
    miinat = tila["miinat"]
    
    monikko = (ajankohta, kesto_min, vuorot, tulos, leveys, korkeus, miinat)
    lista.append(monikko)
    return(lista)
    
def kirjoita_tiedostoon(tiedosto, lista):
    """Kirjoittaa tilastot tiedostoon."""
    try:
        with open(tiedosto, "a") as kohde:
            for monikko in lista:
                kohde.write("{},{},{},{},{},{},{}\n".format(monikko[0], monikko[1], monikko[2], monikko[3], monikko[4], monikko[5], monikko[6]))
    except IOError:
        pass
        
def nayta_tilasto(tiedosto):
    """Lukee ja avaa tiedoston."""
    try:
        with open(tiedosto) as lahde:
            for rivi in lahde.readlines(): 
                lista = rivi.strip("\n").split(",")
                print("Pelin ajankohta: {}. Kesto: {} min, {} vuoroa. Lopputulos: {}, kun kentän koko {}x{} ruutua ja miinoja {} kpl.\n".format(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6]))
    except IOError:
        print("Tilastoja ei vielä ole, pelaa peli ensin.")
        
#main
if __name__ == "__main__":
    print("Valitse a = aloita peli, t = tilastot tai q = lopeta.")
    #~40x20 field is the maximum I'd recommend
    while True:
        valinta = input("Valinta(a,t tai q): ")
        if valinta == "q":
            break
        elif valinta == "t":
            nayta_tilasto("miinaharava_tilastot")
        elif valinta == "a":
            leveys, korkeus, miinat = kysy_kentta_basics()
            tila["kentta"] == luo_kentta(leveys, korkeus, miinat)
            kayttajan_kentta = []
            for rivi in range(korkeus):
                kayttajan_kentta.append([])
                for sarake in range(leveys):
                    kayttajan_kentta[-1].append(" ")
            tila["vuorot"] = 0
            main(kayttajan_kentta)
        else:
            print("Virheellinen syöte!")