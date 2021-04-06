import streamlit            as st
import pandas               as pd
import numpy                as np
from datetime               import timedelta
import SessionState

state = SessionState.get(entrada = {
    'Peso do Paciente (kg)' : [],
    'Dose (mCi)' : [],
    'Hora da Aplicação' : [] 
})


elements = {'Tc99m':361.2,'I131':11520.0,'I123':780.0,'Ga67':4698.0,'Ga68':68110.0,'Tl201':4380.0,'F18':109.8}

tit, open1, save1, clear1 = st.beta_columns(4)
tit.title("MENU Calculator")
openFile = open1.button('Abrir')
saveFile = save1.button('Salvar')
clearFile = clear1.button('Apagar dados')


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

my_expander = st.beta_expander("Dados:", expanded=True)
table = my_expander.table(state.entrada)