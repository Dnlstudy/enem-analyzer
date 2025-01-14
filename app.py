import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Configuração da página (DEVE ser o primeiro comando st)
st.set_page_config(
    page_title="Análise ENEM 2024",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Forçar tema escuro
st.markdown("""
    <script>
        var observer = new MutationObserver(function(mutations) {
            const iframe = document.querySelector('iframe[title="streamlit_option_menu.streamlit_option_menu"]');
            if (iframe) {
                document.documentElement.setAttribute('data-theme', 'dark');
                observer.disconnect();
            }
        });
        observer.observe(document, {childList: true, subtree: true});
    </script>
""", unsafe_allow_html=True)

# Configurar tema escuro
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0E1117;
        }
        [data-testid="stHeader"] {
            background-color: #0E1117;
        }
        [data-testid="stToolbar"] {
            display: none;
        }
        [data-testid="stSidebar"] {
            background-color: #0E1117;
        }
        .main {
            background-color: #0E1117;
        }
        
        /* Estilo dos cards */
        .metric-card {
            background-color: #1E1E1E;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #333;
            text-align: center;
            margin: 0.5rem 0;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #00FF00;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            font-size: 1rem;
            color: #CCC;
        }
        
        /* Títulos */
        h1 {
            color: #00FF00;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
            text-align: center;
        }
        h2 {
            color: #00FF00;
            font-size: 1.8rem;
            margin-top: 2rem;
        }
        h3 {
            color: #00FF00;
            font-size: 1.3rem;
            margin-top: 1.5rem;
        }
        
        /* Inputs e botões */
        .stNumberInput > div > div > input {
            color: #FFF;
            background-color: #1E1E1E;
            border: 1px solid #333;
        }
        .stSelectbox > div > div {
            background-color: #1E1E1E;
            color: #FFF;
        }
        .stRadio > div {
            background-color: #1E1E1E;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #333;
            color: #FFF;
        }
        
        /* Expansores */
        .streamlit-expanderHeader {
            background-color: #1E1E1E;
            color: #FFF;
            border: 1px solid #333;
        }
        .streamlit-expanderContent {
            background-color: #1E1E1E;
            color: #FFF;
            border: 1px solid #333;
        }
        
        /* Alertas */
        .stAlert {
            background-color: #1E1E1E;
            color: #FFF;
            border: 1px solid #333;
        }
        
        /* Divisor de seções */
        hr {
            margin: 2rem 0;
            border-color: #333;
        }

        /* Esconder elementos do tema claro */
        section[data-testid="stSidebar"] div[data-testid="stToolbar"],
        section[data-testid="stSidebar"] button[kind="header"] {
            display: none;
        }

        /* Forçar tema escuro em todos os elementos */
        .stApp, .css-1d391kg, .css-1p05t8e {
            background-color: #0E1117 !important;
        }
        
        .stTextInput>div>div>input {
            background-color: #1E1E1E !important;
            color: white !important;
        }
        
        .stSelectbox>div>div>div {
            background-color: #1E1E1E !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('planilha.xlsx')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.stop()

try:
    df = load_data()
    if 'NU_NOTACORTE' in df.columns:
        df['NU_NOTACORTE'] = pd.to_numeric(df['NU_NOTACORTE'], errors='coerce')
    if 'NO_CURSO' in df.columns:
        df['NO_CURSO'] = df['NO_CURSO'].astype(str)
    if 'SG_UF_CAMPUS' in df.columns:
        df['SG_UF_CAMPUS'] = df['SG_UF_CAMPUS'].astype(str)
except Exception as e:
    st.error("Erro ao carregar os dados. Verifique se o arquivo 'planilha.xlsx' está na pasta correta.")
    st.stop()

# Título principal
st.title("📚 Análise ENEM 2024")

# Container centralizado para o input da nota
col1, col2, col3 = st.columns([1,2,1])
with col2:
    nota_usuario = st.number_input(
        "Digite sua nota do ENEM:",
        min_value=0.0,
        max_value=1000.0,
        value=None,
        step=1.0,
        help="Digite sua nota do ENEM (entre 0 e 1000)"
    )

# Só mostra o resto se a nota for inserida e for maior que zero
if nota_usuario:
    st.markdown("---")  # Divisor
    
    # Seleção de curso e tipo de concorrência em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        curso = st.selectbox(
            "Selecione seu curso:",
            options=sorted(df['NO_CURSO'].unique()),
            help="Escolha o curso que você quer analisar"
        )
    
    with col2:
        tipo_concorrencia = st.radio(
            "Tipo de Concorrência:",
            ["Ampla Concorrência", "Cotas"],
            help="Escolha entre Ampla Concorrência ou Cotas"
        )
    
    # Filtragem dos dados
    if tipo_concorrencia == "Ampla Concorrência":
        df_filtered = df[(df['NO_CURSO'] == curso) & (df['TIPO_CONCORRENCIA'] == 'AC')]
    else:
        df_filtered = df[(df['NO_CURSO'] == curso) & (df['TIPO_CONCORRENCIA'] != 'AC')]
    
    # Análise dos resultados
    if not df_filtered.empty:
        st.markdown("---")  # Divisor
        
        total_vagas = len(df_filtered)
        vagas_aprovadas = len(df_filtered[df_filtered['NU_NOTACORTE'] <= nota_usuario])
        media_notas = df_filtered['NU_NOTACORTE'].mean()
        
        # Métricas em cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_vagas}</div>
                    <div class="metric-label">Total de Vagas</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{vagas_aprovadas}</div>
                    <div class="metric-label">Aprovações Possíveis</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{media_notas:.1f}</div>
                    <div class="metric-label">Nota de Corte Média</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Lista de aprovações
        if vagas_aprovadas > 0:
            st.markdown("---")  # Divisor
            st.markdown("### 🎓 Onde Você Seria Aprovado")
            
            aprovacoes = df_filtered[df_filtered['NU_NOTACORTE'] <= nota_usuario].sort_values('NU_NOTACORTE', ascending=False)
            
            for _, row in aprovacoes.iterrows():
                with st.expander(f"🏛️ {row['SG_IES']} - {row['SG_UF_CAMPUS']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<div style='color: #FFFFFF;'><strong>Nota de Corte:</strong> {row['NU_NOTACORTE']:.1f}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='color: #FFFFFF;'><strong>Sua Nota Está Acima:</strong> {nota_usuario - row['NU_NOTACORTE']:.1f} pontos</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div style='color: #FFFFFF;'><strong>Modalidade:</strong> {row['DS_MOD_CONCORRENCIA']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='color: #FFFFFF;'><strong>Estado:</strong> {row['SG_UF_CAMPUS']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("---")  # Divisor
            st.warning("⚠️ Com sua nota atual, você não seria aprovado em nenhuma vaga nas condições selecionadas.")
            
            menor_nota = df_filtered['NU_NOTACORTE'].min()
            if not pd.isna(menor_nota):
                pontos_faltantes = menor_nota - nota_usuario
                st.info(f"""
                    💡 **Dicas para Aumentar suas Chances:**
                    - Você precisa de mais {pontos_faltantes:.1f} pontos para atingir a menor nota de corte
                    - Considere verificar outros cursos similares
                    - Explore diferentes modalidades de concorrência
                    - Continue se preparando para melhorar sua nota!
                """)
    else:
        st.error("Não foram encontradas vagas para as condições selecionadas.")

# Adiciona um espaço antes do footer
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer com informações
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; background-color: #1E1E1E; padding: 10px; text-align: center; border-top: 1px solid #333;'>
    <p style='color: #FFFFFF; margin: 0;'>
        Dados retirados do site do MEC • Atualizado em 14/01/2025 • 
        Desenvolvido por <a href='https://x.com/danielstudytwt' target='_blank' style='color: #00FF00; text-decoration: none;'>@danielstudytwt</a>
    </p>
</div>
""", unsafe_allow_html=True)
