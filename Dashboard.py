import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .main > div {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    .stApp {
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv('planilha.csv')

df = df.drop_duplicates(subset=['E-mail', 'Nome da empresa'])
df['País da empresa'] = df['País da empresa'].fillna('Desconhecido').astype(str).str.strip().str.title()
df['Cargo'] = df['Cargo'].str.strip().str.title()
df['Setor da empresa'] = df['Setor da empresa'].str.strip().str.title()
df['Nome da empresa'] = df['Nome da empresa'].str.strip().str.title()

flags = {
    'United Kingdom': '🇬🇧',
    'Germany': '🇩🇪',
    'France': '🇫🇷',
    'Spain': '🇪🇸',
    'Italy': '🇮🇹',
    'Netherlands': '🇳🇱',
    'Sweden': '🇸🇪',
    'Poland': '🇵🇱',
    'Belgium': '🇧🇪',
    'Switzerland': '🇨🇭',
    'Portugal': '🇵🇹',
    'Lithuania': '🇱🇹',
    'Afghanistan': '🇦🇫',
    'Australia': '🇦🇺',
    'Brazil': '🇧🇷',
    'Estonia':'🇪🇪',
    'Ireland':'🇮🇪',
    'Japan':'🇯🇵',
    'Mexico': '🇲🇽',
    'Singapore': '🇸🇬',
    'United Arab Emirates': '🇦🇪',
    'United States': '🇺🇸',
    'Desconhecido': '🌍'
}

def categorize_size(size_str):
    if pd.isna(size_str):
        return 'Unknown'
    size_str = str(size_str).strip()
    if size_str == '1-10':
        return 'S'
    elif size_str == '11-50':
        return 'M'
    elif size_str == '51-200':
        return 'L'
    elif size_str in ['201-500', '501-1000']:
        return 'G'
    elif size_str in ['1001-5000', '5001-10000', '10001+']:
        return 'XL'
    else:
        return 'Other'

df['Size Category'] = df['Tamanho da empresa'].apply(categorize_size)

st.markdown('<h1 style="font-size: 24px;">Análise de dados - hCaptcha</h1>', unsafe_allow_html=True)
st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)

countries = sorted([c for c in df['País da empresa'].unique() if c and c != 'Desconhecido'])
selected_country = st.selectbox(
    'Selecione um país:',
    options=countries,
    format_func=lambda c: f"{flags.get(c, '🌍')} {c}"
)

country_df = df[df['País da empresa'] == selected_country]

st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<h3 style="font-size: 35px;">Empresas</h3>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 50px;">{country_df["Nome da empresa"].nunique()}</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<h3 style="font-size: 35px;">Cargo</h3>', unsafe_allow_html=True)
    top_job = country_df['Cargo'].value_counts().idxmax()[:20] if not country_df.empty else 'N/A'
    st.markdown(f'<div style="font-size: 50px;">{top_job}</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<h3 style="font-size: 35px;">Setor</h3>', unsafe_allow_html=True)
    top_industry = country_df['Setor da empresa'].value_counts().idxmax()[:20] if not country_df.empty else 'N/A'
    st.markdown(f'<div style="font-size: 40px;">{top_industry}</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)

size_counts = country_df['Size Category'].value_counts().reindex(['S', 'M', 'L', 'G', 'XL'], fill_value=0)
fig_size = px.bar(x=size_counts.index, y=size_counts.values, labels={'x': 'Tamanho', 'y': 'Quantidade'})
fig_size.update_traces(
    marker_color=['#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336'],
    marker_line_color='black',
    marker_line_width=1.5
)
fig_size.update_layout(
    height=300,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Distribuição por Tamanho',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Tamanho da Empresa",
    yaxis_title="Quantidade",
    showlegend=False
)
with col4:
    st.plotly_chart(fig_size, use_container_width=True)

top_jobs = country_df['Cargo'].value_counts().head(5)
fig_jobs = px.bar(x=top_jobs.index, y=top_jobs.values, labels={'x': 'Cargo', 'y': 'Quantidade'})
fig_jobs.update_traces(
    marker_color=['#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336'],
    marker_line_color='black',
    marker_line_width=1
)
fig_jobs.update_layout(
    height=300,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Top 5 Cargos',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Cargos",
    yaxis_title="Quantidade",
    xaxis_tickangle=-45
)
with col5:
    st.plotly_chart(fig_jobs, use_container_width=True)

top_industries = country_df['Setor da empresa'].value_counts().head(5)
fig_industries = px.bar(x=top_industries.index, y=top_industries.values, labels={'x': 'Setor', 'y': 'Quantidade'})
fig_industries.update_traces(
    marker_color=['#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336'],
    marker_line_color='black',
    marker_line_width=1
)
fig_industries.update_layout(
    height=300,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Top 5 Setores',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Setores",
    yaxis_title="Quantidade",
    xaxis_tickangle=-45
)
with col6:
    st.plotly_chart(fig_industries, use_container_width=True)

st.divider()
st.markdown('<h2 style="font-size: 20px;">Dados Gerais</h2>', unsafe_allow_html=True)

country_counts = df.groupby('País da empresa')['Nome da empresa'].nunique().sort_values(ascending=False).head(15)
fig_countries = px.bar(x=country_counts.index, y=country_counts.values, labels={'x': 'País', 'y': 'Quantidade de Empresas'})
fig_countries.update_traces(
    marker_color=['#FFCE00', # Alemanha (amarelo)
 '#CF142B', # Reino Unido (vermelho)
 '#0055A4', # França (azul)
 '#AA151B', # Espanha (vermelho)
 '#006600', # Portugal (verde)
 '#DC143C', # Polônia (vermelho)
 '#FFCD00', # Bélgica (amarelo)
 '#169B62', # Irlanda (verde)
 '#FFB81C',
'#ff0000',
 '#3C3B6E', # Estados Unidos (azul)
 '#009C3B', # Brasil (verde)
 '#0072CE', # Estônia (azul)
 '#006847', # México (verde)
 '#D32011'] # Afeganistão (vermelho)
,
    marker_line_color='black',
    marker_line_width=1
)
fig_countries.update_layout(
    height=400,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Top 15 Países por Número de Empresas',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Países",
    yaxis_title="Quantidade de Empresas",
    xaxis_tickangle=-45
)
st.plotly_chart(fig_countries, use_container_width=True)

col7, col8 = st.columns(2)
global_top_jobs = df['Cargo'].value_counts().head(10)
fig_global_jobs = px.bar(x=global_top_jobs.index, y=global_top_jobs.values, labels={'x': 'Cargo', 'y': 'Quantidade'})
fig_global_jobs.update_traces(
    marker_color=['#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336','#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336'],
    marker_line_color='black',
    marker_line_width=1
)
fig_global_jobs.update_layout(
    height=400,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Top 10 Cargos Globais',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Cargos",
    yaxis_title="Quantidade",
    xaxis_tickangle=-45
)
with col7:
    st.plotly_chart(fig_global_jobs, use_container_width=True)

global_top_industries = df['Setor da empresa'].value_counts().head(10)
fig_global_industries = px.bar(x=global_top_industries.index, y=global_top_industries.values, labels={'x': 'Setor', 'y': 'Quantidade'})
fig_global_industries.update_traces(
    marker_color=['#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336','#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336'],
    marker_line_color='black',
    marker_line_width=1
)
fig_global_industries.update_layout(
    height=400,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Top 10 Setores Globais',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Setores",
    yaxis_title="Quantidade",
    xaxis_tickangle=-45
)
with col8:
    st.plotly_chart(fig_global_industries, use_container_width=True)
    
st.markdown('<h3 style="font-size: 18px;">Obs:</h3>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #747474">Tamanho das empresas: S = 1-10, M = 11-50, L = 51-200, G = 201-1000, XL = 1001+</li>', unsafe_allow_html=True)
    
global_size_counts = df['Size Category'].value_counts().reindex(['S', 'M', 'L', 'G', 'XL'], fill_value=0)
fig_global_size = px.bar(x=global_size_counts.index, y=global_size_counts.values, labels={'x': 'Tamanho', 'y': 'Quantidade'})
fig_global_size.update_traces(
    marker_color=['#4CAF50','#8BC34A','#2196F3','#9C27B0','#FF9800','#F44336'],
    marker_line_color='black',
    marker_line_width=1.5
)
fig_global_size.update_layout(
    height=400,
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=12, family='Arial'),
    title_text='Distribuição Global por Tamanho de Empresas',
    title_font_size=16,
    plot_bgcolor='#161616',
    paper_bgcolor='#161616',
    xaxis_title="Tamanho da Empresa",
    yaxis_title="Quantidade",
    showlegend=False
)
st.plotly_chart(fig_global_size, use_container_width=True)


st.markdown('<h3 style="font-size: 18px;">Insights💡</h3>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #D6D6D6"><span style="font-weight: 700; color:#2196F3"">Investir na alemanha</span></li>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #D6D6D6;list-style: square; margin-left:50px;"><span style="font-weight: 700; color:#2196F3"">Setor Dominante:</span> "Information Technology & Services" é o setor mais frequente na Alemanha, alinhado com a reputação do país como líder em inovação tecnológica.</li>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #D6D6D6;list-style: square; margin-left:50px;"><span style="font-weight: 700; color:#2196F3"">Oportunidades de Crescimento:</span> Empresas como "Thinkproject" (501-1000 funcionários) e "Evosoft" (1001-5000) indicam potencial para investimentos em empresas de médio a grande porte que podem expandir ainda mais.</li>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #D6D6D6;list-style: square; margin-left:50px;"><span style="font-weight: 700; color:#2196F3"">Riscos:</span> A tabela não mostra dados financeiros diretos (ex.: receita, lucro), então é preciso investigar a saúde financeira dessas empresas. Além disso, a dependência de TI pode ser vulnerável a mudanças tecnológicas rápidas.</li>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #D6D6D6">O cargo mais comum é <span style="font-weight: 700; color:#2196F3">Head of IT</span>, refletindo liderança técnica, enquanto <span style="font-weight: 700; color:#2196F3">Information Technology & Services</span> lidera como setor. Isso sugere investir em parcerias ou treinamentos para líderes de TI, aproveitando o crescimento do setor tecnológico. e  respectivamente</li>', unsafe_allow_html=True)
st.markdown('<li style="font-size: 20px; color: #D6D6D6">Empresas L (51-200 funcionários), como <span style="font-weight: 700; color:#2196F3"">PIKON Germany</span> e <span style="font-weight: 700; color:#2196F3"">Materna Virtual Solution GmbH</span>, são as mais frequentes. Focar nelas é estratégico, dado seu potencial de crescimento em TI e flexibilidade operacional.</li>', unsafe_allow_html=True)