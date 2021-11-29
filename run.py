import streamlit            as st
import pandas               as pd
import numpy                as np
import plotly.express       as px
from datetime               import timedelta
import SessionState
import base64

elements = {'Tc99m':361.2,'I131':11520.0,'I123':780.0,'Ga67':4698.0,'Ga68':68110.0,'Tl201':4380.0,'F18':109.8}

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt,base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def hourToMin(hour1, hour2):
    hour1 = hour1.strftime("%H:%M")
    hour2 = hour2.strftime("%H:%M")
    h1 = timedelta(hours=int(hour1.split(':')[0]), minutes=int(hour1.split(':')[1]))
    minutes1 = h1.total_seconds()/60
    h2 = timedelta(hours=int(hour2.split(':')[0]), minutes=int(hour2.split(':')[1]))
    minutes2 = h2.total_seconds()/60
    return(minutes2-minutes1)

def calculate(entrada, meiavida, qtd0, hora0):
    calculos = []
    sobras = []
    horas = []
    for i in range(len(entrada['Peso do Paciente (kg)'])):
        intervalo = hourToMin(hora0, entrada['Hora da Aplicação'][i])
        horaApp = entrada['Hora da Aplicação'][i]
        #print(f'\n Paciente {i}')
        #print(f'hora0 = {hora0} | horaApp = {horaApp}')
        hora0 = entrada['Hora da Aplicação'][i]
        x = intervalo/meiavida
        #print(f'x = {x} | t = {intervalo} | meiavida = {meiavida}')
        #print(f'q0 = {qtd0}')
        qtd0 = qtd0/2**x
        #print(f'q_decaido = {qtd0}')
        qtd0 = qtd0-entrada['Dose (mCi)'][i]
        #print(f'sobra = {qtd0}')
        horas.append(hora0.strftime("%H:%M"))
        sobras.append(qtd0)
    return horas, sobras

state = SessionState.get(fixos={'meiavida': '','qtd0': 0,'hora0': 0},entrada = {'Peso do Paciente (kg)' : [], 'Dose (mCi)' : [], 'Hora da Aplicação' : []})



tit, buttons, results = st.beta_columns(3)
tit.title("MENU Calculator")
openFile = buttons.button('Abrir')
upload = results.empty()
saveFile = buttons.button('Salvar')
download = results.empty()
clearFile = buttons.button('Apagar dados')


my_expander = st.beta_expander("Entradas:", expanded=True)
in11, in12, in13 = my_expander.beta_columns(3)
element = in11.selectbox('Elemento:', ('Tc99m', 'I131', 'I123', 'Ga67', 'Ga68', 'Tl201', 'F18'))
qtd0 = in12.number_input('Quantidade:', format='%.0f', step=10.0)
hora0 = in13.time_input('Hora Inicial:')


in21, in22 = my_expander.beta_columns(2)
peso = in21.number_input('Peso do Paciente (kg):', format='%.0f', step=10.0)
dose = int(peso)*.1
horaApp = in22.time_input('Hora da Aplicação:')

but1, but2, but3, but4 = my_expander.beta_columns(4)
add = but1.button('Adicionar')
edit = but2.button('Editar')
calc = but3.button('Calcular')
graph = but4.button('Gráfico')

if add:
    state.entrada['Peso do Paciente (kg)'].append(peso)
    state.entrada['Dose (mCi)'].append(dose)
    state.entrada['Hora da Aplicação'].append(horaApp)
    
if clearFile:
    state.entrada = {
        'Peso do Paciente (kg)' : [],
        'Dose (mCi)' : [],
        'Hora da Aplicação' : []
    }

if calc:
    # state.fixos['meiavida'] = elements[element]
    # state.fixos['qtd0'] = qtd0
    # state.fixos['hora0'] = hora0

    horas, sobras = calculate(state.entrada, elements[element], qtd0, hora0)
    state.entrada['Sobra (mCi)'] = sobras

if graph:
      
    fig = px.line(state.entrada, x="Hora da Aplicação", y="Sobra (mCi)", title='Sobra por horario de aplicação')  
    st.plotly_chart(fig)

if openFile:
    upload.file_uploader('', type=['csv', 'xlxs'])

if saveFile:
    df = pd.DataFrame.from_dict(state.entrada)
    tmp_download_link = download_link(df, 'menu_data.csv', 'DOWNLOAD LINK')
    download.markdown(tmp_download_link, unsafe_allow_html=True)



my_expander = st.beta_expander("Dados:", expanded=True)
table = my_expander.table(state.entrada)


