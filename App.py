import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Descontos", layout="centered")
st.title("💸 Calculadora de Descontos")
st.markdown("Calcule rapidamente os descontos do Uber, Patrão, Seguro e Combustível com visual intuitivo.")

# Entradas
st.subheader("Insira os valores:")
valor_inicial = st.number_input("💰 Valor inicial", min_value=0.0, value=1000.0, step=10.0)
perc_uber = st.number_input("🚗 Percentagem Uber (%)", min_value=0.0, value=25.0, step=1.0)
perc_pat = st.number_input("👔 Percentagem Patrão (%)", min_value=0.0, value=12.0, step=1.0)
desc_seguro = st.number_input("🛡️ Desconto Seguro (fixo)", min_value=0.0, value=100.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto Combustível (fixo)", min_value=0.0, value=80.0, step=10.0)

st.markdown("---")  # Separador

# Botão grande de cálculo
if st.button("Calcular 🔹", use_container_width=True):
    st.subheader("📊 Resultado detalhado:")

    # Uber
    desconto_uber = valor_inicial * (perc_uber / 100)
    valor = valor_inicial - desconto_uber
    st.markdown(f"<div style='background-color:#FFCCCC;padding:10px;border-radius:5px'>"
                f"- {perc_uber}% Uber: -{desconto_uber:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    # Patrão
    desconto_pat = valor * (perc_pat / 100)
    valor -= desconto_pat
    st.markdown(f"<div style='background-color:#CCE5FF;padding:10px;border-radius:5px'>"
                f"- {perc_pat}% Patrão: -{desconto_pat:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    # Seguro
    valor -= desc_seguro
    st.markdown(f"<div style='background-color:#CCFFCC;padding:10px;border-radius:5px'>"
                f"- Seguro: -{desc_seguro:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    # Combustível
    valor -= desc_combustivel
    st.markdown(f"<div style='background-color:#FFF2CC;padding:10px;border-radius:5px'>"
                f"- Combustível: -{desc_combustivel:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    # Valor final
    st.success(f"💰 Valor final após descontos: {valor:.2f}")
