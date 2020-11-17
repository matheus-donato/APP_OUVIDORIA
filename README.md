# APP_OUVIDORIA

Este [WebApp](https://app-ouvidoria-subtemas.herokuapp.com/) é a interface gráfica de uma [Api](https://github.com/matheus-donato/API_OUVIDORIA) desenvolvida pelo [Inova_MPRJ](http://www.mprj.mp.br/inova) com a finalidade de permitir a interação com o modelo multi-label de classificação de temas e subtemas das denúncias e reclamações prestadas a [Ouvidoria]().
Foi utilizada a plataforma [Heroku](https://www.heroku.com/) e a biblioteca [stramlit](https://www.streamlit.io/) para criação do app.


## Utilização e interação 

É possível utilizar-se do web app selecionando a classificação direta.
Somente os resultados gerados pelo modelo com probabilidade maior que 90% são reportados.
Por forma direta faz-se refência a utilização da caixa de texto implementada no aplicativo, onde é possível colar um texto ou escrever uma suposta denúncia para ser classificada.



## Bibliotecas utilizadas

As bibliotecas utilizadas para desenvolver a aplicação web encontram-se abaixo:
* streamlit
* pandas
* xlrd
* xlsxWriter

As versões encontram-se no arquivo [requirements]() presente neste repositório.

## Créditos
Este protótipo foi produzido pelo laboratório de Inovação do MPRJ, o [INOVA_MPRJ](http://www.mprj.mp.br/inova).
A equipe de ciência de dados é constituida por:
[Matheus Donato](matheus.donato@mprj.mp.br) que desenvolveu este projeto,
[Bernardo Baron](bernardo.baron@mprj.mp.br),
Estevan Augusto.

![logo_inova](https://github.com/estevanmendes/APP_OUVIDORIA/blob/master/images/logo_azul_horizontal-05.png)
