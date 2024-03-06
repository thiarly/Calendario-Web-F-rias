import json
import streamlit as st
from streamlit_calendar import calendar

# Carregar as opções do calendário de um arquivo JSON
with open("calendar_options.json", "r") as f:
    calendar_options = json.load(f)

# Inicializar variáveis de estado se ainda não existirem
if "ultimo_click" not in st.session_state:
    st.session_state["ultimo_click"] = None

if 'limpar' not in st.session_state:
    st.session_state.limpar = False

# Função para limpar as datas selecionadas
def limpar_datas():
    if 'data_inicio' in st.session_state:
        del st.session_state['data_inicio']
    if 'data_final' in st.session_state:
        del st.session_state['data_final']
    st.session_state.limpar = True  # Indica que a limpeza foi solicitada

# Verificar se a limpeza foi solicitada e executar a lógica de limpeza
if st.session_state.limpar:
    limpar_datas()  # Aqui você chama a lógica de limpeza
    st.session_state.limpar = False  # Reset the flag

# Definição dos eventos do calendário
calendar_events = [
    {
        "title": "Event 1",
        "start": "2024-03-01T08:30:00",
        "end": "2024-03-20T10:30:00",
        "resourceId": "a",
    },
]

# Criação do widget do calendário
calendar_widget = calendar(events=calendar_events, options=calendar_options)
if ("callback" in calendar_widget and calendar_widget["callback"] == 'dateClick'):
    raw_date = calendar_widget["dateClick"]["date"]
    if raw_date != st.session_state["ultimo_click"]:
        st.session_state["ultimo_click"] = raw_date
    
    date = calendar_widget["dateClick"]["date"].split("T")[0]
    if not 'data_inicio' in st.session_state:
        st.session_state['data_inicio'] = date
        st.warning(f"Data de início de férias selecionada {date}")
        
    else:
        st.session_state['data_final'] = date
        data_inicio = st.session_state['data_inicio']
        cols = st.columns([0.7, 0.3])
        with cols[0]:
            st.warning(f"Data de início de férias selecionada {data_inicio}")
        with cols[1]:
            if st.button("Limpar", use_container_width=True):
                limpar_datas()

        cols = st.columns([0.7, 0.3])
        with cols[0]:
            st.warning(f"Data de fim de férias selecionada {date}")
        with cols[1]:
            st.button("Adicionar Férias", use_container_width=True)

st.write(calendar_widget)
