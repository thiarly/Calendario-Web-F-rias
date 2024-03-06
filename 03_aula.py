import streamlit as st
from time import sleep
import pandas as pd
from crud import le_todos_usuarios, cria_usuarios, modifica_usuario, deleta_usuario


def login():
    usuarios = le_todos_usuarios()
    usuarios = {usuario.nome: usuario for usuario in usuarios}
    
    
    with st.container(border=True):
        st.markdown("Bem-Vindos ao App Férias!")
        nome_usuario = st.selectbox("Escolha seu usuário", 
            list(usuarios.keys()))
        
        senha = st.text_input("Digite sua senha", type="password")
        if st.button("Acessar"):
            usuario = usuarios[nome_usuario]
            if usuario.verifica_senha(senha):
                st.success("Login efetuado com sucesso!")
                st.session_state['logado'] = True
                st.session_state['usuario'] = usuario
                st.rerun()        
            else:
                st.error("Senha incorreta!")

def tab_gestao_usuarios():
    tab_vis, tab_cria, tab_mod, tab_del = st.tabs(
        ["Visualizar", "Criar", "Modificar", "Deletar"]
    )
    usuarios = le_todos_usuarios()
    with tab_vis:
        data_usuarios = [{
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "acesso_gestor": usuario.acesso_gestor,
            "inicio_empresa": usuario.inicio_empresa,
        } for usuario in usuarios]
        st.dataframe(pd.DataFrame(data_usuarios).set_index("id"))
        
    with tab_cria:
        nome = st.text_input("Nome do usuário")
        email = st.text_input("Email do usuário")
        senha = st.text_input("Senha do usuário", type="password")
        inicio_empresa = st.date_input("Data de início na empresa (formato AAAA-MM-DD)")
        acesso_gestor = st.checkbox("Acesso de gestor?", value=False)
        
        if st.button("Criar usuário"):
            cria_usuarios(
                nome=nome,
                senha=senha,
                email=email,
                inicio_empresa=inicio_empresa,
                acesso_gestor=acesso_gestor
            )
            st.success("Usuário criado com sucesso!")
            st.rerun()

    with tab_mod:
        usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
        nome_usuario = st.selectbox("Escolha o usuário a ser modificado", list(usuarios_dict.keys()))
        usuario = usuarios_dict[nome_usuario]
        nome = st.text_input("Nome do usuário", value=usuario.nome)
        
        senha = st.text_input("Senha do usuário", value="xxxxxx", type="password")
        email = st.text_input("Email do usuário", value=usuario.email)
        inicio_empresa = st.text_input("Data de início na empresa (formato AAAA-MM-DD)", value=usuario.inicio_empresa)
        acesso_gestor = st.checkbox("Modificar Acesso de gestor?", value=usuario.acesso_gestor)
        
        if st.button("Modificar usuário"):
            if senha == "xxxxxx":
                modifica_usuario(
                    id=usuario.id,
                    nome=nome,
                    email=email,
                    inicio_empresa=inicio_empresa,
                    acesso_gestor=acesso_gestor
                )
                st.success("Usuário modificado com sucesso!")
            else:
                modifica_usuario(
                    id=usuario.id,
                    nome=nome,
                    senha=senha,
                    email=email,
                    inicio_empresa=inicio_empresa,
                    acesso_gestor=acesso_gestor
                )
                sleep(2)
                st.success("Usuário modificado com sucesso!")
                st.rerun()
    
    with tab_del:
        usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
        nome_usuario = st.selectbox("Escolha o usuário a ser deletado", list(usuarios_dict.keys()))
        usuario = usuarios_dict[nome_usuario]
        if st.button("Deletar usuário"):
            deleta_usuario(usuario.id)
            st.success("Usuário deletado com sucesso!")
            st.rerun()
        
            
                
def pagina_caledario():
    st.title("Bem Vindo ao App Férias!")
    st.divider()
    
    usuario = st.session_state['usuario']
    if usuario.acesso_gestor:
        st.markdown("Você é um gestor")
        cols = st.columns(2)
        with cols[0]:
            if st.button("Acessar Gestão de Usuários", use_container_width=True):
                
                st.session_state["pag_gestao_usuarios"] = True
                st.rerun()
        with cols[1]:
            if st.button("Acessar Calendário", use_container_width=True):
                st.session_state["pag_gestao_usuarios"] = False
                st.rerun()
        
    if st.session_state["pag_gestao_usuarios"]:
        st.markdown("Página Gestão de Usuários")
        with st.sidebar:
            tab_gestao_usuarios()
        
    else:
        st.markdown("Página Calendário")

def main():
    
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False
    if not 'pag_gestao_usuarios' in st.session_state:
        st.session_state['pag_gestao_usuarios'] = False
        
    if not st.session_state['logado']:
        login() 
    
    else:
        pagina_caledario()    

    
if __name__ == '__main__':
    main()
