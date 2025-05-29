from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Memoria semplice in RAM (dizionario utente -> lista messaggi)
# Per esempio, se non hai utenti, puoi usare una singola lista globale
chat_memory = []

MAX_MESSAGES = 20

@app.route('/webhook', methods=['POST'])
def webhook():
    global chat_memory
    req = request.get_json(force=True)
    user_message = req['queryResult']['queryText']

    # Aggiungi il messaggio utente alla memoria
    chat_memory.append({"role": "user", "content": user_message})

    # Se la memoria supera 20 messaggi, la resetto (o taglio)
    if len(chat_memory) > MAX_MESSAGES:
        chat_memory = chat_memory[-MAX_MESSAGES:]  # mantieni solo gli ultimi 20

    # Prepara i messaggi con system prompt fisso + la memoria
    messages = [
        {"role": "system", "content": """
        "Sei un assistente esperto dei vini dell'azienda vitivinicola Terre di San Rocco.Fornisci risposte dettagliate e precise basate esclusivamente sulle seguenti informazioni.

I nostri vigneti si trovano a Roncade in provincia di Treviso, tra la laguna di Venezia e le colline del Montello. Una zona con temperature ideali e caratterizzata da interessanti escursioni termiche tra il giorno e la notte, condizioni che favoriscono la perfetta maturazione delle uve.
In questa cornice, illuminata dal sole e accarezzata dalla brezza, in un territorio argilloso e vocato alla vigna alleviamo Pinot Grigio, Pinot Bianco, Chardonnay, Merlot e Cabernet Franc nei tre appezzamenti tutti adiacenti alla cantina. I filari sono collocati considerando il terroir e le migliori condizioni di esposizione, perché i nostri vini nascono in vigna con una cura maniacale che parte proprio dal campo nel rispetto della terra e della pianta. Crediamo fortemente che sia importante rispettare i ritmi della natura e raccogliere i frutti che essa ci offre, seguendo le tecniche agronomiche dell'agricoltura biologica. Questo ci permette di ottenere un prodotto veramente naturale che solo piccole produzioni possono garantire.
Produrre Metodo Classico con uno stile originale ed eclettico, in una zona conosciuta in tutto il mondo per la produzione del Prosecco, richiede una buona dose di incoscienza e follia.
Siamo orgogliosi di poter garantire che i vini che produciamo sono il risultato delle uve raccolte nei terreni di nostra proprietà, l'unico modo che conosciamo per poter avere il controllo totale della filiera produttiva fino all'imbottigliamento, l'etichettatura e il confezionamento dei nostri vini e questo assicura l'altissimo
standard qualitativo.
Da ogni acino nasce una storia, unica: allevare viti è un po' come veder crescere i propri figli: da un lato li si può educare, stimolare, raddrizzare, dall'altro bisogna lasciar fare alla natura. Per i nostri vini è proprio così: il microclima, il caldo, il freddo, la pioggia, la paura della grandine, le nebbie sono tutti elementi che non possiamo controllare e che rendono ogni vendemmia diversa e unica. Le vigne hanno sempre, anche con il passare degli anni, qualcosa da insegnare. Tanti sono gli stimoli che credono tutto questo entusiasmante, un gioco in equilibrio tra colori, sentori, aromi, profumi, sapori, gusti, persistenza in una continua ricerca della perfezione.

Schede prodotto: 

METODO CLASSICO
BRUT NATURE ROSE' MARIA VITTORIA
Vitigno: Pinot Grigio
Tipologia: Rosè Metodo Classico Brut Nature
Sistema di allevamento: Cordone speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di agosto
Vinificazione: Dopo un'attenta selezione, l'uva viene diraspata e pigiata in modo soffice ed il mosto ottenuto rimane a contatto con le bucce in macerazione pellicolare a freddo prefermentativa, per un tempo tale da conferire sfumature cromatiche ed aromatiche che rendono unico questo Vino.
Dopo una delicata pressatura, il mosto svolge una prima fermentazione in recipienti di acciaio inox a temperature controllata. Dopo il tiraggio, il vino riposerà per un periodo di 50 mesi in bottiglia, svolgendo la seconda fermentazione a temperatura controllata e costante, si procede poi al remuage.
Durante sboccatura la bottiglia verrà ricolmata con lo stesso vino, quindi vino su vino, senza alcun dosaggio al fine di lasciare trasparire la personalità e la tipicità d'annata.
Sboccatura: almeno 50 mesi non dosato
Gradazione alcolica: 12,5 % vol
Colore ed aspetto: di color oro rosa compatto che ricorda il color cipria, con finissimo perlage.
Profumo: naso teso con richiami di mandarino e sentori di fragolina di bosco. Buona complessità e finezza, accenno di lavanda ed una piacevole chiusura balsamica e pepe bianco.
Gusto: in bocca il Maria Vittoria Rosè Nature risulta denso con bollicina croccante e piena, ma per niente invadente. Richiami di agrumi con un fresco finale minerale, di bella persistenza ha una spettacolare bevibilità.
Abbinamento: sembra nato appositamente per le moeche fritte, ma il fritto di paranza potrebbe rendergli onore. Perfetto con pizze ad importante lievitazione, predilige tartare di carne o pesce, pesce sfilettato, crudité di crostacei. Da solo!
Servizio: servire a 6-8 °C in flute leggermente ampia.
Degustare ascoltando: Amy Winehouse-Back to Black

METODO CLASSICO
BRUT NATURE 2012
Vitigno: Chardonnay e Pinot Bianco
Tipologia: Metodo Classico Brut Nature Millesimato
Sistema di allevamento: Cordone Speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di agosto
Vinificazione: dopo un'attenta selezione l'uva viene diraspata e pigiata in modo soffice ed il mosto ottenuto rimane a contatto con le proprie bucce in macerazione pellicolare a freddo prefermentativa, per un tempo tale da conferire sfumature cromatiche ed aromatiche che rendono unico questo vino. Dopo una delicata pressatura il mosto svolge una prima fermentazione in recipienti d' acciaio inox a temperatura controllata a circa 16° C. Affina per 9 mesi con bâttonage sistematico ogni 10 giorni circa in contenitori in acciaio.
La presa di spuma avviene a temperatura controllata a 13/15 ° C.
Dopo il tiraggio il vino riposerà per un periodo in bottiglia di 84 mesi per poi procedere alla messa in punta della bottiglia e successiva sboccatura operando il rabbocco esclusivamente "vino su vino".
Sboccatura: 84 mesi Dosaggio Zero
Gradazione alcolica: 12,5% vol
Colore ed aspetto: riflessi dorati su giallo brillante il perlage è finissimo e persistente.
Profumo: bouquet intenso e complesso dove emerge una spiccata mineralità con sentori di frutta esotica matura. Si evidenziano note di nocciola arricchite da spezie con un finale agrumato.
Gusto: nonostante la freschezza il palato viene coinvolto dal corpo cremoso e vellutato con fragranze di frutta esotica, la lunga permanenza sui lieviti conferisce un finale di gran complessità senza compromettere una facilità di beva a dir poco sorprendente.
Abbinamento: dal momento dell'aperitivo fino a tutto pasto, fedele amico dell'ostrica rosa di Scardovari senza prevaricare la sua delicatezza, tataki di tonno, per i più temerari le carni rosse.
Servizio: servire a 8° C in calice ultralight leggermente ampio con svasatura sulla sommità.
Degustare ascoltando: John Legend - Ordinary People (live)

METODO CLASSICO
BRUT NATURE PINOT BIANCO
Vitigno: Pinot Bianco
Tipologia: Metodo Classico brut nature millesimato
Sistema di allevamento: Cordone Speronato
Numeri ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: a mano nel mese di agosto
Vinificazione: Dopo un'attenta selezione, l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo. Il mosto svolge una prima fermentazione in recipienti d'acciaio a temperatura controllata.
Dopo aver effettuato il tiraggio il vino riposerà in bottiglia svolgendo la seconda fermentazione a temperatura costante e controllata per almeno 36 mesi. Successivamente al remouage, durante la sboccatura, la bottiglia verrà ricolmata con lo stesso vino, quindi vino su vino, senza alcun dosaggio al finedi lasciar trasparire la personalità e la tipicità d'annata.
Sboccatura: almeno 36 mesi non dosato
Gradazione alcolica: 12,5% vol.
Colore ed aspetto: brillante giallo paglierino con finissimo perlage
persistente
Profumo: bouquet di fiori di campo freschi e con fruttato, esotico di lici e papaya. Si percepisce la raffinatezza del giglio e della ginestra
con il bergamotto.
Gusto: fresco e minerale, ma al tempo stesso elegante all'ingresso del palato promette morbidezza celando una chiusura perfettamente secca e sapida, degna di questo Nature.
Abbinamento: perfetto per aperitivo con cicchetti veneziani dal baccalà mantecato al salmone leggermente affumicato, ma anche a tutto pasto. Risotto con con Go & cape tonde ( ghiozzi e molluschi della laguna veneta) fino ai primi con carni bianche o un grande spago al pomodoro fresco e basilico.
Servizio: servire 6/8° in flûte leggermente ampia
Degustare ascoltando: Rihanna - Work (feat Drake)

METODO CLASSICO
EXTRA BRUT PINOT BIANCO
Vitigno: Pinot Bianco
Tipologia: Metodo Classico Extra brut Millesimato
Sistema di allevamento: Cordone Speronato
Numeri ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di agosto
Vinificazione: Dopo un'attenta selezione, l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo. Il mosto svolge una prima fermentazione in recipienti di acciaio, a temperature controllata. Dopo aver effettuato il tiraggio il vino riposerà in bottiglia svolgendo la seconda fermazione a temperature costante e controllata per almeno 48 mesi. Successivamente al remouage, durante la sboccatura, la bottiglia verrà ricolmata con lo stesso vino, quindi vino su vino, senza alcun dosaggio al fine di lasciar trasparire la personalità e la tipicità d'annata..
Sboccatura: almeno 48 mesi non dosato
Gradazione alcolica: 13,5% vol.
Colore ed aspetto: brillante giallo paglierino e intense, con finissimo perlage persistente
Profumo: buona complessità e finezza, fruttato importante con note di pera e mela fresca. Limetta e citronella assicurano
freschezza agrumata.
Gusto: fresco, sapido, ma al tempo stesso forte ed avvincente, sorprendente per struttura del Pinot Bianco. Il palato è avvolgente ed elegante in grado di riproporre I sentori promessi all'olfatto.
Abbinamento: perfetto per un aperitivo e incredibilmente versatile a tutto pasto, predilige specialmente | frutti di mare ed il pesce alla brace. Perfetto con carni bianche o e se volessimo proprio osare una costata taglio fiorentina, di Razza Blonde d'Aquitaine con frollatura importante e cottura da Serial Griller....
Servizio: servire 6/8° in flûlte leggermente ampia
Degustare ascoltando: Cold Play- Adventure of a Lifetime

METODO CLASSICO
EXTRA BRUT PINOT BIANCO
Vitigno: Pinot Bianco
Tipologia: Metodo Classico Extra brut Millesimato
Sistema di allevamento: Cordone Speronato
Numeri ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di agosto
Vinificazione: Dopo un'attenta selezione, l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo. Il mosto svolge una prima fermentazione in recipienti di acciaio, a temperature controllata. Dopo aver effettuato il tiraggio il vino riposerà in bottiglia svolgendo la seconda fermazione a temperature costante e controllata per almeno 48 mesi. Successivamente al remouage, durante la sboccatura, la bottiglia verrà ricolmata con lo stesso vino, quindi vino su vino, senza alcun dosaggio al fine di lasciar trasparire la personalità e la tipicità d'annata..
Sboccatura: almeno 48 mesi non dosato
Gradazione alcolica: 13,5% vol.
Colore ed aspetto: brillante giallo paglierino e intense, con finissimo perlage persistente
Profumo: buona complessità e finezza, fruttato importante con note di pera e mela fresca. Limetta e citronella assicurano
freschezza agrumata.
Gusto: fresco, sapido, ma al tempo stesso forte ed avvincente, sorprendente per struttura del Pinot Bianco. Il palato è avvolgente ed elegante in grado di riproporre I sentori promessi all'olfatto.
Abbinamento: perfetto per un aperitivo e incredibilmente versatile a tutto pasto, predilige specialmente | frutti di mare ed il pesce alla brace. Perfetto con carni bianche o e se volessimo proprio osare una costata taglio fiorentina, di Razza Blonde d'Aquitaine con frollatura importante e cottura da Serial Griller....
Servizio: servire 6/8° in flûlte leggermente ampia
Degustare ascoltando: Cold Play- Adventure of a Lifetime

METODO CLASSICO9
BRUT PINOT BIANCO
Vitigno: Pinot Bianco
Tipologia: Metodo Classico Brut Millesimato
Sistema di allevamento: Cordone speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di agosto
Vinificazione: dopo un'attenta selezione l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo.
Il mosto svolge una prima fermentazione in recipienti d'acciaio, a temperatura controllata di circa 17 °C, fino a quando raggiungerà un determinato residuo zuccherino, il quale verrà esaurito durante una seconda fermentazione che si svolgerà in bottiglia, dopo aver effettuato il tiraggio.
Il vino riposa poi, per almeno 36 mesi.
Successivamente la bottiglia sarà sottoposta a remouage e sboccatura.
Sboccatura: almeno 36 mesi non dosato
Gradazione alcolica: 12,5 % vol
Colore ed aspetto: il giallo paglierino brillante è rincorso da numerose bollicine di buona persistenza.
Profumo: fine florealità di ginestra, giglio, camomilla, acacia.
Il fruttato di papaya, pesca gialla, albicocca, e bergamotto è disteso su un velo di crema pasticcera e leggera vaniglia.
Gusto: buona freschezza a bilanciare morbidezze importanti.
Il classico ritorno elegantemente floreale del Pinot Bianco si propone in bocca.
Abbinamento: al momento dell'aperitivo con mousse di caprino e olive di Gaeta, oppure con barchette di peperone giallo al forno e capperi, con una tartina di pane nero e burro alle acciughe.
Servizio: servire a 6 °C in flute.
Degustare ascoltando: Dua Lipa - Be the one

VINO SPUMANTE DI QUALITÀ
PINOT BIANCO BRUT NATURE
Vitigno: Pinot Bianco
Tipologia: Spumante di qualità Brut Nature Millesimato
Sistema di allevamento: Cordone Speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia:
Vinificazione: dopo un'attenta selezione, l'uva viene diraspata e pigiata in modo soffice ed il mosto ottenuto rimane a contatto con le proprie bucce in macerazione pellicolare a freddo prefermentativa, per un tempo tale da conferire sfumature cromatiche ed aromatiche che rendono unico questo vino. Dopo una delicata pressatura il mosto svolge una prima fermentazione in recipienti d'acciaio inox a temperatura controllata a circa 16° C fino a quando raggiungerà un determinato residuo zuccherino che verrà esaurito durante la seconda fermentazione che si svolgerà in bottiglia.
Dopo il tiraggio il vino riposerà in bottiglia per un periodo di 24 mesi per poi procedere alla messa in punta della bottiglia e successiva sboccatura *à la volée" senza effettuare il congelamento del collo della bottiglia, operando il rabbocco esclusivamente "vino su vino".
Sboccatura: 24 mesi Dosaggio Zero
Gradazione alcolica: 11,5 % vol
Colore ed aspetto: giallo paglierino brillante con finissimo perlage persistente ed una lievissima velatura che lo caratterizza.
Profumo: tropicalità assoluta con fine florealità di ginestra, giglio, camomilla, acacia. Fruttato di papaya, pesca gialla,
albicocca e bergamotto.
Il vino si presenta torbido per effetto dei lieviti che ne salvaguardano la longevità, il vino può essere servito senza scuotere la bottiglia, decantato, se si desidera separarlo dai suoi lieviti presenti sul fondo, oppure agitato leggermente prima di stappare per apprezzare tutte le particolari sfumature.
gusto: grande freschezza corredata da una quasi Adriatica sapidità, con un ritorno elegantemente floreale al palato degno della bacca del Pinot Bianco.
Abbinamento: dal momento dell'aperitivo fino a tutto pasto, fedele amico dell'ostrica veneta di Sacca degli Scardovari esaltandone la sostenuta sapidità, saute di Cozze Mitilla di Pellestrina.
Degustare ascoltando: Red Hot Chili Peppers - By the way

VINO SPUMANTE DI QUALITA'
RIFLESSO DI LUCE ROSE' BRUT NATURE
Uve: Pinot Grigio in purezza
Tipologia: Spumante di qualità Brut Nature Rosé Millesimato
Sistema allevamento: Cordone Speronato
Numero ceppi per ettaro: 5000 Ceppi/Ettaro
Resa per ceppo: 1/1.2 kg
Vendemmia: manuale nella prima decade del mese di agosto
Vinificazione: Dopo un'
attenta selezione l' uva viene diraspata e
pigiata in modo soffice ed il mosto ottenuto rimane a contatto con le oprie bucce in macerazione pellicolare a freddo prefermentativa, pe n temoo tale da conferire sfumature cromatiche ed aromatiche ch
rendono unico questo Vino.
Dopo una delicata pressatura il mosto svolge una prima fermentazione in recipienti d'acciaio inox a temperatura controllata a circa 16° C fino a quando raggiungerà un determinato residuo zuccherino, che verrà esaurito durante la seconda fermentazione, che si svolgerà in bottiglia.
Dopo il tiraggio il vino riposerà per un lungo periodo in bottiglia di almeno 24 mesi per poi procedere alla messa in punta della bottiglia e successiva sboccatura " a la volée "
,senza effettuare la ghiacciatura
del collo della bottiglia, operando il rabbocco esclusivamente " vino
su vino".
Successivamente al remuage, durante la sboccatura, la bottiglia verrà ricolmata con lo stesso vino, quindi vino su vino, al fine di preservarne la totale integrità e personalità senza alcuna interferenza organolettica, ed elevando le caratteristiche del vino e l'importante concetto di tipicità d' annata.
Sboccatura: almeno 24 mesi non dosato
Gradazione alcolica: 11.5% Vol
Colore ed aspetto: Delicatissime tonalità rame con nuance oro rosa, in cui le numerose e sottili bollicine risalgono attraverso una tenue velatura data dai lieviti
Il vino si presenta velato, per effetto dei lieviti che salvaguardano la longevità.
Può essere servito senza capovolgere la bottiglia, decantato, se si desidera mantenere la separazione dai sui lieviti presenti sulfondo, oppure, agitando leggermente prima di stappare per apprezzare tutte le sue sfumature.
Profumo: Al naso sottile e diretto, profuma di susina matura e corteccia verde, conchiglie e punta di rabarbaro.
Gusto: Attacco gustativo con sorso ampio, sapido, molto equilibrato. Il corpo poggia su una sorprendente morbidezza, nonostante la notevole freschezza che va a braccetto con il dosaggio
Nature. Esce a distanza, sorprendendoti, una finissima ed elegante nota balsamica.
Abbinamenti: Spiccata propensione all' aperitivo, fedelissimo alle declinazioni di Cicchetti
Veneziani, Carpaccio di Gambero Rosso di Mazara del Vallo con lime, olio Evo, sale in foglia e pepe di Sichuan, cicchetto con pane arrostito lardo di Colonnata e alice di Sciacca, spaghetto alla chitarra aglio, olio e peperoncino, ragout di seppia con il suo fegato.
Servizio: servire a 6/8° in flute leggermente ampia
Degustare ascoltando: Asap Rocky - Everyday (feat Rod Stewart)

PINOT GRIGIO MACERATO
Vitigno: Pinot Grigio
Tipologia: Pinot Grigio delle Venezie DOC
Sistema di allevamento: Cordone Speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di settembre
Vinificazione: dopo un'attenta selezione, l'uva viene diraspata, il pigiato ottenuto esegue una macerazione pre-fermentativa di 36 ore a freddo.
Dopodiché il pigiato viene pressato in modo soffice e fatto sedimentare mediante decantazione statica.
Il mosto fermenta in acciaio a temperatura controllata.
Alla fine della fermentazione alcolica il vino viene affinato in vasche d'acciaio, attuando dei bâtonnage ripetuti con cadenza periodica fino al momento dell'imbottigliamento.
Gradazione alcolica: 13 % vol
Colore ed aspetto: il vino presenta dei riflessi ramati importanti caratteristici della buccia di cipolla, che lo caratterizzano durante la sua conservazione.
Profumo: dotato di una finezza aromatica decisa dove esordisce con note fruttate di albicocca matura e sfumature di lamponi e ciliegia.
Emergono anche profumi speziati di pepe bianco e fumè.
Gusto: al palato è morbido e avvolgente, dosa sapientemente un buon corpo con una nervatura piacevole, acidula, che dona freschezza alla beva.
Equilibrato in ogni componente, ha un'ottima persistenza ed eleganza.
Abbinamento: grande versatilità in tavola, è ottimo l'abbinamento con carni e pesci saporiti come il tonno.
Si sposa bene anche a primi piatti a base di pesce e zuppe saporite di legumi.
Perfetto infine accostato a salumi stagionati.
Servizio: servire a 12-14 °C in ampi calici a bocca svasata.
Degustare ascoltando: Mario Biondi - This is what you are

PINOT GRIGIO
Vitigno: Pinot Grigio
Tipologia: Pinot Grigio delle Venezie DOC
Sistema di allevamento: Cordone Speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di settembre
Vinificazione: dopo un'attenta selezione, l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo. Il mosto fermenta in acciaio a temperatura controllata. Alla fine della fermentazione il vino viene mantenuto sui propri lieviti in vasche d'acciaio inox per circa 10/15 mesi con bâtonnage settimanale.
Gradazione alcolica: 13 % vol
Colore ed aspetto: giallo paglierino con riflessi grigio-verde, accenni buccia di cipolla, cristallino e consistente.
Profumo: deciso, intenso, di buona complessità e finezza.
La frutta matura irrompe con una susina degna della migliore slivovitz ed è accompagnata da mela golden e pera.
Florealità determinata da ginestra, biancospino ed iris.
Leggera speziatura di cardamomo e pepe bianco.
Gusto: morbidezza ed alcolicità si misurano con una buona freschezza e mineralità decisa.
Coerente con quanto preannunciato al naso, ritorna il fruttato della susina.
L'ottima intensità e lunghezza di bocca chiudono su un finale elegantemente ammandorlato.
Abbinamento: grande capacità di rispondere al mare: spaghetti con bottarga, tranci di pesce spada con pomodorini pachino, capperi ed olive troveranno motivo su cui misurarsi.
Ma l'aromaticità, la morbidezza e la capacità sgrassante di questo grande vino potranno ben confrontarsi anche con una choucroute alsaziana.
Servizio: servire a 8-10 °C in calici a tulipano chiuso di buona ampiezza.
Degustare ascoltando: Robbie Williams - Feel

PINOT BIANCO
Vitigno: Pinot Bianco
Tipologia: Pinot Bianco igt Veneto
Sistema di allevamento: Cordone Speronato
Numeri ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: Nel mese di settembre
Vinificazione: Dopo un'attenta selezione, l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo. Il mosto fermenta in acciaio a temperatura controllata di circa 16°C. Alla fine della fermentazione il vino viene affinati in vasche d'acciaio attuando dei bâttonage ripetuti con cadenza periodica fino al momento dell'imbottigliamento.
Gradazione alcolica: 13% Vol.
Colore ed aspetto: Paglierino tenue con nuance verdi, luminoso, consistente e alla mescita rivela grande freschezza.
Profumo: Delicata intensità e finezza, inizia con un floreale esotico, di fiori dolci, che si allatga nei minuti successivi. Ai fiori di campo, glicine, giglio e camomilla, fanno eco mela fresca, pesca bianca,
mora di gelso.
Gusto: entra in bocca ripettando le promesse di freschezza degli aromi olfattivi. Bella sapidità, equilibrio e mineralità.
Abbinamento: la buona persistenza permette a questo vino di essere abbinato ad antipasti a base di pesce, alla tartare si salmone selvaggio, Cappe Sante gratinate e grigliate di pesce, persico reale
sfilettato ed impanato.
Servizio: 10-12° C in calici a tulipano
Degustare ascoltando: Mika (feat. Chiara) - Stardust

CHARDONNAY
Vitigno: Chardonnay
Tipologia: Chardonnay igt Veneto
Sistema di allevamento: Cordone Speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: Nel mese di settembre
Vinificazione: Dopo un'attenta selezione, l'uva è immediatamente pressata in modo soffice ed il mosto viene fatto sedimentare mediante decantazione statica a freddo. Il mosto fermenta in acciaio a temperatura controllata di circa 16°C. Alla fine della fermentazione il vino viene affinati in vasche d'acciaio attuando dei battonage ripetuti con cadenza periodica fino al momento dell'imbottigliamento.
Gradazione alcolica: 13% Vol.
Colore ed aspetto: giallo paglierino tenue percorso da lampi verdi, molto luminoso e consistente
Profumo: Intenso, mediamente complesso e fine. In evidenza le note fruttate di ananas, mela verde acerba e scorza d'agrumi, completate anche dalle floreali del biancospino e verbena.
Gusto: Equilibrato ed intenso, di buon corpo e persistenza sempre supportata da soffusa mineralità e delicate note citrine.
Abbinamento: Estremamente duttile può ben far fronte ad antipasti di mare come carpaccio di spigola olio Evo e pepe sichuan, ma anche da gnocchi burro e salvia, ad un risotto di verdure mantecato con casatella, ad una sogliola alla mugnaia.
Servizio: 8-10° C in calici a tulipano chiuso di media ampiezza
Degustare ascoltando: Coldplay (feat. Bts) - My universe

CABERNET FRANC
Vitigno: Cabernet Franc
Tipologia: Cabernet Franc IGT Veneto
Sistema di allevamento: Cordone speronato
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di settembre
Vinificazione: dopo un'attenta selezione, l'uva viene diraspata e pigiata per poi fermentare in recipienti troncoconici d'acciaio con macerazione lunga: 16/18 giorni.
Successivamente riposa per 16/18 mesi in vasche di acciaio inox.
Gradazione alcolica: 13% vol
Colore ed aspetto: limpido, rubino con squarci granata, buona consistenza.
Profumo: l'intensità e la finezza rispondono ad una complessità determinata dall'erbaceo:
corteccia verde di salice e rucola.
Seguono la mora di rovo e lampone ed il floreale di sambuco e pruno selvatico.
Chiude la spezia dei chiodi di garofano.
Gusto: l'alcolicità discreta e la morbidezza mitigano gli effetti tannici. Bella freschezza e sapidità cui fa seguito buona intensit e persistenza.
Abbinamento: salsicce "aperte" ai ferri, ma anche con tastasale e fagioli di Lamon, oppure con un ottimo formaggio d'alpeggio: il Vezzena (in cimbro "Vesen").
Servizio: servire a 15-16 °C in balloon di media ampiezza.
Degustare ascoltando: Jack Savoretti - The other side of love

MERLOT
Vitigno: Merlot
Tipologia: Merlot IGT Veneto
Sistema di allevamento: GDC
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di settembre
Vinificazione: dopo un'attenta selezione, l'uva viene diraspata e pigiata
per poi fermentare in recipienti troncoconici d'acciaio con macerazione lunga:
16/18 giorni (a seconda dell'annata).
Successivamente riposa per 16/18 mesi in vasche di acciaio inox.
Gradazione alcolica: 13 % vol
Colore ed aspetto: granato in cui permangono ancora ricordi rubino, limpido e di buona consistenza.
Profumo: esprime buona complessita su uno sfondo di misurata intensit e finezza.
Il leggero erbaceo del mallo di noce si frappone tra il fruttato del ribes, della mora di rovo, della prugna ed il floreale di viola e peonia.
Gusto: asciutto e sufficientemente morbido, pur con una tannicita di tutto rispetto cui fa seguito buona freschezza e sapidità.
Abbinamento: certo una pasta e fagioli alla veneta oppure un arrosto d'oca, ma può ben figurare anche accanto ad una fiorentina.
Servizio: servire a 15-16 °C in balloon di media ampiezza.
Degustare ascoltando: Gotye (feat Kimbra) Somebody that I use to know

MERLOT RISERVA
Vitigno: Merlot
Tipologia: Merlot IGT Veneto
Sistema di allevamento: GDC
Numero di ceppi per ettaro: 5000
Resa per ceppo: 1-1,2 Kg
Vendemmia: nel mese di settembre
Vinificazione: dopo un'attenta selezione, l'uva viene diraspata e pigiata per poi fermentare in recipienti troncoconici d'acciaio con macerazione lunga:
16/18 giorni (a seconda dell'annata).
Successivamente riposa per 16/18 mesi in barrique e tonneau di rovere Allier a tostatura leggera.
Gradazione alcolica: 14% vol
Colore ed aspetto: granato esemplare, limpido e consistente.
Profumo: complessità sugli spalti: il fruttato della confettura di mora, di prugna, di amarene sotto spirito e del succo di sambuco viaggia assieme alla rosa rossa secca, alla viola ed iris in appassimento.
Alla speziatura di vaniglia e cannella rispondono, liquirizia e cioccolato.
Gusto: morbidezza che legata all'alcool si propone in bocca a fronte di un'ottima sapidità.
È un susseguirsi continuo di frutta ed aromi terziari.
I tannini, non ancora domi, continuano ad asciugare il cavo orale ed a manifestare la bella struttura.
Abbinamento: si può spaziare dagli spaghetti al sugo rosso con guanciale di Amatrice e pecorino romano, al filetto al pepe verde, ad una bella scaglia di Bagoss e pane casareccio.
Servizio: servire a 16-18 °C in balloon di buona ampiezza.
Degustare ascoltando: Frank Sinatra - My Way

BIANCO IGT VENETO 18:00 - 20:00
Vitigni: Assemblaggio Pinot Grigio e Chardonnay
Tipologia: Bianco IGT Veneto
Sistema di allevamento: Cordone speronato
Numero di ceppi per ettaro: 4800
Resa per ceppo: 2,5 Kg
Vendemmia: nel mese di settembre
Vinificazione: Diraspatura soffice per eliminare il raspo.
Leggera macerazione pellicolare a 8-10 °C
per 3-5 h di contatto.
Pressatura soffice e batonage del mosto ottenuto per 24-36 h.
Separazione del mosto fiore con la decantazione statica e fermentazione in contenitori di acciaio a 17°C.
Si effettuano periodici Batonnage del vino ottenuto fino all'atto dell'imbottigliamento.
Degustazione: Colore giallo brillante, profumo delicato di frutti tropicali maturi.
Vino fine, elegante con un finale leggermente aromatico e persistente a ricordare le note olfattive.
Ideale come aperitivo, primi e secondi piatti delicati.
Servizio: Servire a 12-14 °C
Degustare ascoltando: Harry Styles - Watermelon sugar

ROSATO IGT VENETO 18:00 - 20:00
Vitigno: Pinot Grigio
Tipologia: Rosato IGT Veneto
Sistema di allevamento: Cordone speronato
Numero di ceppi per ettaro: 4500
Resa per ceppo: 2,5 Kg
Vendemmia: nel mese di settembre
Vinificazione: Diraspatura soffice, contatto della frazione liquida (mosto)
con la frazione solida (bucce) delle uve, per circa 12 ore. Il diraspato viene pressato in modo soffice e viene eseguita la selezione delle pressature. Il mosto rosato ottenuto, di debole intensità cromatica,
viene fatto fermentare in vasche di acciaio inox a 17°C per mantenere le note aromatiche di freschezza tipiche di un vino a bacca bianca.
Si effettuano periodici Batonnage del vino ottenuto fino all'atto dell'imbottigliamento.
Degustazione: Colore rosa, con note al naso fruttate che ricordano la pesca bianca e note floreali dove emerge la rosa.
Al gusto si presenta snello, vivace e dotato di grande sapidità.
Ideale come aperitivo e accompagna la tavola estiva, si abbina bene ai salumi, ai primi piatti ed al pesce
Ideale come aperitivo, primi e secondi piatti delicati.
Servizio: Servire a 12-14 °C
Degustare ascoltando: Bruno Mars - The lazy song

ROSSO IGT VENETO 18:00 - 20:00
Vitigni: Assemblaggio Merlot e Cabernet Franc
Tipologia: Rosso IGT Veneto
Sistema di allevamento: Cordone speronato
Numero di ceppi per ettaro: 4500
Resa per ceppo: 2,5 Kg
Vendemmia: nel mese di settembre
Vinificazione: Diraspatura delicata e riempimento dei maceratori in inox troncoconici.
Il contatto della frazione liquida (mosto) con la frazione solida (bucce) delle uve, ha una durata per 6 giorni con fermentazione a 22-23 °C.
Il vino attenuto viene lasciato riposare in serbatoi di inox dove svolge la fermentazione malolattica e successivamente confezionato.
Degustazione: Vino rosso rubino, curato particolarmente nella qualità, è un prodotto nuovo che vuole essere apprezzato per la sua freschezza e sorbevolezza.
Ha particolari note olfattive fruttate, con leggeri richiami speziati.
Al gusto è caratterizzato da una buona struttura e persistenza. Ideale come aperitivo e abbinamento ai piatti della tavola quotidiana.
Servizio: Servire a 12-14 °C
Degustare ascoltando: Maroon 5 - Sugar

Contatti e posizione:
-Situata nella provincia di Treviso, a Roncade, via Vivaldi 32/E.  
- info@terredisanrocco.it, telefono +39 3891260990  
- https://terredisanrocco.it "
        "Rispondi con professionalità e gentilezza alle domande sull’azienda, sui vini, sugli abbinamenti. "
        "Adatta automaticamente la lingua della risposta a quella dell’utente (italiano o inglese)."
"""}] + chat_memory

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_response = response.choices[0].message.content

        # Aggiungi risposta del bot alla memoria
        chat_memory.append({"role": "assistant", "content": bot_response})

        return jsonify({'fulfillmentText': bot_response})

    except Exception as e:
        return jsonify({'fulfillmentText': f"Errore: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


        