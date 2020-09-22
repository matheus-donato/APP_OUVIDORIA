import streamlit as st
import pandas as pd
from pandas import ExcelWriter
from utils import api_classificador
import json
import base64
from io import BytesIO
from local_css import local_css
import time
import SessionState

def api_results_data_frame(texto):
    resultado = api_classificador(texto,endpoint='ouvidoria')
    resultado_json = json.loads(resultado)
    df = pd.DataFrame({"Promotoria": resultado_json["temas"],"Probabilidade":resultado_json["p"], "Temas_sub":resultado_json["temas_sub"]})
    return df

def api_results_data_frame_subtema(texto, tema):
    resultado = api_classificador(texto = texto,endpoint='ouvidoria/temas',tema=tema)
    resultado_json = json.loads(resultado)
    df = pd.DataFrame({"Promotoria": resultado_json["temas"],"Probabilidade":resultado_json["p"]})
    return df

# def to_excel(df):
#     output = BytesIO()
#     writer = ExcelWriter(output,engine="xlsxwriter")
#     df.to_excel(writer)
#     writer.save()
#     processed_data = output.getvalue()
#     return processed_data

# def get_table_download_link(df):
#     """Generates a link allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """
#     val = to_excel(df)
#     b64 = base64.b64encode(val)
#     return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="temas_classificados.xlsx">Baixar arquivo Excel</a>' # decode b'abc' => abc

def temas_print(temas:list):
            for tema,cor in zip(temas, range(1,len(temas)+1)):
                t = f"<span class = 'highlight green{cor}'>{tema}</span>"
                st.markdown(t, unsafe_allow_html=True)

def main():
    #Criando barra lateral
    st.sidebar.image("images/logo_desenvolvido-01.png",use_column_width = True)
    fun_select = st.sidebar.selectbox(
        "",
        ["Classificação direta"])

    
    #Classificação direta
    if fun_select == "Classificação direta":

        st.title("Classificador de temas da ouvidoria")

        texto = st.text_area("Cole o texto da denúncia aqui:")
        texto = ' '.join(texto.split())

        session_state = SessionState.get(name="", classificar = False)
        classificar = st.button('Temas')
        if texto == '' and classificar is True:
                st.error("Digite ou cole um texto de ouvidoria.")        
        if (classificar or session_state.classificar) and texto != "":                
            st.markdown("---")
            st.markdown("### Temas preditos")
            session_state.classificar = True
        #Chama a API e constroi dataframe com resultados
            df = api_results_data_frame(texto)

            #Refinando resuldados
            df = df.query("Probabilidade >= 0.1").sort_values("Probabilidade",ascending=False)

            #Mostrando o resultado        
            temas_preditos = df['Promotoria'].tolist()
            temas_selecionados = st.multiselect('', temas_preditos, default=temas_preditos)
            temas_sub = df.query(f"Promotoria in {temas_preditos}").Temas_sub.tolist()
            local_css("style.css")
            temas_print(temas_selecionados)

            #Classificação de subtemas
        session_state_sub = SessionState.get(name="", classificar_subtemas=False)
        classificar_subtemas = st.button('Subtemas')
        if classificar_subtemas:
            st.markdown('''
            ---
            ### Subtemas preditos
            ''')
            for idx, tema_s in enumerate(temas_selecionados):
                    tema = temas_sub[idx]
                    st.markdown(f"#### {tema_s}")
                    df = api_results_data_frame_subtema(texto= texto, tema=tema)

                    #Refinando resuldados
                    df_sub = df.query("Probabilidade >= 0.1").sort_values("Probabilidade",ascending=False)
                    #Mostrando o resultado        
                    temas_preditos = df_sub['Promotoria'].tolist()
                    #temas_selecionados = st.multiselect('', temas_preditos, default=temas_preditos)
                    local_css("style.css")
                    temas_print(temas_preditos)

#Removendo rodapé com o nome do streamlit
hide_footer_style = """
        <style>
        .reportview-container .main footer {visibility: hidden;}    
        """
st.markdown(hide_footer_style, unsafe_allow_html=True)
        
if __name__=="__main__":
    main()