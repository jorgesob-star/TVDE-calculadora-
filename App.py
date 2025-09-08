import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Calculadora TVDE Semanal",
    page_icon="🚗",
    layout="centered"
)

# Título da aplicação
st.title("🚗 Calculadora de Ganhos Semanais TVDE")
st.markdown("Calcule seus rendimentos líquidos semanais como motorista TVDE")

# Inicializar variáveis de sessão
if 'comissao_plataforma' not in st.session_state:
    st.session_state.comissao_plataforma = 6.0
if 'aluguer_semanal' not in st.session_state:
    st.session_state.aluguer_semanal = 270.0
if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False

# Função para alternar a visualização das configurações avançadas
def toggle_advanced():
    st.session_state.show_advanced = not st.session_state.show_advanced

# Botão para mostrar/ocultar configurações avançadas
st.button(
    "⚙️ Configurações Avançadas" if not st.session_state.show_advanced else "⬆️ Ocultar Configurações",
    on_click=toggle_advanced
)

# Mostrar configurações avançadas se o botão foi clicado
if st.session_state.show_advanced:
    with st.expander("Configurações Avançadas", expanded=True):
        st.session_state.comissao_plataforma = st.number_input(
            "Comissão da Plataforma (%)", 
            min_value=0.0, max_value=100.0, 
            value=st.session_state.comissao_plataforma, step=0.5,
            key="comissao_input"
        )
        st.session_state.aluguer_semanal = st.number_input(
            "Aluguer Semanal da Viatura (€)", 
            min_value=0.0, value=st.session_state.aluguer_semanal, step=10.0,
            key="aluguer_input"
        )

# Entradas principais do usuário
st.header("Entradas Semanais")

# Valores iniciais conforme solicitado
apuro_semanal = 1000.0
combustivel_semanal = 250.0

col1, col2 = st.columns(2)

with col1:
    dias_trabalhados = st.slider("Dias trabalhados na semana", 1, 7, 7)
    ganhos_brutos_semana = st.number_input(
        "Ganhos Brutos Semanais (€)", 
        min_value=0.0, 
        value=apuro_semanal, 
        step=10.0,
        help="Total de ganhos brutos na semana (apuro)"
    )

with col2:
    custo_gasolina_semana = st.number_input(
        "Custo com Gasolina Semanal (€)", 
        min_value=0.0, 
        value=combustivel_semanal, 
        step=10.0
    )
    outros_custos = st.number_input(
        "Outros Custos Semanais (€)", 
        min_value=0.0, 
        value=0.0, 
        step=5.0,
        help="Lavagens, portagens, estacionamento, etc."
    )

# Cálculos
comissao_valor_semana = ganhos_brutos_semana * (st.session_state.comissao_plataforma / 100)

ganhos_liquidos_semana = (ganhos_brutos_semana - comissao_valor_semana - 
                         custo_gasolina_semana - st.session_state.aluguer_semanal - outros_custos)

margem_lucro = (ganhos_liquidos_semana / ganhos_brutos_semana) * 100 if ganhos_brutos_semana > 0 else 0

# Exibir resultados
st.header("Resultados Semanais")

col1, col2, col3 = st.columns(3)
col1.metric("Ganhos Líquidos Semanais", f"€{ganhos_liquidos_semana:.2f}")
col2.metric("Comissão Plataforma", f"€{comissao_valor_semana:.2f}")
col3.metric("Margem de Lucro", f"{margem_lucro:.1f}%")

# Tabela de detalhamento
st.subheader("📊 Detalhamento dos Custos")
det_col1, det_col2 = st.columns(2)

with det_col1:
    st.write("**Ganhos:**")
    st.write(f"- Apuro Bruto: €{ganhos_brutos_semana:.2f}")
    st.write("")
    st.write("**Custos:**")
    st.write(f"- Comissão Plataforma: €{comissao_valor_semana:.2f}")
    st.write(f"- Gasolina: €{custo_gasolina_semana:.2f}")
    st.write(f"- Aluguer Viatura: €{st.session_state.aluguer_semanal:.2f}")
    st.write(f"- Outros Custos: €{outros_custos:.2f}")

with det_col2:
    st.write("**Totais:**")
    st.write(f"- Total Ganhos: €{ganhos_brutos_semana:.2f}")
    total_custos = comissao_valor_semana + custo_gasolina_semana + st.session_state.aluguer_semanal + outros_custos
    st.write(f"- Total Custos: €{total_custos:.2f}")
    st.write(f"- **Lucro Líquido: €{ganhos_liquidos_semana:.2f}**")
    st.write(f"- Margem de Lucro: {margem_lucro:.1f}%")

# Cálculo diário
st.subheader("💰 Médias Diárias")
ganho_bruto_diario = ganhos_brutos_semana / dias_trabalhados
ganho_liquido_diario = ganhos_liquidos_semana / dias_trabalhados

col1, col2 = st.columns(2)
col1.metric("Ganho Bruto Diário", f"€{ganho_bruto_diario:.2f}")
col2.metric("Ganho Líquido Diário", f"€{ganho_liquido_diario:.2f}")

# Projeção mensal
st.header("📈 Projeção Mensal")
dias_uteis_mes = st.slider("Dias úteis no mês", 20, 31, 25)
semanas_mes = dias_uteis_mes / dias_trabalhados
ganhos_mensais = ganhos_liquidos_semana * semanas_mes

proj_col1, proj_col2 = st.columns(2)
proj_col1.metric("Projeção de Ganhos Mensais", f"€{ganhos_mensais:.2f}")
proj_col2.metric("Média Diária Líquida", f"€{ganho_liquido_diario:.2f}")

# Resumo final
st.header("💶 Resumo Financeiro Semanal")
resumo_col1, resumo_col2, resumo_col3 = st.columns(3)
resumo_col1.metric("Apuro Semanal", f"€{ganhos_brutos_semana:.2f}")
resumo_col2.metric("Custos Semanais", f"€{total_custos:.2f}")
resumo_col3.metric("Lucro Semanal", f"€{ganhos_liquidos_semana:.2f}", 
                  delta=f"{margem_lucro:.1f}%")

# Mostrar valores ocultos apenas em modo avançado
if st.session_state.show_advanced:
    st.info(f"ℹ️ **Valores atuais das configurações avançadas:** Comissão: {st.session_state.comissao_plataforma}%, Aluguer: €{st.session_state.aluguer_semanal:.2f}")

# Rodapé
st.markdown("---")
st.caption("App desenvolvido para cálculo de ganhos no TVDE. Use o botão 'Configurações Avançadas' para ajustar a comissão e aluguer.")
