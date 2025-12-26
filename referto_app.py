import streamlit as st
import google.generativeai as genai
import os # Ci serve per controllare se il logo esiste

# Configurazione della pagina
st.set_page_config(page_title="ChiaroReferto", page_icon="🩺")

# --- LOGO E SIDEBAR ---
# Controlliamo se c'è il file logo.png
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=200)
else:
    st.sidebar.write("*(Inserisci un file 'logo.png' nella cartella per vedere il logo qui)*")

st.sidebar.header("Impostazioni")
api_key = st.sidebar.text_input("Inserisci la tua Google API Key", type="password")

# --- CORPO PRINCIPALE ---
st.title("🩺 ChiaroReferto")
st.write("""
**Benvenuto.** Incolla qui sotto il testo del tuo referto medico.
L'Intelligenza Artificiale ti aiuterà a capire i termini difficili e ti suggerirà cosa chiedere al tuo medico.
""")

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
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Agisci come un assistente medico empatico e molto chiaro.
            Ecco un referto medico: "{testo_referto}"
            
            Fai queste 3 cose:
            1. SPIEGAZIONE SEMPLICE: Spiega cosa dice il referto usando parole che capirebbe una persona anziana.
            2. PUNTI CHIAVE: Elenca in breve i punti principali.
            3. DOMANDE PER IL DOTTORE: Suggerisci 3 domande specifiche da fare al medico.
            
            IMPORTANTE: Sii rassicurante. Ricorda che sei un'AI e NON è una diagnosi.
            """
            
            with st.spinner('L\'AI sta analizzando il referto...'):
                response = model.generate_content(prompt)
                
            st.success("Analisi completata!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")

# --- FOOTER & CREDITS ---
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 0.8em;'>
        App realizzata da <b><a href='https://www.marcopingitore.it' target='_blank' style='text-decoration: none; color: inherit;'>Marco Pingitore</a></b><br>
        Rilasciato sotto licenza <b>EUPL v1.2</b> (European Union Public License).<br>
        Software conforme per il riuso nella Pubblica Amministrazione.
    </div>
    """, 
    unsafe_allow_html=True
)
