# Benvenuto nel programma del bar PyDrinks&Snacks
print("Benvenuto nel bar PyDrinks&Snacks!")

# Chiedi all'utente cosa preferisce ordinare
risposta1 = input("Ti piacerebbe ordinare da bere o da mangiare?")

# Se l'utente vuole ordinare da bere
if risposta1 == "da bere":
    # Chiedi se preferisce alcolici o analcolici
    risposta2 = input("Preferisci una bevanda alcolica o analcolica?")

    # Se vuole una bevanda alcolica
    if risposta2 == "alcolica":
        # Controllo dell'età per gli alcolici
        print("Devo sapere se sei maggiorenne per poterti servire una bevanda alcolica.")
        eta = int(input("Quanti anni hai?"))

        # Se l'utente è minorenne, non può ordinare alcolici
        if eta < 18:
            print("Sei minorenne, mi dispiace ma non posso servirti una bevanda alcolica.")
        else:
            # L'utente è maggiorenne, quindi può ordinare alcolici
            print("Sei maggiorenne, ecco il nostro menù di alcolici")
            alcolici = ["birra", "vino", "cocktail"]

            # Mostra TUTTI gli elementi del menù prima di chiedere l'ordine
            for alcolico in alcolici:
                print(alcolico)

            # Ora che il menù è completo, chiedi cosa ordinare
            ordine = input("Cosa desideri ordinare?")

            # Continua a chiedere finché l'utente non sceglie un elemento valido
            while ordine not in alcolici:
                print("Mi dispiace, non abbiamo questo alcolico. Per favore scegli tra", alcolici)
                ordine = input("Cosa desideri ordinare?")

            # Ordine valido confermato
            print("Hai ordinato", ordine, "ottima scelta!")
    elif risposta2 == "analcolica":
        # L'utente vuole una bevanda analcolica
        print("Ecco il nostro menù di bevande analcoliche")
        analcolici = ["acqua", "succo di frutta", "bibita gassata"]

        # Mostra TUTTI gli elementi del menù prima di chiedere l'ordine
        for analcolico in analcolici:
            print(analcolico)

        # Ora che il menù è completo, chiedi cosa ordinare
        ordine = input("Cosa desideri ordinare?")

        # Continua a chiedere finché l'utente non sceglie un elemento valido
        while ordine not in analcolici:
            print("Mi dispiace, non abbiamo questa bevanda. Per favore scegli tra", analcolici)
            ordine = input("Cosa desideri ordinare?")

        # Ordine valido confermato
        print("Hai ordinato", ordine, "ottima scelta!")
elif risposta1 == "da mangiare":
    # L'utente vuole ordinare del cibo
    print("Ecco il nostro menù di snack")
    snacks = ["patatine", "popcorn", "noccioline", "cioccolato", "caramelle"]

    # Mostra TUTTI gli elementi del menù prima di chiedere l'ordine
    for snack in snacks:
        print(snack)

    # Ora che il menù è completo, chiedi cosa ordinare
    ordine = input("Cosa desideri ordinare?")

    # Continua a chiedere finché l'utente non sceglie un elemento valido
    while ordine not in snacks:
        print("Mi dispiace, non abbiamo questo snack. Per favore scegli tra", snacks)
        ordine = input("Cosa desideri ordinare?")

    # Ordine valido confermato
    print("Hai ordinato", ordine, "ottima scelta!")
else:
    # Se l'utente non ha risposto correttamente, continua a chiedere
    while True:
        print("Mi dispiace, non ho capito la tua risposta. Per favore rispondi con 'da bere' o 'da mangiare'.")
        risposta1 = input("Ti piacerebbe ordinare da bere o da mangiare?")

        # Se la risposta è valida, esci dal ciclo
        if risposta1 == "da bere" or risposta1 == "da mangiare":
            break
        # Opzione per uscire senza ordinare
        elif risposta1 == "non voglio nulla, grazie":
            print("Grazie per essere passato, buona giornata!")
            break
        else:
            # Continua il ciclo per chiedere di nuovo
            continue

# Pausa finale prima di chiudere il programma
input("Premi invio per uscire.")
