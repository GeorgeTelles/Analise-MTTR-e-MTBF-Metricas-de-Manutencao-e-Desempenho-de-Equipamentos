import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

equipamentos_df = pd.read_excel('Equipamentos_e_Falhas_Refinaria.xlsx', sheet_name='Equipamentos')
falhas_df = pd.read_excel('Equipamentos_e_Falhas_Refinaria.xlsx', sheet_name='Equipamentos_Falha')
manutencao_preventiva_df = pd.read_excel('Equipamentos_e_Falhas_Refinaria.xlsx', sheet_name='Manutencao_Preventiva')

falhas_df['Data_Falha'] = pd.to_datetime(falhas_df['Data_Falha'])
falhas_df['Data_Resolução'] = pd.to_datetime(falhas_df['Data_Resolução'])
falhas_df = falhas_df.sort_values(by='Data_Falha', ascending=True)

# Calculo do tempo de inatividade e tempo de reparo
falhas_df['Tempo_Parada_Horas'] = (falhas_df['Data_Resolução'] - falhas_df['Data_Falha']).dt.total_seconds() / 3600
falhas_df['Tempo_Reparo_Horas'] = falhas_df['Tempo_Parada_Horas']  # Supondo que o tempo de reparo é igual ao tempo de parada

# Calcular o MTTR (Tempo Médio para Reparo)
mttr_por_equipamento = falhas_df.groupby('ID_Equipamento')['Tempo_Reparo_Horas'].mean().reset_index()
mttr_por_equipamento.columns = ['ID_Equipamento', 'MTTR_Horas']

# Calcular o MTBF (Tempo Médio Entre Falhas)
falhas_df['Tempo_Entre_Falhas_Horas'] = falhas_df.groupby('ID_Equipamento')['Data_Falha'].diff().dt.total_seconds() / 3600
mtbf_por_equipamento = falhas_df.groupby('ID_Equipamento')['Tempo_Entre_Falhas_Horas'].mean().reset_index()
mtbf_por_equipamento.columns = ['ID_Equipamento', 'MTBF_Horas']

# Juntar as métricas MTTR e MTBF
analise_metrica = pd.merge(mttr_por_equipamento, mtbf_por_equipamento, on='ID_Equipamento')

analise_metrica = pd.merge(analise_metrica, equipamentos_df[['ID_Equipamento', 'Nome_Equipamento', 'Tipo']], on='ID_Equipamento')

print(analise_metrica)

# Gráfico de MTTR
fig_mttr = px.bar(analise_metrica, x='MTTR_Horas', y='Nome_Equipamento',
                  title='Tempo Médio para Reparo (MTTR) por Equipamento',
                  labels={'MTTR_Horas': 'Tempo de Reparo (Horas)', 'Nome_Equipamento': 'Equipamento'},
                  color_discrete_sequence=px.colors.qualitative.Set1)
fig_mttr.update_layout(barmode='group', height=800)

# Gráfico de MTBF
fig_mtbf = px.bar(analise_metrica, x='MTBF_Horas', y='Nome_Equipamento', 
                  title='Tempo Médio Entre Falhas (MTBF) por Equipamento',
                  labels={'MTBF_Horas': 'Tempo Entre Falhas (Horas)', 'Nome_Equipamento': 'Equipamento'},
                  color_discrete_sequence=px.colors.sequential.Viridis)
fig_mtbf.update_layout(barmode='group', height=800)

fig_mttr.show()
fig_mtbf.show()

# Análise de Custo de Manutenção
print(falhas_df['Custo_Manutencao'].head())

# Limpar a coluna de Custo_Manutencao para remover 'R$', vírgulas e '00'
falhas_df['Custo_Manutencao'] = falhas_df['Custo_Manutencao'].apply(
    lambda x: str(x).replace('R$', '').replace(',', '').replace('00', '').strip())
# Converter a coluna para float após a limpeza
falhas_df['Custo_Manutencao'] = falhas_df['Custo_Manutencao'].astype(float)

# Verificar a coluna após a conversão
print(falhas_df['Custo_Manutencao'].head())

custo_manutencao_por_equipamento = falhas_df.groupby('ID_Equipamento')['Custo_Manutencao'].sum().reset_index()
custo_manutencao_por_equipamento = pd.merge(custo_manutencao_por_equipamento, equipamentos_df[['ID_Equipamento', 'Nome_Equipamento']], on='ID_Equipamento')

