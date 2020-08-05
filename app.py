import streamlit as st
import pandas as pd
from pandas import ExcelWriter
from utils import api_classificador
import json
import base64
from io import BytesIO
from local_css import local_css
import time

def api_results_data_frame(texto):
    resultado = api_classificador(texto)
    resultado_json = json.loads(resultado)
    df = pd.DataFrame({"Promotoria": resultado_json["temas"],"Probabilidade":resultado_json["p"]})
    return df

def to_excel(df):
    output = BytesIO()
    writer = ExcelWriter(output,engine="xlsxwriter")
    df.to_excel(writer)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="temas_classificados.xlsx">Baixar arquivo Excel</a>' # decode b'abc' => abc

def temas_print(temas:list):
            for tema,cor in zip(temas, range(1,len(temas)+1)):
                t = f"<span class = 'highlight green{cor}'>{tema}</span>"
                st.markdown(t, unsafe_allow_html=True)

def main():

    #Criando barra lateral
    st.sidebar.image("images/logo_desenvolvido-01.png",use_column_width = True)
    fun_select = st.sidebar.selectbox(
        "",
        ("Classificação direta","Classificação a partir de um arquivo"))

    #Classificação direta
    if fun_select == "Classificação direta":

        st.title("Classificador de temas da ouvidoria")

        texto = st.text_area("Cole o texto da denúncia aqui:")

        if st.button('Classificar'):

        #Chama a API e constroi dataframe com resultados
            df = api_results_data_frame(texto)

            #Refinando resuldados
            df = df.query("Probabilidade >= 0.1").sort_values("Probabilidade",ascending=False)

            #Mostrando o resultado        
            local_css("style.css")
            temas_print(df.Promotoria.tolist())
    
    #Classificação a partir de um arquivo
    else:
        arquivo = st.file_uploader("Anexe um arquivo .xlsx (Planilha Excel)",type="xlsx")
        #coluna_texto = st.text_input("Escreva o nome da coluna com os textos e pressione enter.")
        if arquivo is not None:
            df = pd.read_excel(arquivo)
            df.columns.str.title()
            coluna_texto = df.columns.tolist()[0]
            st.write(df.head(8))

            if st.button("Classificar"):
            
                st.markdown("### Resultados")

                #Chama a API e constroi dataframe com resultados
                df_final = pd.DataFrame()
                my_bar = st.progress(0)                
                n_texto = 0
                passos = 1/len(df[coluna_texto])

                for texto in df[coluna_texto]:
                    r = api_results_data_frame(texto)

                    #Refinando resultados
                    r["Texto"] = texto
                    r = r.query("Probabilidade >= 0.1").sort_values("Probabilidade",ascending = False).reset_index()
                    r = r.groupby("Texto").agg(Promotorias = ("Promotoria",", ".join)).reset_index()

                    #Atualizando resultado final
                    df_final = pd.concat([df_final,r],ignore_index=True)
                    time.sleep(0.5)
                    n_texto += passos
                    my_bar.progress(n_texto)

                #Disponibiliza download da planilha com resultados
                st.markdown(get_table_download_link(df_final), unsafe_allow_html=True)

#Removendo rodapé com o nome do streamlit
hide_footer_style = """
        <style>
        .reportview-container .main footer {visibility: hidden;}    
        """
st.markdown(hide_footer_style, unsafe_allow_html=True)
        
if __name__=="__main__":
    main()