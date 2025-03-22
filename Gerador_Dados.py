import pandas as pd
import random
import datetime

def gerar_dados_equipamentos(num_equipamentos):
    tipos_equipamentos = ['Bomba de Alta Pressão', 'Compressor de Gás', 'Válvula de Controle', 'Turbina a Gás', 'Gerador Elétrico']
    modelos = ['X100', 'V200', 'M300', 'T400', 'B500', 'T600']
    localizacoes = ['Seção de Destilação', 'Unidade de Craqueamento', 'Unidade de Hidrogenação', 'Seção de Recuperação de Solventes', 'Área de Geração de Energia']
    
    equipamentos = []
    for i in range(1, num_equipamentos + 1):
        equipamento = {
            'ID_Equipamento': i,
            'Nome_Equipamento': f'{tipos_equipamentos[random.randint(0, len(tipos_equipamentos) - 1)]} {chr(65 + i % 26)}',
            'Modelo': random.choice(modelos),
            'Tipo': random.choice(tipos_equipamentos),
            'Localizacao': random.choice(localizacoes),
            'Data_Aquisicao': str(datetime.date(random.randint(2015, 2022), random.randint(1, 12), random.randint(1, 28)))
        }
        equipamentos.append(equipamento)
    
    return pd.DataFrame(equipamentos)

def gerar_dados_falhas(num_falhas, num_equipamentos):
    causas_falha = [
        'Falha no sistema de bombeamento', 'Falha no compressor de gás', 'Corrosão na válvula de controle', 
        'Superaquecimento do compressor', 'Falha no gerador elétrico', 'Falha no sistema hidráulico', 
        'Falha no sistema de refrigeração', 'Falha elétrica', 'Vazamento de fluido', 'Falha no sistema de vácuo'
    ]
    tipos_manutencao = ['Corretiva', 'Preventiva', 'Preditiva']
    falhas = []
    
    for i in range(1, num_falhas + 1):
        equipamento_id = random.randint(1, num_equipamentos)
        data_falha = datetime.datetime(2025, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        tempo_parada = random.randint(2, 10)  # horas de parada
        tempo_reparo = random.randint(2, 6)  # horas de reparo
        data_resolucao = data_falha + datetime.timedelta(hours=tempo_parada + tempo_reparo)
        
        falha = {
            'ID_Falha': i,
            'ID_Equipamento': equipamento_id,
            'Data_Falha': data_falha,
            'Data_Resolução': data_resolucao,
            'Tempo_Parada': f'{tempo_parada} horas',
            'Causa_Falha': random.choice(causas_falha),
            'Tipo_Manutencao': random.choice(tipos_manutencao),
            'Tempo_Reparo': f'{tempo_reparo} horas',
            'Custo_Manutencao': f'R$ {random.randint(200, 5000)},00'
        }
        falhas.append(falha)
    
    return pd.DataFrame(falhas)

def gerar_dados_manutencao_preventiva(num_manutencao, num_equipamentos):
    manutencao_preventiva = []
    descricoes = ['Troca de óleo', 'Substituição de vedações', 'Inspeção de segurança', 'Limpeza de filtros', 'Troca de peças danificadas']
    
    for i in range(1, num_manutencao + 1):
        equipamento_id = random.randint(1, num_equipamentos)
        data_manutencao = datetime.datetime(2025, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
        manutencao = {
            'ID_Manutencao': i,
            'ID_Equipamento': equipamento_id,
            'Data_Manutencao': data_manutencao,
            'Tipo_Manutencao': 'Preventiva',
            'Descricao': random.choice(descricoes),
            'Custo_Manutencao': f'R$ {random.randint(100, 2000)},00'
        }
        manutencao_preventiva.append(manutencao)
    
    return pd.DataFrame(manutencao_preventiva)

num_equipamentos = 100
num_falhas = 400
num_manutencao = 200  # Exemplo de manutenções preventivas

equipamentos_df = gerar_dados_equipamentos(num_equipamentos)
falhas_df = gerar_dados_falhas(num_falhas, num_equipamentos)
manutencao_preventiva_df = gerar_dados_manutencao_preventiva(num_manutencao, num_equipamentos)

with pd.ExcelWriter('Equipamentos_e_Falhas_Refinaria.xlsx') as writer:
    equipamentos_df.to_excel(writer, sheet_name='Equipamentos', index=False)
    falhas_df.to_excel(writer, sheet_name='Equipamentos_Falha', index=False)
    manutencao_preventiva_df.to_excel(writer, sheet_name='Manutencao_Preventiva', index=False)

print("Planilha gerada com sucesso!")
