print("Benvenuto nel mio bar!") # Saluta il cliente e chiedi il suo nome
nome = input("Come ti chiami? ")
risposta = input(f"Ciao {nome}, cosa ti piacerebbe bere? ") # Chiedi al cliente se vuole bere alcolici o analcolici
if risposta == "alcolici": # Se il cliente vuole bere alcolici, chiedi la sua età
    print("Aspetta, prima devo sapere quanti anni hai.") # Chiedi l'età del cliente
    eta = int(input("Quanti anni hai? ")) # Controlla se il cliente è maggiorenne o minorenne
    if eta < 18: # Se il cliente è minorenne, non servirlo alcolici
        print("Mi dispiace, non posso servirti alcolici perché sei minorenne.")
    else: # Se il cliente è maggiorenne, mostrargli il menu degli alcolici e chiedigli cosa vuole ordinare
        print("Possiamo servirti alcolici, ecco il nostro menu:") # Mostra il menu degli alcolici
        alcolici = ["birra", "vino", "cocktail"] # Crea una lista di alcolici e la stampa
        for alcolico in alcolici: # Stampa ogni alcolico nella lista insieme a print(alcolico)
            print(alcolico)
        ordine = input("Cosa vuoi ordinare tra gli alcolici che abbiamo? ") # Chiedi al cliente cosa vuole ordinare tra gli alcolici offerti
        if ordine in alcolici: # Se il cliente ordina un alcolico che abbiamo, servilo e ringrazialo
            print("Ecco a te. Grazie e buona giornata!")
        else: # Se il cliente ordina un alcolico che non abbiamo, scusati e digli che non lo abbiamo
            print("Mi dispiace, non abbiamo quello che vuoi ordinare.")
elif risposta == "analcolici": # Se il cliente vuole bere analcolici, mostrargli il menu degli analcolici e chiedigli cosa vuole ordinare
    print("Ecco il nostro menu di analcolici:")
    analcolici = ["acqua", "succo di frutta", "bibite gassate"] # Crea una lista di analcolici e la stampa
    for analcolico in analcolici: # Stampa ogni analcolico nella lista insieme a print(analcolico)
        print(analcolico)
    ordine = input("Cosa vuoi ordinare tra gli analcolici che abbiamo? ") # Chiedi al cliente cosa vuole ordinare tra gli analcolici offerti
    if ordine in analcolici: # Se il cliente ordina un analcolico che abbiamo, servilo e ringrazialo
        print("Ecco a te. Grazie e buona giornata!")
    else: # Se il cliente ordina un analcolico che non abbiamo, scusati e digli che non lo abbiamo
        print("Mi dispiace, non abbiamo quello che vuoi ordinare.")
else: # Se il cliente non vuole bere alcolici o analcolici, chiedigli se vuole qualcosa da mangiare
    risposta2 = input("Vuoi qualcosa da mangiare? ")
    if risposta2 == "sì": # Se il cliente vuole mangiare, chiedigli se preferisce dolce o salato
        risposta3 = input("Dolce o salato? ")
        if risposta3 == "dolce": # Se il cliente preferisce dolce, mostrargli il menu dei dolci e chiedigli cosa vuole ordinare
            print("Ecco il nostro menu di dolci:")
            dolci = ["torta", "gelato", "biscotti"] # Crea una lista di dolci e la stampa
            for dolce in dolci: # Stampa ogni dolce nella lista insieme a print(dolce)
                print(dolce)
            ordine = input("Cosa vuoi ordinare tra i dolci che abbiamo? ") # Chiedi al cliente cosa vuole ordinare tra i dolci offerti
            if ordine in dolci: # Se il cliente ordina un dolce che abbiamo, servilo e ringrazialo
                print("Ecco a te. Grazie e buona giornata!")
            else: # Se il cliente ordina un dolce che non abbiamo, scusati e digli che non lo abbiamo
                print("Mi dispiace, non abbiamo quello che vuoi ordinare.")
        elif risposta3 == "salato": # Se il cliente preferisce salato, mostrargli il menu dei salati e chiedigli cosa vuole ordinare
            print("Ecco il nostro menu di salati:")
            salati = ["panino", "pizza", "patatine"] # Crea una lista di salati e la stampa
            for salato in salati: # Stampa ogni salato nella lista insieme a print(salato)
                print(salato)
            ordine = input("Cosa vuoi ordinare tra i salati che abbiamo? ") # Chiedi al cliente cosa vuole ordinare tra i salati offerti
            if ordine in salati: # Se il cliente ordina un salato che abbiamo, servilo e ringrazialo
                print("Ecco a te. Grazie e buona giornata!")
            else: # Se il cliente ordina un salato che non abbiamo, scusati e digli che non lo abbiamo
                print("Mi dispiace, non abbiamo quello che vuoi ordinare.")
    # Se il cliente non vuole mangiare
    else:
        print("Va bene, grazie per essere venuto al nostro bar. Buona giornata!")

# Attende un input prima di chiudere il programma
input("Premi un tasto per uscire.")
