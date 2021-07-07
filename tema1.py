"""
Cazan Bogdan-Marian, 323CB, Tema1 Analiza Algoritmilor
"""

import sys
"""
Functie care citeste codificarea unei masini Turing
Returneaza atat codificarea tranzitiilor, adica codifTM, cat si starile
Tranzitiile sunt reprezentate sub forma unor dictionare:
    - key este un tuple, care reprezinta cele doua variabile ale lui delta, iar
    - valoarea este de asemenea un tuple, care reprezinta in sine valoarea
    functiei delta in respectivul key
Starile sunt si ele de asemenea intr-un dictionar, unde key este numarul starii,
iar valoarea este de tip boolean: True daca este stare finala si False altfel.    
"""
def readTM():
    numberStates = int(input())
    codifTM = {}
    states = {}
    for i in range(0, numberStates):
        states.update({i : False})

    finalStates = (input().split())
    if finalStates[0] != "-":
        for i in range(0, len(finalStates)):
            states.update({int(finalStates[i]) : True})
            
    for line in sys.stdin:
        line = line.split()
        key = (line[0], line[1])
        value = (line[2], line[3], line[4])
        codifTM.update({key : value})
          
    return codifTM, states

"""
Functie care nu citeste o configuratie si o returneaza sub forma unei liste,
pentru a se putea opera mai usor pe aceasta
"""
def readConfigurations():
    configurations = []
    config = input().split()
    for elem in config:
        elem = elem.strip("()").split(",")
        configurations.append(elem)
    return configurations

"""
Functie care face trecerea dintr-o configuratie actuala primita ca si parametru,
intr-o noua configuratie, in functie de tabelul de tranzitii al MT-ului dat
De remarcat ca aceasta functie este de fapt functia STEP din cadrul temei,
numai ca am considerat ca trebuie sa aiba un nume mai sugestiv, intrucat o vom
folosi si mai departe
"""
def getNewConfiguration(configuration, codifTM):
    currDeltaInput = (configuration[1], configuration[2][0])
    #daca nu exista o noua configuratie, returneaza fals
    if currDeltaInput not in codifTM:
        return False
    currDeltaOutput = codifTM[currDeltaInput]
    configuration.pop(1)
    configuration.insert(1, currDeltaOutput[0])
    
    ##se realizeaza o deplasare in functie de directia data: H, L sau R
    #pentru Hold, se va trece la o noua stare si se va schimba valoarea de pe
    #cursor, fara ca acesta sa fie mutat
    if currDeltaOutput[2] == 'H':
        newLeftWord = currDeltaOutput[1] + configuration[2][1:]
        configuration.pop(2)
        configuration.append(newLeftWord)
    
    #pentru Right, se trece intr-o noua stare si se modifica prima litera din
    #dreapta cursorului
    elif currDeltaOutput[2] == 'R':
        newLeftWord = configuration[0] + currDeltaOutput[1]
        configuration.pop(0)
        configuration.insert(0, newLeftWord)
        newRightWord = configuration[2][1:]
        if newRightWord == "":
            newRightWord = "#"
        configuration.pop(2)
        configuration.append(newRightWord)
    
    #pentru Left, se intampla la fel ca la Right (in mare parte)
    else:
        newRightWord = configuration[0][len(configuration[0]) - 1] +\
            currDeltaOutput[1]  + configuration[2][1:]
        configuration.pop(2)
        configuration.append(newRightWord)
        newLeftWord = configuration[0][0:len(configuration[0]) - 1]
        if newLeftWord == "":
            newLeftWord = "#"
        configuration.pop(0)
        configuration.insert(0, newLeftWord)
        
    return [configuration[0], configuration[1],\
        configuration[2]]

"""
Functie care rezlova atat task-ul accept, cat si cel de k_accept, in felul
urmator: daca are de rezolvat accept, atunci va primi ca si parametru K o
valoare negativa, stiind ca se garanteaza terminarea; pentru cazul k_accept,
atunci k nu va fi nimeni altul decat numarul de pasi in care se doreste
efectuarea acceptarii
"""
def accept(word, codifTM, states, k):
    oldConfiguration = ["#", '0', word]
    while k != 0:
        newConfiguration = getNewConfiguration(oldConfiguration, codifTM)
        if newConfiguration == False:
            return False
        else:
            oldConfiguration = newConfiguration
            k -= 1
        if states[int(oldConfiguration[1])] == True:
            return True
    return False
    
"""
Functia de main, in care am facut mici prelucrari in cadrul programlui, cum ar
fi selectarea task-ului care trebuie rezlovat citirea unor mici date de la
inceputul programului, si, nu in ultimul rand, afisarea/printarea rezultatelor
dorite la stdout
"""
def main():
    taskType = input()
    
    #prelucrare input/output pentru step
    if taskType == "step":
        configurations = readConfigurations()
        [codifTM, states] = readTM()
        for config in configurations:
            newConfig = getNewConfiguration(config, codifTM)
            if newConfig == False:
                print(False, end=" ")
                continue
            print("(", end="")
            print(newConfig[0], newConfig[1],\
                newConfig[2], sep=",", end="")
            if config != configurations[len(configurations) - 1]:
                print(")", end=" ")
            else:
                print(")", end="")
                
    #prelucrare input/output pentru accept
    elif taskType == "accept":
        words = input().split()
        [codifTM, states] = readTM()
        for i in range(0, len(words)):
            if i == len(words) - 1:
                print(accept(words[i], codifTM, states, -1), end="")
            else:
                print(accept(words[i], codifTM, states, -1), end=" ")
                
    #prelucrare input/output pentru k_accept
    else:
        lineOfWords = input().split()
        [codifTM, states] = readTM()
        for i in range(0, len(lineOfWords)):
            wordAndK = lineOfWords[i].split(",")
            if i == len(lineOfWords) - 1:
                print(accept(wordAndK[0], codifTM,\
                    states, int(wordAndK[1])), end="")
            else:
                print(accept(wordAndK[0], codifTM,\
                    states, int(wordAndK[1])), end=" ")                
            
if __name__ == '__main__':
    main()