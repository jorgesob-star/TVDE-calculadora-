import streamlit as st

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Descontos", layout="centered", page_icon="💸")
st.title("💸 Comparador de Descontos: Alugado vs Próprio")

# --- Valores padrão ---
DEFAULTS = {
    'aluguer': 280.0,
    'perc_aluguer': 7.0,
    'seguro': 45.0,
    'perc_seguro': 12.0,
    'manutencao': 50.0
}

# Inicializa o estado da sessão
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Sidebar ---
with st.sidebar:
    st.header("ℹ️ Sobre o App")
    st.info("""
    Esta ferramenta ajuda a comparar financeiramente duas opções:
    - **Opção 1 (Alugado)**: Desconto percentual + valor fixo de aluguer
    - **Opção 2 (Próprio)**: Desconto percentual + seguro + manutenção
    """)
    st.header("📝 Instruções")
    st.write("""
    1. Preencha os valores de entrada
    2. Ajuste as opções se necessário
    3. Clique em 'Calcular' para ver os resultados
    """)

# --- Entradas principais com session_state ---
st.header("📋 Entradas do Usuário")
col1, col2, col3 = st.columns(3)

with col1:
    if 'apuro' not in st.session_state:
        st.session_state.apuro = 700.0
    apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=st.session_state.apuro, step=10.0)
    st.session_state.apuro = apuro

with col2:
    if 'desc_combustivel' not in st.session_state:
        st.session_state.desc_combustivel = 200.0
    desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=st.session_state.desc_combustivel, step=1.0)
    st.session_state.desc_combustivel = desc_combustivel

with col3:
    if 'horas_trabalho' not in st.session_state:
        st.session_state.horas_trabalho = 40.0
    horas_trabalho = st.number_input("⏱️ Horas trabalhadas", min_value=1.0, value=st.session_state.horas_trabalho, step=1.0)
    st.session_state.horas_trabalho = horas_trabalho

st.markdown("---")

# --- Opções da empresa ---
st.header("⚙️ Opções da Empresa")
if st.button("🔧 Modificar Opções Padrão", type="secondary"):
    st.session_state.show_inputs = not st.session_state.show_inputs

if st.session_state.show_inputs:
    st.subheader("Configurações Personalizadas")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏢 Opção Alugado")
        st.number_input("Aluguer mensal (€)", min_value=0.0, value=st.session_state.aluguer, step=1.0, key='aluguer')
        st.number_input("Percentual de desconto (%)", min_value=0.0, value=st.session_state.perc_aluguer, step=0.5, key='perc_aluguer')
    with col2:
        st.markdown("#### 🚗 Opção Próprio")
        st.number_input("Seguro mensal (€)", min_value=0.0, value=st.session_state.seguro, step=1.0, key='seguro')
        st.number_input("Percentual de desconto (%)", min_value=0.0, value=st.session_state.perc_seguro, step=0.5, key='perc_seguro')
        st.number_input("Manutenção mensal (€)", min_value=0.0, value=st.session_state.manutencao, step=1.0, key='manutencao')
else:
    st.info("ℹ️ Usando valores padrão. Clique em 'Modificar Opções Padrão' para personalizar.")

st.markdown("---")

# --- Função para barras horizontais ---
def barra_horizontal(valor, label, cor, max_valor, formato="€"):
    proporcao = min(abs(valor) / max_valor, 1) if max_valor > 0 else 0
    valor_formatado = f"{valor:,.2f}{formato}" if formato == "€" else f"{valor:,.2f}{formato}"
    st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:10px;">
            <div style="width:120px; font-weight:bold;">{label}</div>
            <div style="flex:1; background-color:#f0f0f0; border-radius:8px; height:30px; box-shadow:inset 0 1px 3px rgba(0,0,0,0.2);">
                <div style="width:{proporcao*100}%; background-color:{cor}; height:100%; border-radius:8px; 
                            display:flex; align-items:center; padding-right:10px; justify-content:flex-end; 
                            color:white; font-weight:bold; font-size:0.9em; box-shadow:0 2px 4px rgba(0,0,0,0.2);">
                    {valor_formatado if proporcao > 0.3 else ""}
                </div>
            </div>
            <div style="width:100px; text-align:right; font-weight:bold; padding-left:10px;">
                {valor_formatado}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Cálculo e Visualização ---
