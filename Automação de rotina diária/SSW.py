import requests
import pandas as pd
from Variaveis import itens_ign, all_index, indexes, meses, mes_atual, ano_atual

url = 'https://ssw.inf.br/api/tracking'
cnpj = '00069957000194'
path = r'K:/CWB/Logistica/Rastreamento/Controle_Monitoramento/MONITORAMENTO 2021 v.1.2.xlsx'
name_m_atual = meses[str(int(mes_atual))].upper() + '-' + str(ano_atual)
name_m_ant = meses[str(int(mes_atual) - 1)].upper() + '-' + str(ano_atual)


def search_data(mes):
    df = pd.read_excel(path, mes)
    df.columns = all_index
    df.fillna(0)
    df = df.query(
        "Fantasia_Do_Transportador != 'MALBEC' & Fantasia_Do_Transportador != 'URANOLOG' &\
        Fantasia_Do_Transportador != 'JOHNKE TRANSPORTES' & Fantasia_Do_Transportador > '0' &\
         Fantasia_Do_Transportador != 'ALIANCA' & Fantasia_Do_Transportador != 'GRANDE ADEGA - MATRIZ' &\
          Fantasia_Do_Transportador != 'TRANSFRIOS TRANSP' & Fantasia_Do_Transportador != 'BRINGER DO BRASIL' &\
           Fantasia_Do_Transportador != 'GRANDE ADEGA' & Fantasia_Do_Transportador != 'TRANSFRIOS SP' & D_Entrega == '-'")
    nf = []

    for x in df['Número']:

        nro_nf = x

        request = requests.post(url=url, data={'cnpj': cnpj, 'nro_nf': nro_nf})

        info = []
        inf = []
        cont = 0
        for stat in request.text.split(sep='<'):

            stat = stat.replace('/', '')
            stat = stat.replace('>', '; ')
            if 'success; false' in stat:
                continue
            if stat in itens_ign:
                continue
            elif 'tipo' in stat:
                continue
            elif 'tracking' in stat:
                continue
            elif 'message' in stat:
                continue
            elif 'remetente' in stat:
                continue
            elif 'destinatario' in stat:
                continue
            elif 'success' in stat:
                continue
            elif 'efetiva' in stat:
                continue
            stat = stat.split(';')
            if cont == 0:
                inf.append(nro_nf)
            if cont == 5:
                cont = 0
                info.append(inf)
                inf = []
            else:
                inf.append(stat[1])
                cont += 1
        try:
            nf.append(info[-1])
        except IndexError:
            pass
            info = []

    df_ssw = pd.DataFrame(data=nf, columns=indexes)
    print(df_ssw)
    writer = pd.ExcelWriter(path=r'K:/CWB/Logistica/Rastreamento/Patrick/Teste/teste' + mes + '.xlsx', engine='openpyxl')
    df_ssw.to_excel(excel_writer=writer, index=False)
    writer.save()

    return df_ssw


search_data(name_m_atual)
search_data(name_m_ant)
