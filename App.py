# --- Cálculo e Visualização ---
if st.button("Calcular 🔍", type="primary", use_container_width=True):
    # Preparar dados
    opcoes = {k: st.session_state[k] for k in ['aluguer', 'perc_aluguer', 'seguro', 'perc_seguro', 'manutencao']}

    # Descontos da empresa (sempre sobre o apuro total bruto)
    desconto_empresa_alugado = apuro * opcoes['perc_aluguer'] / 100
    desconto_empresa_proprio = apuro * opcoes['perc_seguro'] / 100

    # Custos fixos
    custos_fixos_alugado = opcoes['aluguer']
    custos_fixos_proprio = opcoes['seguro'] + opcoes['manutencao']

    # Desconto de combustível (igual para ambas opções)
    desconto_combustivel = desc_combustivel

    # Sobra final
    sobra_opcao1 = apuro - desconto_empresa_alugado - custos_fixos_alugado - desconto_combustivel
    sobra_opcao2 = apuro - desconto_empresa_proprio - custos_fixos_proprio - desconto_combustivel

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
        st.metric("Combustível", f"{desconto_combustivel:,.2f} €")
    with col3:
        if melhor_idx != -1:
            st.metric("Diferença", f"{diferenca:,.2f} €", f"{percentual_diferenca:+.1f}%")

    st.markdown("---")

    # --- Abas ---
    tab1, tab2 = st.tabs(["📈 Dashboard Visual", "🧮 Detalhes dos Cálculos"])
    
    with tab1:
        st.write("### Comparação Visual")
        
        max_sobra = max(abs(sobra_opcao1), abs(sobra_opcao2), 1)
        max_ganho = max(abs(ganho_hora_opcao1), abs(ganho_hora_opcao2), 1)
        
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
            - **Apuro Bruto:** {apuro:,.2f} €
            - Desconto da Empresa ({opcoes['perc_aluguer']}%): -{desconto_empresa_alugado:,.2f} €
            - Custo do Aluguer: -{custos_fixos_alugado:,.2f} €
            - Combustível: -{desconto_combustivel:,.2f} €
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
            - Combustível: -{desconto_combustivel:,.2f} €
            ---
            - **Sobra Final:** {sobra_opcao2:,.2f} €
            - Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h
            """)

# --- Rodapé ---
st.markdown("---")
st.caption("© 2025 Comparador de Descontos - Desenvolvido para auxiliar na análise financeira de opções de veículo")