if st.button("Calcular 🔍", type="primary", use_container_width=True):
    opcoes = {k: st.session_state[k] for k in ['aluguer', 'perc_aluguer', 'seguro', 'perc_seguro', 'manutencao']}

    # Descontos
    desconto_empresa_alugado = apuro * opcoes['perc_aluguer'] / 100
    desconto_empresa_proprio = apuro * opcoes['perc_seguro'] / 100

    # Custos fixos
    custos_fixos_alugado = opcoes['aluguer']
    custos_fixos_proprio = opcoes['seguro'] + opcoes['manutencao']

    # Sobra final
    sobra_opcao1 = apuro - desconto_empresa_alugado - custos_fixos_alugado - desc_combustivel
    sobra_opcao2 = apuro - desconto_empresa_proprio - custos_fixos_proprio - desc_combustivel

    # Ganho por hora
    ganho_hora_opcao1 = sobra_opcao1 / max(horas_trabalho, 1)
    ganho_hora_opcao2 = sobra_opcao2 / max(horas_trabalho, 1)

    # Melhor opção
    if sobra_opcao1 > sobra_opcao2:
        melhor_idx = 0
        diferenca = sobra_opcao1 - sobra_opcao2
        percentual_diferenca = (diferenca / sobra_opcao2) * 100 if sobra_opcao2 != 0 else 0
    elif sobra_opcao2 > sobra_opcao1:
        melhor_idx = 1
        diferenca = sobra_opcao2 - sobra_opcao1
        percentual_diferenca = (diferenca / sobra_opcao1) * 100 if sobra_opcao1 != 0 else 0
    else:
        melhor_idx = -1
        diferenca = 0
        percentual_diferenca = 0

    # --- Resultados ---
    st.subheader("📊 Resultados")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Apuro Bruto", f"{apuro:,.2f} €")
    with col2:
        st.metric("Combustível", f"{desc_combustivel:,.2f} €")
    with col3:
        if melhor_idx != -1:
            st.metric("Diferença", f"{diferenca:,.2f} €", f"{percentual_diferenca:+.1f}%")

    st.markdown("---")

    tab1, tab2 = st.tabs(["📈 Dashboard Visual", "🧮 Detalhes dos Cálculos"])
    
    with tab1:
        st.write("### Comparação Visual")
        max_sobra = max(abs(sobra_opcao1), abs(sobra_opcao2), 1)
        max_ganho = max(abs(ganho_hora_opcao1), abs(ganho_hora_opcao2), 1)
        container = st.container()
        with container:
            st.write("**Sobra Final (€)**")
            barra_horizontal(sobra_opcao1, f"Alugado {'🏆' if melhor_idx==0 else ''}", '#4caf50' if melhor_idx==0 else '#a5d6a7', max_sobra)
            barra_horizontal(sobra_opcao2, f"Próprio {'🏆' if melhor_idx==1 else ''}", '#2196f3' if melhor_idx==1 else '#90caf9', max_sobra)
            st.write("**Ganho por Hora (€/h)**")
            barra_horizontal(ganho_hora_opcao1, f"Alugado {'🏆' if melhor_idx==0 else ''}", '#4caf50' if melhor_idx==0 else '#a5d6a7', max_ganho, "€/h")
            barra_horizontal(ganho_hora_opcao2, f"Próprio {'🏆' if melhor_idx==1 else ''}", '#2196f3' if melhor_idx==1 else '#90caf9', max_ganho, "€/h")

        st.markdown("---")
        if melhor_idx == 0:
            st.success(f"**🎉 Recomendação: Opção Alugado**\n- Diferença: {diferenca:,.2f} €\n- Ganho/h: {ganho_hora_opcao1:,.2f} €/h")
        elif melhor_idx == 1:
            st.success(f"**🎉 Recomendação: Opção Próprio**\n- Diferença: {diferenca:,.2f} €\n- Ganho/h: {ganho_hora_opcao2:,.2f} €/h")
        else:
            st.info("ℹ️ Ambas as opções resultam no mesmo valor financeiro.")

    with tab2:
        st.write("### Detalhamento dos Cálculos")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏢 Opção Alugado")
            st.write(f"""
            - **Apuro Bruto:** {apuro:,.2f} €
            - Desconto da Empresa ({opcoes['perc_aluguer']}%): -{desconto_empresa_alugado:,.2f} €
            - Custo do Aluguer: -{custos_fixos_alugado:,.2f} €
            - Combustível: -{desc_combustivel:,.2f} €
            ---
            - **Sobra Final:** {sobra_opcao1:,.2f} €
            - Ganho por Hora: {ganho_hora_opcao1:,.2f} €/h
            """)
        with col2:
            st.markdown("#### 🚗 Opção Próprio")
            st.write(f"""
            - **Apuro Bruto:** {apuro:,.2f} €
            - Desconto da Empresa ({opcoes['perc_seguro']}%): -{desconto_empresa_proprio:,.2f} €
            - Custo do Seguro: -{opcoes['seguro']:,.2f} €
            - Custo de Manutenção: -{opcoes['manutencao']:,.2f} €
            - Combustível: -{desc_combustivel:,.2f} €
            ---
            - **Sobra Final:** {sobra_opcao2:,.2f} €
            - Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h
            """)

# --- Rodapé ---
st.markdown("---")
st.caption("© 2025 Comparador de Descontos - Desenvolvido para auxiliar na análise financeira de opções de veículo")
