import streamlit as st
import pandas as pd
from pandas import ExcelWriter
from utils import api_classificador
import json
import base64
from io import BytesIO
from local_css import local_css

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
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Baixar arquivo Excel</a>' # decode b'abc' => abc

def temas_print(temas:list):
            for tema,cor in zip(temas, range(1,len(temas)+1)):
                t = f"<span class = 'highlight green{cor}'>{tema}</span>"
                st.markdown(t, unsafe_allow_html=True)

def main():

    #Criando barra lateral
    st.sidebar.image("images/logo_azul_horizontal-05.png",use_column_width = True)
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

    else:
        st.markdown("## Em construção :wrench:")

    #     arquivo = st.file_uploader("Anexe um arquivo .xlsx (Planilha Excel)",type="xlsx")
    #     coluna_texto = st.text_input("Nome da coluna com os textos")

    #     if arquivo is not None:
    #         df = pd.read_excel(arquivo).head(8)
    #         st.write(df)

    #         if st.button("Classificar"):
            
    #             st.markdown("### Resultados")

    #             #Chama a API e constroi dataframe com resultados
    #             lista_df = []
    #             with st.spinner("Classificando textos..."):
    #                 for texto in df[coluna_texto]:
    #                     r = api_results_data_frame(texto)
    #                     r["Texto"] = texto
    #                     r = r.sort_values("Probabilidade",ascending = False).head(5)

    #                     st.write(r)

    #             st.success("Classificação finalizada")

    #             df_final = r

    #             st.write(df_final)
    #             st.markdown(get_table_download_link(df_final), unsafe_allow_html=True)

if __name__=="__main__":
    main()