# Plotar gráfico de custo de manutenção
fig_custo_manutencao = px.bar(custo_manutencao_por_equipamento, x='Custo_Manutencao', y='Nome_Equipamento', 
                              title='Custo Total de Manutenção por Equipamento',
                              labels={'Custo_Manutencao': 'Custo de Manutenção (R$)', 'Nome_Equipamento': 'Equipamento'},
                              color_discrete_sequence=px.colors.sequential.Viridis)
fig_custo_manutencao.update_layout(height=800)

fig_custo_manutencao.show()

# Análise de Causa de Falha
causas_falha_mais_frequentes = falhas_df['Causa_Falha'].value_counts().reset_index()
causas_falha_mais_frequentes.columns = ['Causa_Falha', 'Contagem']

# Plotar gráfico de causas de falha
fig_causas_falha = px.bar(causas_falha_mais_frequentes, x='Contagem', y='Causa_Falha', 
                          title='Causas de Falha Mais Frequentes',
                          labels={'Contagem': 'Número de Ocorrências', 'Causa_Falha': 'Causa da Falha'},
                          color_discrete_sequence=px.colors.qualitative.Set2)
fig_causas_falha.update_layout(height=800)

fig_causas_falha.show()

# 5 equipamentos com maior MTBF
top_5_mtbf = analise_metrica.nlargest(5, 'MTBF_Horas')

# 5 equipamentos com maior MTTR
top_5_mttr = analise_metrica.nlargest(5, 'MTTR_Horas')

# 5 equipamentos com menor MTBF
bottom_5_mtbf = analise_metrica.nsmallest(5, 'MTBF_Horas')

# 5 equipamentos com menor MTTR
bottom_5_mttr = analise_metrica.nsmallest(5, 'MTTR_Horas')

# Plotar gráficos

# Gráfico MTBF para os 5 maiores
fig_top_5_mtbf = px.bar(top_5_mtbf, x='MTBF_Horas', y='Nome_Equipamento', color='Nome_Equipamento', 
                        title='Top 5 Equipamentos com Maior MTBF - tempo médio entre as falhas',
                        labels={'MTBF_Horas': 'Tempo Entre Falhas (Horas)', 'Nome_Equipamento': 'Equipamento'},
                        color_discrete_sequence=px.colors.sequential.Plasma)
fig_top_5_mtbf.update_layout(height=800)

# Gráfico MTTR para os 5 maiores
fig_top_5_mttr = px.bar(top_5_mttr, x='MTTR_Horas', y='Nome_Equipamento', color='Nome_Equipamento', 
                        title='Top 5 Equipamentos com Maior MTTR - tempo médio de reparo',
                        labels={'MTTR_Horas': 'Tempo de Reparo (Horas)', 'Nome_Equipamento': 'Equipamento'},
                        color_discrete_sequence=px.colors.sequential.Viridis)
fig_top_5_mttr.update_layout(height=800)

# Gráfico MTBF para os 5 menores
fig_bottom_5_mtbf = px.bar(bottom_5_mtbf, x='MTBF_Horas', y='Nome_Equipamento', color='Nome_Equipamento', 
                           title='Top 5 Equipamentos com Menor MTBF - Tempo médio entre falhas',
                           labels={'MTBF_Horas': 'Tempo Entre Falhas (Horas)', 'Nome_Equipamento': 'Equipamento'},
                           color_discrete_sequence=px.colors.sequential.RdBu)
fig_bottom_5_mtbf.update_layout(height=800)

# Gráfico de MTTR para os 5 menores
fig_bottom_5_mttr = px.bar(bottom_5_mttr, x='MTTR_Horas', y='Nome_Equipamento', color='Nome_Equipamento', 
                           title='Top 5 Equipamentos com Menor MTTR - tempo médio de reparo',
                           labels={'MTTR_Horas': 'Tempo de Reparo (Horas)', 'Nome_Equipamento': 'Equipamento'},
                           color_discrete_sequence=px.colors.sequential.Viridis)
fig_bottom_5_mttr.update_layout(height=800)

fig_top_5_mtbf.show()
fig_top_5_mttr.show()
fig_bottom_5_mtbf.show()
fig_bottom_5_mttr.show()
