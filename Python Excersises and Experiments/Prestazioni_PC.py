print("Benvenuto! Questo programma calcola le prestazioni dei PC.")
print("Puoi eseguire il test automatico o il test manuale. Tieni presente che durante il test automatico è consigliato chiudere tutte le altre applicazioni e che il pc potrebbe surriscaldarsi e che le ventole potrebbero essere rumorose.")
test_type = input("Scegli il tipo di test da eseguire: Automatico (A) o Manuale (M)? ")

if test_type.upper() == "A":
    # Import per creare hash e stressare la CPU.
    import hashlib
    # Import per operazioni su file e percorsi.
    import os
    # Import per avviare processi separati nel test multi-core.
    import subprocess
    # Import per usare l'interprete Python corrente nei processi figli.
    import sys
    # Import per creare file temporanei per il test disco.
    import tempfile
    # Import per misurare tempi ad alta precisione.
    import time
    # Import per scaricare dati e misurare la rete.
    import urllib.request
    # Import per data/ora nel report finale.
    from datetime import datetime

    # Avvisa l'utente dell'avvio del benchmark automatico.
    print("Eseguendo il test automatico...")

    # Funzione di supporto per limitare un valore in un intervallo.
    def clamp(value, low, high):
        # Restituisce value compreso tra low e high.
        return max(low, min(high, value))

    # Converte un rapporto prestazionale in punteggio 1-100.
    def score_from_ratio(ratio):
        # Esempio: ratio 1.0 -> 100, ratio 0.5 -> 50.
        return int(clamp(round(ratio * 100), 1, 100))

    # ---------------- CPU ----------------
    # Messaggio di avanzamento test CPU.
    print("[CPU] Test single-core e multi-core in corso...")
    # Durata di ogni benchmark CPU in secondi (test piu lungo).
    cpu_duration = 6.0
    # Nota eventuale se il multi-core non riesce completamente.
    cpu_note = ""

    # Salva il tempo iniziale del test CPU single-core.
    cpu_single_start = time.perf_counter()
    # Contatore cicli CPU completati nel test single-core.
    cpu_single_loops = 0
    # Payload iniziale usato negli hash ripetuti.
    payload = b"PC-BENCH"
    # Esegue il test single-core per la durata impostata.
    while time.perf_counter() - cpu_single_start < cpu_duration:
        # Inizializza digest con il payload corrente.
        digest = payload
        # Esegue molti hash consecutivi per caricare un singolo core.
        for _ in range(3000):
            # Calcola SHA-256 del digest precedente.
            digest = hashlib.sha256(digest).digest()
        # Incrementa il numero di loop completati.
        cpu_single_loops += 1
    # Calcola tempo totale single-core evitando divisione per zero.
    cpu_single_elapsed = max(time.perf_counter() - cpu_single_start, 1e-9)
    # Calcola loop al secondo nel test single-core.
    cpu_single_ops = cpu_single_loops / cpu_single_elapsed
    # Converte la metrica single-core in punteggio.
    cpu_single_score = score_from_ratio(cpu_single_ops / 220.0)

    # Numero di worker per il test multi-core (almeno 2).
    cpu_multi_workers = max(2, os.cpu_count() or 2)
    # Codice Python eseguito da ogni processo worker multi-core.
    cpu_worker_code = (
        "import hashlib,time,sys\n"
        "duration=float(sys.argv[1])\n"
        "start=time.perf_counter()\n"
        "loops=0\n"
        "payload=b'PC-BENCH'\n"
        "while time.perf_counter()-start<duration:\n"
        "    digest=payload\n"
        "    for _ in range(3000):\n"
        "        digest=hashlib.sha256(digest).digest()\n"
        "    loops+=1\n"
        "elapsed=max(time.perf_counter()-start,1e-9)\n"
        "print(loops/elapsed)\n"
    )
    # Lista processi attivi per il benchmark multi-core.
    multi_processes = []
    # Avvia un processo per ogni core logico disponibile.
    for _ in range(cpu_multi_workers):
        # Crea processo worker che esegue benchmark CPU isolato.
        process = subprocess.Popen(
            [sys.executable, "-c", cpu_worker_code, str(cpu_duration)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Salva il processo per raccogliere i risultati.
        multi_processes.append(process)

    # Somma delle prestazioni loop/s di tutti i worker.
    cpu_multi_ops = 0.0
    # Contatore worker falliti nel test multi-core.
    cpu_multi_failures = 0
    # Raccoglie output da ogni processo worker avviato.
    for process in multi_processes:
        # Attende fine processo e acquisisce output.
        stdout_text, _stderr_text = process.communicate(timeout=int(cpu_duration) + 15)
        # Valida che il processo sia terminato correttamente.
        if process.returncode == 0:
            # Tenta conversione output in float loop/s.
            try:
                cpu_multi_ops += float(stdout_text.strip().splitlines()[-1])
            # Conta come errore se output non interpretabile.
            except (ValueError, IndexError):
                cpu_multi_failures += 1
        else:
            # Conta worker fallito.
            cpu_multi_failures += 1

    # Se almeno un worker e riuscito, calcola punteggio multi-core.
    if cpu_multi_failures < cpu_multi_workers:
        # Usa riferimento proporzionale al numero di worker.
        cpu_multi_ref = 220.0 * cpu_multi_workers * 0.90
        # Converte metrica multi-core in punteggio.
        cpu_multi_score = score_from_ratio(cpu_multi_ops / cpu_multi_ref)
    else:
        # In caso di fallimento totale assegna valori minimi.
        cpu_multi_ops = 0.0
        cpu_multi_score = 1
        cpu_note = "Test CPU multi-core non completato correttamente."

    # Combina single-core e multi-core in un punteggio CPU unico.
    cpu_score = int(round(cpu_single_score * 0.40 + cpu_multi_score * 0.60))

    # ---------------- RAM ----------------
    # Messaggio di avanzamento test RAM.
    print("[RAM] Test in corso...")
    # Quantita di RAM da allocare per il benchmark (test piu lungo).
    ram_mb = 256
    # Converte MB in byte.
    ram_size = ram_mb * 1024 * 1024
    # Alloca un buffer in memoria.
    ram_buf = bytearray(ram_size)

    # Avvia timer per scrittura RAM.
    t0 = time.perf_counter()
    # Scrive pattern nel buffer per testare banda in scrittura.
    ram_buf[:] = b"\xAA" * ram_size
    # Ferma timer scrittura RAM.
    t1 = time.perf_counter()
    # Legge una parte del buffer per testare banda in lettura.
    checksum = sum(ram_buf[::4096])
    # Ferma timer lettura RAM.
    t2 = time.perf_counter()
    # Usa la variabile per evitare warning su valore non usato.
    _ = checksum

    # Calcola MB/s in scrittura RAM.
    ram_write_mb_s = ram_mb / max(t1 - t0, 1e-9)
    # Calcola MB/s in lettura RAM.
    ram_read_mb_s = ram_mb / max(t2 - t1, 1e-9)
    # Calcola media tra scrittura e lettura.
    ram_avg = (ram_write_mb_s + ram_read_mb_s) / 2
    # Converte prestazione RAM in punteggio.
    ram_score = score_from_ratio(ram_avg / 3500.0)

    # ---------------- DISCO ----------------
    # Messaggio di avanzamento test disco.
    print("[DISCO] Test in corso...")
    # Dimensione totale del test disco in MB (test piu lungo).
    disk_mb = 512
    # Crea chunk casuale da 4 MB per scrittura su disco.
    chunk = os.urandom(4 * 1024 * 1024)
    # Numero di scritture da 4 MB necessarie.
    repeats = max(1, disk_mb // 4)
    # Crea file temporaneo su cui fare benchmark.
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # Salva il percorso del file temporaneo.
        tmp_path = tmp.name

    # Inizia blocco protetto per pulizia file temporaneo.
    try:
        # Avvia timer scrittura disco.
        d0 = time.perf_counter()
        # Apre il file temporaneo in scrittura binaria.
        with open(tmp_path, "wb") as f:
            # Scrive tutti i chunk previsti.
            for _ in range(repeats):
                # Scrive 4 MB per iterazione.
                f.write(chunk)
            # Svuota buffer Python su disco.
            f.flush()
            # Forza sync su disco fisico.
            os.fsync(f.fileno())
        # Ferma timer scrittura disco.
        d1 = time.perf_counter()

        # Apre il file temporaneo in lettura binaria.
        with open(tmp_path, "rb") as f:
            # Legge tutto il file a blocchi da 4 MB.
            while f.read(4 * 1024 * 1024):
                # Non serve elaborare i dati letti.
                pass
        # Ferma timer lettura disco.
        d2 = time.perf_counter()

        # Calcola MB/s in scrittura disco.
        disk_write_mb_s = disk_mb / max(d1 - d0, 1e-9)
        # Calcola MB/s in lettura disco.
        disk_read_mb_s = disk_mb / max(d2 - d1, 1e-9)
        # Calcola media prestazioni disco.
        disk_avg = (disk_write_mb_s + disk_read_mb_s) / 2
        # Converte prestazione disco in punteggio.
        disk_score = score_from_ratio(disk_avg / 450.0)
    # Esegue sempre la pulizia del file temporaneo.
    finally:
        # Tenta di rimuovere il file temporaneo.
        try:
            # Cancella file benchmark dal disco.
            os.remove(tmp_path)
        # Ignora errori di rimozione non bloccanti.
        except OSError:
            # Nessuna azione aggiuntiva necessaria.
            pass

    # ---------------- RETE ----------------
    # Messaggio di avanzamento test rete.
    print("[RETE] Test in corso...")
    # Velocita di rete iniziale in MB/s.
    net_mb_s = 0.0
    # Punteggio rete iniziale.
    net_score = 0
    # Nota eventuale in caso di errore rete.
    net_note = ""
    # Avvia test download rete con gestione errori.
    try:
        # Limita il download a 15 MB per una misura piu stabile.
        max_bytes = 15 * 1024 * 1024
        # Contatore byte scaricati.
        downloaded = 0
        # Avvia timer rete.
        n0 = time.perf_counter()
        # Apre URL di test della banda.
        with urllib.request.urlopen("https://speed.hetzner.de/10MB.bin", timeout=10) as resp:
            # Continua a leggere finche non raggiunge il limite.
            while downloaded < max_bytes:
                # Legge un blocco di dati dalla risposta.
                data = resp.read(min(256 * 1024, max_bytes - downloaded))
                # Esce se non arrivano altri dati.
                if not data:
                    # Fine stream.
                    break
                # Aggiorna totale scaricato.
                downloaded += len(data)
        # Ferma timer rete.
        n1 = time.perf_counter()
        # Calcola MB/s download.
        net_mb_s = (downloaded / (1024 * 1024)) / max(n1 - n0, 1e-9)
        # Converte prestazione rete in punteggio.
        net_score = score_from_ratio(net_mb_s / 60.0)
    # Cattura qualsiasi errore di rete senza bloccare il report.
    except Exception as exc:
        # Salva nota errore da includere nel report.
        net_note = f"Test rete non completato: {exc}"

    # ---------------- PUNTEGGIO FINALE ----------------
    # Calcola punteggio finale pesato dei singoli componenti.
    total_score = int(round(
        # Peso CPU 35%.
        cpu_score * 0.35 +
        # Peso RAM 25%.
        ram_score * 0.25 +
        # Peso Disco 25%.
        disk_score * 0.25 +
        # Peso Rete 15%.
        net_score * 0.15
    ))

    # Classifica qualitativa in base al punteggio totale.
    if total_score >= 85:
        # Fascia molto alta.
        livello = "ECCELLENTE"
    elif total_score >= 70:
        # Fascia alta.
        livello = "BUONO"
    elif total_score >= 50:
        # Fascia intermedia.
        livello = "MEDIO"
    else:
        # Fascia base.
        livello = "BASE"

    # Inizializza struttura del report testuale.
    report = []
    # Aggiunge separatore superiore.
    report.append("=" * 64)
    # Aggiunge titolo report.
    report.append("REPORT TEST AUTOMATICO COMPONENTI PC")
    # Aggiunge separatore sotto il titolo.
    report.append("=" * 64)
    # Aggiunge timestamp del test.
    report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Riga vuota per leggibilita.
    report.append("")
    # Riga risultati CPU single-core.
    report.append(f"CPU single-core -> {cpu_single_ops:.2f} hash-loop/s | Punteggio: {cpu_single_score}/100")
    # Riga risultati CPU multi-core.
    report.append(f"CPU multi-core  -> {cpu_multi_ops:.2f} hash-loop/s ({cpu_multi_workers} core) | Punteggio: {cpu_multi_score}/100")
    # Riga punteggio CPU combinato.
    report.append(f"CPU totale      -> Punteggio combinato: {cpu_score}/100")
    # Riga risultati RAM.
    report.append(f"RAM   -> {ram_avg:.2f} MB/s medi    | Punteggio: {ram_score}/100")
    # Riga risultati Disco.
    report.append(f"DISCO -> {disk_avg:.2f} MB/s medi    | Punteggio: {disk_score}/100")
    # Riga risultati Rete.
    report.append(f"RETE  -> {net_mb_s:.2f} MB/s down    | Punteggio: {net_score}/100")
    # Se presente, aggiunge nota errore rete.
    if net_note:
        # Inserisce dettaglio errore rete nel report.
        report.append(net_note)
    # Se presente, aggiunge nota errore CPU multi-core.
    if cpu_note:
        # Inserisce dettaglio errore CPU nel report.
        report.append(cpu_note)
    # Aggiunge separatore sezione finale.
    report.append("-" * 64)
    # Aggiunge punteggio totale.
    report.append(f"PUNTEGGIO FINALE: {total_score}/100")
    # Aggiunge valutazione qualitativa.
    report.append(f"VALUTAZIONE: {livello}")
    # Aggiunge separatore di chiusura.
    report.append("-" * 64)

    # Unisce tutte le righe in un unico testo.
    report_text = "\n".join(report)
    # Stampa report completo a video.
    print("\n" + report_text)

    # Crea nome file report con data e ora.
    report_name = f"report_prestazioni_pc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    # Imposta la cartella Documenti dell'utente come destinazione report.
    documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
    # Crea la cartella se non esiste.
    os.makedirs(documents_dir, exist_ok=True)
    # Calcola percorso assoluto file report in Documenti.
    report_path = os.path.join(documents_dir, report_name)
    # Apre file report in scrittura UTF-8.
    with open(report_path, "w", encoding="utf-8") as rf:
        # Scrive contenuto report nel file.
        rf.write(report_text)
    # Comunica dove e stato salvato il report.
    print(f"Report salvato in: {report_path}")

    # Mantiene la finestra aperta finche l'utente non preme Invio.
    input("Premi invio per chiudere il programma...")

elif test_type.upper() == "M":
    # Import locali per analizzare testo componenti e salvare report.
    import os
    import re
    from datetime import datetime

    # Acquisisce modello CPU in modalita manuale.
    cpu = input("Inserisci il modello della CPU: ").strip()
    # Acquisisce quantita RAM in modalita manuale.
    ram = input("Inserisci la quantità di RAM (es. 16GB): ").strip()
    # Acquisisce disco in modalita manuale.
    disk = input("Inserisci il tipo e la capacità del disco (es. SSD 512GB): ").strip()
    # Acquisisce GPU facoltativa in modalita manuale.
    gpu = input("Inserisci il modello della GPU (se presente, altrimenti lascia vuoto): ").strip()

    # Estrae una capacita in GB da stringhe tipo "1TB", "512GB", "16384MB".
    def parse_capacity_gb(text):
        # Converte testo in minuscolo e uniforma la virgola decimale.
        normalized = text.lower().replace(",", ".")
        # Cerca numero + unita.
        match = re.search(r"(\d+(?:\.\d+)?)\s*(tb|gb|mb)", normalized)
        # Se non trova nulla restituisce None.
        if not match:
            return None
        # Converte il valore numerico trovato.
        value = float(match.group(1))
        # Legge l'unita associata.
        unit = match.group(2)
        # Converte tutto in GB.
        if unit == "tb":
            return value * 1024.0
        if unit == "mb":
            return value / 1024.0
        return value

    # Stima punteggio CPU da modello inserito.
    def estimate_cpu_score(cpu_text):
        # Base iniziale.
        score = 45
        # Normalizza testo CPU.
        t = cpu_text.lower()
        # Classi alte.
        if "i9" in t or "ryzen 9" in t or "threadripper" in t:
            score += 35
        # Classi medio-alte.
        elif "i7" in t or "ryzen 7" in t:
            score += 25
        # Classi medie.
        elif "i5" in t or "ryzen 5" in t:
            score += 15
        # Classi entry.
        elif "i3" in t or "ryzen 3" in t:
            score += 5
        # Bonus per generazioni recenti Intel/AMD.
        if "14th" in t or "13th" in t or "12th" in t or "zen 5" in t or "zen 4" in t:
            score += 8
        # Limita score a 1..100.
        return max(1, min(100, score))

    # Stima punteggio RAM da capacita e tecnologia.
    def estimate_ram_score(ram_text):
        # Estrae capacita in GB.
        gb = parse_capacity_gb(ram_text)
        # Se non trova un numero usa valore medio prudente.
        if gb is None:
            score = 55
        elif gb >= 64:
            score = 95
        elif gb >= 32:
            score = 85
        elif gb >= 16:
            score = 70
        elif gb >= 8:
            score = 50
        else:
            score = 35
        # Bonus piccolo per DDR5.
        if "ddr5" in ram_text.lower():
            score += 5
        # Limita score a 1..100.
        return max(1, min(100, score)), gb

    # Stima punteggio disco da tipo e capacita.
    def estimate_disk_score(disk_text):
        # Normalizza testo disco.
        t = disk_text.lower()
        # Base in funzione del tipo di storage.
        if "nvme" in t or "m.2" in t:
            score = 90
        elif "ssd" in t:
            score = 75
        elif "hdd" in t or "meccanico" in t:
            score = 45
        else:
            score = 60
        # Estrae capacita in GB.
        gb = parse_capacity_gb(disk_text)
        # Bonus capacita disco.
        if gb is not None:
            if gb >= 2000:
                score += 8
            elif gb >= 1000:
                score += 5
            elif gb >= 500:
                score += 2
        # Limita score a 1..100.
        return max(1, min(100, score)), gb

    # Stima punteggio GPU da modello, se presente.
    def estimate_gpu_score(gpu_text):
        # Se GPU non specificata restituisce None.
        if not gpu_text:
            return None
        # Normalizza testo GPU.
        t = gpu_text.lower()
        # Fasce prestazionali principali.
        if "4090" in t:
            score = 100
        elif "4080" in t or "7900 xtx" in t:
            score = 95
        elif "4070" in t or "7800 xt" in t:
            score = 85
        elif "4060" in t or "7600" in t:
            score = 75
        elif "1660" in t or "580" in t:
            score = 55
        elif "intel uhd" in t or "iris" in t or "vega" in t:
            score = 35
        else:
            score = 60
        # Limita score a 1..100.
        return max(1, min(100, score))

    # Calcola i punteggi stimati dai dati manuali.
    cpu_score_manual = estimate_cpu_score(cpu)
    ram_score_manual, ram_gb = estimate_ram_score(ram)
    disk_score_manual, disk_gb = estimate_disk_score(disk)
    gpu_score_manual = estimate_gpu_score(gpu)

    # Pesi dinamici: con GPU presente usa 4 componenti, altrimenti 3.
    if gpu_score_manual is not None:
        total_score = int(round(
            cpu_score_manual * 0.30 +
            ram_score_manual * 0.25 +
            disk_score_manual * 0.20 +
            gpu_score_manual * 0.25
        ))
    else:
        total_score = int(round(
            cpu_score_manual * 0.40 +
            ram_score_manual * 0.35 +
            disk_score_manual * 0.25
        ))

    # Classifica qualitativa in base al punteggio totale.
    if total_score >= 85:
        livello = "ECCELLENTE"
    elif total_score >= 70:
        livello = "BUONO"
    elif total_score >= 50:
        livello = "MEDIO"
    else:
        livello = "BASE"

    # Crea brevi consigli automatici in base ai punti deboli.
    consigli = []
    if ram_score_manual < 65:
        consigli.append("Valuta un upgrade RAM (almeno 16GB consigliati).")
    if disk_score_manual < 65:
        consigli.append("Un SSD/NVMe migliora molto tempi di avvio e caricamento.")
    if gpu_score_manual is not None and gpu_score_manual < 60:
        consigli.append("Per gaming/rendering, una GPU piu recente darebbe un salto netto.")
    if cpu_score_manual < 60:
        consigli.append("Una CPU di fascia piu recente puo aumentare molto la reattivita generale.")
    if not consigli:
        consigli.append("Configurazione bilanciata: non risultano colli di bottiglia evidenti.")

    # Costruisce report testuale del test manuale intelligente.
    report = []
    report.append("=" * 64)
    report.append("REPORT TEST MANUALE INTELLIGENTE")
    report.append("=" * 64)
    report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append(f"CPU inserita   : {cpu}")
    report.append(f"CPU stimata    : {cpu_score_manual}/100")
    report.append(f"RAM inserita   : {ram}")
    report.append(f"RAM stimata    : {ram_score_manual}/100" + (f" ({ram_gb:.0f} GB rilevati)" if ram_gb is not None else ""))
    report.append(f"DISCO inserito : {disk}")
    report.append(f"DISCO stimato  : {disk_score_manual}/100" + (f" ({disk_gb:.0f} GB rilevati)" if disk_gb is not None else ""))
    if gpu:
        report.append(f"GPU inserita   : {gpu}")
        report.append(f"GPU stimata    : {gpu_score_manual}/100")
    else:
        report.append("GPU inserita   : non specificata")
    report.append("-" * 64)
    report.append(f"PUNTEGGIO FINALE STIMATO: {total_score}/100")
    report.append(f"VALUTAZIONE: {livello}")
    report.append("-" * 64)
    report.append("Consigli:")
    for c in consigli:
        report.append(f"- {c}")

    # Unisce righe report in unico testo.
    report_text = "\n".join(report)
    # Mostra report a schermo.
    print("\n" + report_text)

    # Salva report nella cartella Documenti.
    report_name = f"report_test_manuale_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
    os.makedirs(documents_dir, exist_ok=True)
    report_path = os.path.join(documents_dir, report_name)
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(report_text)
    print(f"Report salvato in: {report_path}")

    # Mantiene la finestra aperta finche l'utente non preme Invio.
    input("Premi invio per chiudere il programma...")
else:
    # Gestisce input non valido.
    print("Scelta non valida. Per favore, esegui di nuovo il programma e scegli A o M.")
    input("Premi invio per chiudere il programma...")
    
