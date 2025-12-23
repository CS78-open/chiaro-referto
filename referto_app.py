import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="ChiaroReferto", page_icon="🩺")

# Titolo e introduzione
st.title("🩺 ChiaroReferto")
st.write("""
**Benvenuto.** Incolla qui sotto il testo del tuo referto medico.
L'Intelligenza Artificiale ti aiuterà a capire i termini difficili e ti suggerirà cosa chiedere al tuo medico.
""")

# Sidebar per la chiave di sicurezza (API KEY)
st.sidebar.header("Impostazioni")
api_key = st.sidebar.text_input("Inserisci la tua Google API Key", type="password")

# Area per incollare il referto
testo_referto = st.text_area("Incolla qui il testo del referto:", height=200)

# Bottone per avviare
if st.button("Spiegami e Rassicurami"):
    if not api_key:
        st.error("⚠️ Per favore, inserisci la tua API Key nella barra laterale a sinistra.")
    elif not testo_referto:
        st.warning("⚠️ Per favore, incolla il testo del referto.")
    else:
        try:
            # Configura l'AI con la chiave
            genai.configure(api_key=api_key)
            
            # USIAMO IL MODELLO CHE ABBIAMO TROVATO NELLA TUA LISTA
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Creiamo il prompt (le istruzioni per l'AI)
            prompt = f"""
            Agisci come un assistente medico empatico e molto chiaro.
            Ecco un referto medico: "{testo_referto}"
            
            Fai queste 3 cose:
            1. SPIEGAZIONE SEMPLICE: Spiega cosa dice il referto usando parole che capirebbe una persona anziana. Evita il "medichese".
            2. PUNTI CHIAVE: Elenca in breve i punti principali emersi (positivi e negativi).
            3. DOMANDE PER IL DOTTORE: Suggerisci 3 domande intelligenti e specifiche che il paziente dovrebbe fare al suo medico curante.
            
            IMPORTANTE:
            - Sii rassicurante.
            - Inizia e finisci ricordando che sei un'AI e che questa NON è una diagnosi medica.
            """
            
            # Mostriamo un caricamento mentre l'AI pensa
            with st.spinner('L\'AI sta analizzando il referto con il modello Gemini 2.5...'):
                response = model.generate_content(prompt)
                
            # Mostriamo il risultato
            st.success("Analisi completata!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")
            st.info("Suggerimento: Controlla di aver copiato tutta la API Key correttamente senza spazi.")

# Disclaimer a fondo pagina
st.divider()
st.caption("⚠️ ATTENZIONE: Servizio sperimentale basato su AI. Non sostituisce il parere medico.")