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

# --- Sidebar para informações adicionais ---
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

# --- Entradas principais ---
st.header("📋 Entradas do Usuário")
col1, col2, col3 = st.columns(3)
with col1:
    apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=700.0, step=10.0, 
                           help="Valor total recebido antes de quaisquer descontos")
with col2:
    desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0,
                                      help="Valor descontado para combustível")
with col3:
    horas_trabalho = st.number_input("⏱️ Horas trabalhadas", min_value=1.0, value=40.0, step=1.0,
                                    help="Total de horas trabalhadas no período")

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
        st.number_input("Aluguer mensal (€)", min_value=0.0, value=st.session_state.aluguer, 
                       step=1.0, key='aluguer', help="Custo fixo do aluguer do veículo")
        st.number_input("Percentual de desconto (%)", min_value=0.0, value=st.session_state.perc_aluguer, 
                       step=0.5, key='perc_aluguer', help="Percentual descontado pela empresa")
    with col2:
        st.markdown("#### 🚗 Opção Próprio")
        st.number_input("Seguro mensal (€)", min_value=0.0, value=st.session_state.seguro, 
                       step=1.0, key='seguro', help="Custo do seguro do veículo")
        st.number_input("Percentual de desconto (%)", min_value=0.0, value=st.session_state.perc_seguro, 
                       step=0.5, key='perc_seguro', help="Percentual descontado pela empresa")
        st.number_input("Manutenção mensal (€)", min_value=0.0, value=st.session_state.manutencao, 
                       step=1.0, key='manutencao', help="Custo estimado de manutenção")
else:
    st.info("ℹ️ Usando valores padrão. Clique em 'Modificar Opções Padrão' para personalizar.")

st.markdown("---")

# --- Função para barras horizontais melhorada ---
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
    # Preparar dados
    apuro_liquido = apuro - desc_combustivel
    opcoes = {k: st.session_state[k] for k in ['aluguer', 'perc_aluguer', 'seguro', 'perc_seguro', 'manutencao']}

    # Cálculos
    desconto_opcao1 = apuro * opcoes['perc_aluguer'] / 100
    desconto_opcao2 = apuro * opcoes['perc_seguro'] / 100
    
    sobra_opcao1 = apuro_liquido - desconto_opcao1 - opcoes['aluguer']
    sobra_opcao2 = apuro_liquido - desconto_opcao2 - opcoes['seguro'] - opcoes['manutencao']

    ganho_hora_opcao1 = sobra_opcao1 / max(horas_trabalho, 1)
    ganho_hora_opcao2 = sobra_opcao2 / max(horas_trabalho, 1)

    # Melhor opção
    if sobra_opcao1 > sobra_opcao2:
        melhor_idx = 0
        diferenca = sobra_opcao1 - sobra_opcao2
        percentual_diferenca = (diferenca / sobra_opcao2) * 100
    elif sobra_opcao2 > sobra_opcao1:
        melhor_idx = 1
        diferenca = sobra_opcao2 - sobra_opcao1
        percentual_diferenca = (diferenca / sobra_opcao1) * 100
    else:
        melhor_idx = -1
        diferenca = 0
        percentual_diferenca = 0

    # --- Resultados ---
    st.subheader("📊 Resultados")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Apuro Líquido", f"{apuro_liquido:,.2f} €")
    with col2:
        st.metric("Horas Trabalhadas", f"{horas_trabalho:,.0f} h")
    with col3:
        if melhor_idx != -1:
            st.metric("Diferença", f"{diferenca:,.2f} €", f"{percentual_diferenca:+.1f}%")

    st.markdown("---")

    # --- Abas ---
    tab1, tab2 = st.tabs(["📈 Dashboard Visual", "🧮 Detalhes dos Cálculos"])
    
    with tab1:
        st.write("### Comparação Visual")
        
        # Determinar valores máximos para escala
        max_sobra = max(abs(sobra_opcao1), abs(sobra_opcao2), 1)
        max_ganho = max(abs(ganho_hora_opcao1), abs(ganho_hora_opcao2), 1)
        
        # Container para os gráficos
        container = st.container()
        
        with container:
            st.write("**Sobra Final (€)**")
            barra_horizontal(sobra_opcao1, f"Alugado {'🏆' if melhor_idx==0 else ''}", 
                            '#4caf50' if melhor_idx==0 else '#a5d6a7', max_sobra)
            barra_horizontal(sobra_opcao2, f"Próprio {'🏆' if melhor_idx==1 else ''}", 
                            '#2196f3' if melhor_idx==1 else '#90caf9', max_sobra)
            
            st.write("**Ganho por Hora (€/h)**")
            barra_horizontal(ganho_hora_opcao1, f"Alugado {'🏆' if melhor_idx==0 else ''}", 
                            '#4caf50' if melhor_idx==0 else '#a5d6a7', max_ganho, "€/h")
            barra_horizontal(ganho_hora_opcao2, f"Próprio {'🏆' if melhor_idx==1 else ''}", 
                            '#2196f3' if melhor_idx==1 else '#90caf9', max_ganho, "€/h")

        # Mensagem de recomendação
        st.markdown("---")
        if melhor_idx == 0:
            st.success(f"""
            **🎉 Recomendação: Opção Alugado**
            
            A opção de veículo alugado é financeiramente mais vantajosa, proporcionando:
            - **{diferenca:,.2f} €** a mais por mês
            - **{percentual_diferenca:+.1f}%** de diferença
            - **{ganho_hora_opcao1:,.2f} €/h** vs {ganho_hora_opcao2:,.2f} €/h na opção próprio
            """)
        elif melhor_idx == 1:
            st.success(f"""
            **🎉 Recomendação: Opção Próprio**
            
            A opção de veículo próprio é financeiramente mais vantajosa, proporcionando:
            - **{diferenca:,.2f} €** a mais por mês
            - **{percentual_diferenca:+.1f}%** de diferença
            - **{ganho_hora_opcao2:,.2f} €/h** vs {ganho_hora_opcao1:,.2f} €/h na opção alugado
            """)
        else:
            st.info("ℹ️ Ambas as opções resultam no mesmo valor financeiro. Considere outros fatores como conveniência e flexibilidade.")

    with tab2:
        st.write("### Detalhamento dos Cálculos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 Opção Alugado")
            st.write(f"""
            - Apuro Líquido: {apuro_liquido:,.2f} €
            - Desconto da Empresa ({opcoes['perc_aluguer']}%): {desconto_opcao1:,.2f} €
            - Custo do Aluguer: {opcoes['aluguer']:,.2f} €
            - **Total de Descontos: {desconto_opcao1 + opcoes['aluguer']:,.2f} €**
            - **Sobra Final: {sobra_opcao1:,.2f} €**
            - Ganho por Hora: {ganho_hora_opcao1:,.2f} €/h
            """)
        
        with col2:
            st.markdown("#### 🚗 Opção Próprio")
            st.write(f"""
            - Apuro Líquido: {apuro_liquido:,.2f} €
            - Desconto da Empresa ({opcoes['perc_seguro']}%): {desconto_opcao2:,.2f} €
            - Custo do Seguro: {opcoes['seguro']:,.2f} €
            - Custo de Manutenção: {opcoes['manutencao']:,.2f} €
            - **Total de Descontos: {desconto_opcao2 + opcoes['seguro'] + opcoes['manutencao']:,.2f} €**
            - **Sobra Final: {sobra_opcao2:,.2f} €**
            - Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h
            """)

# --- Rodapé ---
st.markdown("---")
st.caption("© 2023 Comparador de Descontos - Desenvolvido para auxiliar na análise financeira de opções de veículo")
