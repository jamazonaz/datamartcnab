import streamlit as st
import pandas as pd
import pyodbc
import altair as alt
from datetime import datetime

# Conexão com o SQL Server
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=DM_CNAB;"
        "UID=SEU_USUARIO;"
        "PWD=SUA_SENHA"
    )

# Carregar filtros dinâmicos
def get_filtros():
    conn = get_connection()
    bancos = pd.read_sql("SELECT DISTINCT ID_BANCO, NOME_BANCO FROM DIMBANCOS", conn)
    ocorrencias = pd.read_sql("SELECT DISTINCT COD_OCORRENCIA, DESC_OCORRENCIA FROM DIMOCORRENCIAS", conn)
    conn.close()
    return bancos, ocorrencias

# Cabeçalho e configurações
st.set_page_config(layout="wide")
st.title("📊 Painel de Auditoria Financeira - CNAB 400")

# Sidebar: Filtros
# Sidebar: Filtros
st.sidebar.header("🔍 Filtros")

# Carrega bancos
conn = get_connection()
bancos = pd.read_sql("SELECT DISTINCT ID_BANCO, NOME_BANCO FROM DIMBANCOS", conn)

# Seleciona banco
banco_nome = st.sidebar.selectbox("Banco", ["Todos"] + bancos["NOME_BANCO"].tolist())
id_banco = None
if banco_nome != "Todos":
    id_banco = int(bancos[bancos["NOME_BANCO"] == banco_nome]["ID_BANCO"].values[0])

# Filtra ocorrências com base no banco selecionado
if id_banco:
    ocorrencias = pd.read_sql(
        "SELECT DISTINCT O.COD_OCORRENCIA, O.DESC_OCORRENCIA "
        "FROM DIMOCORRENCIAS O WHERE O.ID_BANCO = ?", conn, params=[id_banco]
    )
else:
    ocorrencias = pd.read_sql("SELECT DISTINCT COD_OCORRENCIA, DESC_OCORRENCIA FROM DIMOCORRENCIAS", conn)
conn.close()

# Seleciona ocorrência
ocorrencia_nome = st.sidebar.selectbox("Ocorrência", ["Todas"] + ocorrencias["DESC_OCORRENCIA"].tolist())
cod_ocorrencia = None
if ocorrencia_nome != "Todas":
    cod_ocorrencia = ocorrencias[ocorrencias["DESC_OCORRENCIA"] == ocorrencia_nome]["COD_OCORRENCIA"].values[0]

# Outros filtros
data_inicio = st.sidebar.date_input("Data Início", datetime(2024, 1, 1))
data_fim = st.sidebar.date_input("Data Fim", datetime.today())
semestre = st.sidebar.selectbox("Semestre", ["Todos", 1, 2])
ano = st.sidebar.selectbox("Ano", ["Todos"] + list(range(2020, datetime.today().year + 1)))

# Informativo dos filtros aplicados
st.markdown(f"📅 Período: **{data_inicio.strftime('%d/%m/%Y')}** até **{data_fim.strftime('%d/%m/%Y')}**")
if banco_nome != "Todos":
    st.markdown(f"🏦 Banco Selecionado: **{banco_nome}**")
if ocorrencia_nome != "Todas":
    st.markdown(f"📌 Ocorrência: **{ocorrencia_nome}**")

# Abas para os 4 painéis principais
aba1, aba2, aba3, aba4 = st.tabs([
    "🔎 Auditoria de Tarifas",
    "📆 DMR - Dias Médios de Recebimento",
    "📉 Taxa de Inadimplência",
    "✅ Índice de Pontualidade"
])

# Cada aba será preenchida com gráficos e tabelas nas próximas etapas
with aba1:
    st.subheader("🔎 Auditoria de Tarifas")

    # Monta filtros adicionais
    filtros_where = "WHERE F.VL_TARIFA IS NOT NULL AND T.DATA BETWEEN ? AND ?"
    params = [data_inicio, data_fim]

    if id_banco:
        filtros_where += " AND F.ID_BANCO = ?"
        params.append(id_banco)

    if cod_ocorrencia:
        filtros_where += " AND O.COD_OCORRENCIA = ?"
        params.append(cod_ocorrencia)

    if semestre != "Todos":
        filtros_where += f" AND T.SEMESTRE = {semestre}"
    if ano != "Todos":
        filtros_where += f" AND T.ANO = {ano}"

    # Consulta resumida por categoria
    query_categoria = f"""
    SELECT
        CASE 
            WHEN F.VL_TARIFA > TC.VL_TARIFA_CONTRATO AND F.VL_PAGO > TC.VL_TARIFA_CONTRATO THEN 'Pago > Tarifa Contrato'
            WHEN F.VL_TARIFA > 0 THEN 'Tarifa Aplicada'
            ELSE 'Outros'
        END AS CATEGORIA,
        COUNT(*) AS QTDE_TITULOS
    FROM FACTCNAB F
    JOIN DIMTARIFASCONTRATO TC ON F.ID_CONTRATO = TC.ID_CONTRATO
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where}
    GROUP BY 
        CASE 
            WHEN F.VL_TARIFA > TC.VL_TARIFA_CONTRATO AND F.VL_PAGO > TC.VL_TARIFA_CONTRATO THEN 'Pago > Tarifa Contrato'
            WHEN F.VL_TARIFA > 0 THEN 'Tarifa Aplicada'
            ELSE 'Outros'
        END
    """

    conn = get_connection()
    df_cat = pd.read_sql(query_categoria, conn, params=params)

    st.altair_chart(
        alt.Chart(df_cat).mark_bar().encode(
            x=alt.X("CATEGORIA:N", title="Categoria"),
            y=alt.Y("QTDE_TITULOS:Q", title="Quantidade de Títulos"),
            color="CATEGORIA:N",
            tooltip=["CATEGORIA", "QTDE_TITULOS"]
        ).properties(
            width=600,
            height=400,
            title="Títulos com Tarifa Acima do Contrato"
        ),
        use_container_width=True
    )

    # Consulta detalhada
    query_detalhe = f"""
    SELECT 
        F.ID_DUPLICATA,
        D.DUPLICATA,
        F.VL_TARIFA,
        TC.VL_TARIFA_CONTRATO,
        (F.VL_TARIFA - TC.VL_TARIFA_CONTRATO) AS EXCESSO_TARIFA,
        B.NOME_BANCO,
        T.DATA AS DATA_CREDITO
    FROM FACTCNAB F
    JOIN DIMTARIFASCONTRATO TC ON F.ID_CONTRATO = TC.ID_CONTRATO
    JOIN DIMTITULOS D ON F.ID_DUPLICATA = D.ID_DUPLICATA
    JOIN DIMBANCOS B ON F.ID_BANCO = B.ID_BANCO
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where}
    AND F.VL_TARIFA > TC.VL_TARIFA_CONTRATO
    ORDER BY EXCESSO_TARIFA DESC
    """

    df_det = pd.read_sql(query_detalhe, conn, params=params)
    conn.close()

    st.markdown("#### 📋 Detalhamento de Títulos com Tarifa Acima do Contrato")
    st.dataframe(df_det, use_container_width=True)


    # Gráfico adicional: Evolução mensal do excesso de tarifa cobrada
    query_evolucao = f"""
    SELECT 
        T.ANO,
        T.MES,
        FORMAT(T.DATA, 'MM/yyyy') AS MES_ANO,
        SUM(F.VL_TARIFA - TC.VL_TARIFA_CONTRATO) AS TOTAL_EXCESSO
    FROM FACTCNAB F
    JOIN DIMTARIFASCONTRATO TC ON F.ID_CONTRATO = TC.ID_CONTRATO
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where}
    AND F.VL_TARIFA > TC.VL_TARIFA_CONTRATO
    GROUP BY T.ANO, T.MES, FORMAT(T.DATA, 'MM/yyyy')
    ORDER BY T.ANO, T.MES
    """

    conn = get_connection()
    df_evolucao = pd.read_sql(query_evolucao, conn, params=params)
    conn.close()

    # Indicador: total geral do excesso
    total_excesso = df_evolucao["TOTAL_EXCESSO"].sum() if not df_evolucao.empty else 0

    st.markdown("#### 💰 Valor Total de Tarifas Cobradas a Mais no Período")
    st.metric(label="💸 Excesso Cobrado", value=f"R$ {total_excesso:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.markdown("#### 📈 Evolução Mensal do Excesso de Tarifas Cobradas")
    if not df_evolucao.empty:
        chart_evolucao = alt.Chart(df_evolucao).mark_line(point=True).encode(
            x=alt.X("MES_ANO:N", title="Mês/Ano", sort=None),
            y=alt.Y("TOTAL_EXCESSO:Q", title="Valor Total de Excesso (R$)"),
            tooltip=["MES_ANO", "TOTAL_EXCESSO"]
        ).properties(
            width=700,
            height=400
        )
        st.altair_chart(chart_evolucao, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para esse filtro.")

with aba2:
    st.subheader("📆 DMR – Dias Médios de Recebimento")

    # Filtros SQL
    filtros_where_dmr = "WHERE F.VL_PAGO > 0 AND C.DATA IS NOT NULL AND V.DATA IS NOT NULL AND C.DATA BETWEEN ? AND ?"
    params_dmr = [data_inicio, data_fim]

    if id_banco is not None:
        filtros_where_dmr += " AND F.ID_BANCO = ?"
        params_dmr.append(id_banco)

    if cod_ocorrencia is not None:
        filtros_where_dmr += " AND O.COD_OCORRENCIA = ?"
        params_dmr.append(cod_ocorrencia)

    if semestre != "Todos":
        filtros_where_dmr += f" AND T.SEMESTRE = {semestre}"
    if ano != "Todos":
        filtros_where_dmr += f" AND T.ANO = {ano}"

    # 📌 Consulta: tipos de pagamento
    query_tipo_pagamento = f"""
    SELECT
        CASE
            WHEN C.DATA < V.DATA THEN 'Adiantado'
            WHEN C.DATA = V.DATA THEN 'No Prazo'
            WHEN C.DATA > V.DATA THEN 'Atrasado'
            ELSE 'Indefinido'
        END AS TIPO_PAGAMENTO,
        COUNT(*) AS QTDE
    FROM FACTCNAB F
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO C ON F.DT_CREDITO = C.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_dmr}
    GROUP BY
        CASE
            WHEN C.DATA < V.DATA THEN 'Adiantado'
            WHEN C.DATA = V.DATA THEN 'No Prazo'
            WHEN C.DATA > V.DATA THEN 'Atrasado'
            ELSE 'Indefinido'
        END
    """

    conn = get_connection()
    df_tp = pd.read_sql(query_tipo_pagamento, conn, params=params_dmr)

    # 📈 Consulta: evolução do DMR
    query_dmr = f"""
    SELECT 
        B.NOME_BANCO,
        T.ANO,
        T.MES,
        FORMAT(C.DATA, 'MM/yyyy') AS MES_ANO,
        AVG(DATEDIFF(DAY, V.DATA, C.DATA)) AS DMR
    FROM FACTCNAB F
    JOIN DIMBANCOS B ON F.ID_BANCO = B.ID_BANCO
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO C ON F.DT_CREDITO = C.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_dmr}
    GROUP BY B.NOME_BANCO, T.ANO, T.MES, FORMAT(C.DATA, 'MM/yyyy')
    ORDER BY T.ANO, T.MES
    """
    df_dmr = pd.read_sql(query_dmr, conn, params=params_dmr)
    conn.close()

    # ✅ KPIs: cálculo com df_tp agora existente
    media_dmr = round(df_dmr["DMR"].mean(), 2) if not df_dmr.empty else 0

    df_tp_dict = df_tp.set_index("TIPO_PAGAMENTO")["QTDE"].to_dict()
    qtde_total = sum(df_tp_dict.values())

    qtde_adiantado = df_tp_dict.get("Adiantado", 0)
    qtde_no_prazo = df_tp_dict.get("No Prazo", 0)
    qtde_atrasado = df_tp_dict.get("Atrasado", 0)

    perc_adiantado = (qtde_adiantado / qtde_total * 100) if qtde_total > 0 else 0
    perc_no_prazo = (qtde_no_prazo / qtde_total * 100) if qtde_total > 0 else 0
    perc_atrasado = (qtde_atrasado / qtde_total * 100) if qtde_total > 0 else 0

    st.markdown("#### 📊 Indicadores de Recebimento")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Dias Médios (DMR)", f"{media_dmr:.2f} dias")
    col2.metric("⏩ Adiantado", f"{perc_adiantado:.1f}%", delta=f"{qtde_adiantado} títulos")
    col3.metric("📆 No Prazo", f"{perc_no_prazo:.1f}%", delta=f"{qtde_no_prazo} títulos")
    col4.metric("⏳ Atrasado", f"{perc_atrasado:.1f}%", delta=f"{qtde_atrasado} títulos")

    # 🎯 Gráfico Classificação
    st.markdown("#### 📊 Classificação dos Pagamentos por Tipo")
    if not df_tp.empty:
        chart_tp = alt.Chart(df_tp).mark_bar().encode(
            x=alt.X("TIPO_PAGAMENTO:N", title="Tipo de Pagamento"),
            y=alt.Y("QTDE:Q", title="Quantidade de Títulos"),
            color=alt.Color("TIPO_PAGAMENTO:N", scale=alt.Scale(
                domain=["Adiantado", "No Prazo", "Atrasado"],
                range=["#2ca02c", "#1f77b4", "#d62728"]
            )),
            tooltip=["TIPO_PAGAMENTO", "QTDE"]
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart_tp, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para a classificação dos pagamentos.")

    # 📈 Gráfico de DMR
    st.markdown("#### 📈 Evolução Mensal do DMR")
    if not df_dmr.empty:
        chart_dmr = alt.Chart(df_dmr).mark_line(point=True).encode(
            x=alt.X("MES_ANO:N", title="Mês/Ano", sort=None),
            y=alt.Y("DMR:Q", title="Dias Médios"),
            color="NOME_BANCO:N",
            tooltip=["NOME_BANCO", "MES_ANO", "DMR"]
        ).properties(
            width=800,
            height=400
        )
        st.altair_chart(chart_dmr, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros aplicados.")
    
    # 📊 Gráfico de evolução mensal do tipo de pagamento (empilhado)
    query_evolucao_tipo = f"""
    SELECT 
        FORMAT(C.DATA, 'MM/yyyy') AS MES_ANO,
        CASE
            WHEN C.DATA < V.DATA THEN 'Adiantado'
            WHEN C.DATA = V.DATA THEN 'No Prazo'
            WHEN C.DATA > V.DATA THEN 'Atrasado'
            ELSE 'Indefinido'
        END AS TIPO_PAGAMENTO,
        COUNT(*) AS QTDE
    FROM FACTCNAB F
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO C ON F.DT_CREDITO = C.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_dmr}
    GROUP BY FORMAT(C.DATA, 'MM/yyyy'),
        CASE
            WHEN C.DATA < V.DATA THEN 'Adiantado'
            WHEN C.DATA = V.DATA THEN 'No Prazo'
            WHEN C.DATA > V.DATA THEN 'Atrasado'
            ELSE 'Indefinido'
        END
    ORDER BY MES_ANO
    """

    conn = get_connection()
    df_evolucao_tipo = pd.read_sql(query_evolucao_tipo, conn, params=params_dmr)
    conn.close()

    st.markdown("#### 📊 Evolução Mensal do Tipo de Pagamento")
    if not df_evolucao_tipo.empty:
        chart_evo_tp = alt.Chart(df_evolucao_tipo).mark_bar().encode(
            x=alt.X("MES_ANO:N", title="Mês/Ano", sort=None),
            y=alt.Y("QTDE:Q", title="Qtd. de Títulos"),
            color=alt.Color("TIPO_PAGAMENTO:N", scale=alt.Scale(
                domain=["Adiantado", "No Prazo", "Atrasado"],
                range=["#2ca02c", "#1f77b4", "#d62728"]
            )),
            tooltip=["MES_ANO", "TIPO_PAGAMENTO", "QTDE"]
        ).properties(
            width=800,
            height=400
        )
        st.altair_chart(chart_evo_tp, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para evolução do tipo de pagamento.")

    # 📊 Distribuição dos dias de atraso em faixas
    query_atraso_faixa = f"""
    SELECT
        CASE
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) = 0 THEN 'No Vencimento'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) BETWEEN 1 AND 3 THEN '1-3 dias'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) BETWEEN 4 AND 7 THEN '4-7 dias'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) BETWEEN 8 AND 15 THEN '8-15 dias'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) > 15 THEN '+15 dias'
            ELSE 'Adiantado'
        END AS FAIXA_ATRASO,
        COUNT(*) AS QTDE
    FROM FACTCNAB F
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO C ON F.DT_CREDITO = C.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_dmr}
    AND C.DATA >= V.DATA  -- Considera apenas pagamentos iguais ou após vencimento
    GROUP BY
        CASE
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) = 0 THEN 'No Vencimento'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) BETWEEN 1 AND 3 THEN '1-3 dias'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) BETWEEN 4 AND 7 THEN '4-7 dias'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) BETWEEN 8 AND 15 THEN '8-15 dias'
            WHEN DATEDIFF(DAY, V.DATA, C.DATA) > 15 THEN '+15 dias'
            ELSE 'Adiantado'
        END
    ORDER BY FAIXA_ATRASO
    """

    conn = get_connection()
    df_faixas = pd.read_sql(query_atraso_faixa, conn, params=params_dmr)
    conn.close()

    st.markdown("#### 📊 Distribuição dos Dias de Atraso")
    if not df_faixas.empty:
        chart_faixa = alt.Chart(df_faixas).mark_bar().encode(
            x=alt.X("FAIXA_ATRASO:N", title="Faixa de Atraso"),
            y=alt.Y("QTDE:Q", title="Quantidade de Títulos"),
            color=alt.Color("FAIXA_ATRASO:N", legend=None),
            tooltip=["FAIXA_ATRASO", "QTDE"]
        ).properties(
            width=700,
            height=400
        )
        st.altair_chart(chart_faixa, use_container_width=True)
    else:
        st.warning("Nenhum dado de atraso encontrado para os filtros aplicados.")


    # 📋 Tabela de títulos com maior DMR
    query_titulos_criticos = f"""
    SELECT TOP 20
        D.DUPLICATA,
        B.NOME_BANCO,
        V.DATA AS DATA_VENCIMENTO,
        C.DATA AS DATA_CREDITO,
        DATEDIFF(DAY, V.DATA, C.DATA) AS DMR
    FROM FACTCNAB F
    JOIN DIMTITULOS D ON F.ID_DUPLICATA = D.ID_DUPLICATA
    JOIN DIMBANCOS B ON F.ID_BANCO = B.ID_BANCO
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO C ON F.DT_CREDITO = C.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_dmr}
    AND F.VL_PAGO > 0
    AND C.DATA > V.DATA
    ORDER BY DMR DESC
    """

    conn = get_connection()
    df_criticos = pd.read_sql(query_titulos_criticos, conn, params=params_dmr)
    conn.close()

    st.markdown("#### 🧾 Títulos com Maior Atraso (Top 20 DMR)")
    if not df_criticos.empty:
        st.dataframe(df_criticos, use_container_width=True)
    else:
        st.warning("Nenhum título com atraso encontrado para os filtros aplicados.")


with aba3:
    st.subheader("📉 Taxa de Inadimplência")

    # Filtros SQL
    filtros_where_inad = "WHERE T.DATA <= ? AND V.DATA <= ?"
    params_inad = [data_fim, data_fim]  # Apenas vencidos até a data fim

    if id_banco is not None:
        filtros_where_inad += " AND F.ID_BANCO = ?"
        params_inad.append(id_banco)

    if cod_ocorrencia is not None:
        filtros_where_inad += " AND O.COD_OCORRENCIA = ?"
        params_inad.append(cod_ocorrencia)

    if semestre != "Todos":
        filtros_where_inad += f" AND T.SEMESTRE = {semestre}"
    if ano != "Todos":
        filtros_where_inad += f" AND T.ANO = {ano}"

    # Consulta inadimplência por mês
    query_inad = f"""
    SELECT 
        T.ANO,
        T.MES,
        FORMAT(T.DATA, 'MM/yyyy') AS MES_ANO,
        B.NOME_BANCO,
        COUNT(*) AS TOTAL_TITULOS,
        COUNT(CASE WHEN F.VL_PAGO = 0 THEN 1 END) AS TITULOS_INADIMPLENTES,
        (COUNT(CASE WHEN F.VL_PAGO = 0 THEN 1 END) * 1.0 / COUNT(*)) * 100 AS TAXA_INADIMPLENCIA
    FROM FACTCNAB F
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMBANCOS B ON F.ID_BANCO = B.ID_BANCO
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_inad}
    GROUP BY T.ANO, T.MES, FORMAT(T.DATA, 'MM/yyyy'), B.NOME_BANCO
    ORDER BY T.ANO, T.MES
    """

    conn = get_connection()
    df_inad = pd.read_sql(query_inad, conn, params=params_inad)
    conn.close()

    # KPI: inadimplência média
    inad_media = round(df_inad["TAXA_INADIMPLENCIA"].mean(), 2) if not df_inad.empty else 0

    st.markdown("#### 📌 Taxa Média de Inadimplência no Período")
    st.metric(label="❗ Inadimplência", value=f"{inad_media:.2f} %")

    # Gráfico de linha: inadimplência mensal
    st.markdown("#### 📈 Evolução Mensal da Inadimplência")
    if not df_inad.empty:
        chart_inad = alt.Chart(df_inad).mark_line(point=True).encode(
            x=alt.X("MES_ANO:N", title="Mês/Ano", sort=None),
            y=alt.Y("TAXA_INADIMPLENCIA:Q", title="Inadimplência (%)"),
            color="NOME_BANCO:N",
            tooltip=["NOME_BANCO", "MES_ANO", "TAXA_INADIMPLENCIA"]
        ).properties(
            width=800,
            height=400
        )
        st.altair_chart(chart_inad, use_container_width=True)
    else:
        st.warning("Nenhum dado de inadimplência encontrado para os filtros aplicados.")

    # Tabela detalhada
    st.markdown("#### 📋 Detalhamento por Banco e Mês")
    if not df_inad.empty:
        st.dataframe(df_inad, use_container_width=True)
    else:
        st.info("Não há registros de inadimplência para os critérios selecionados.")

    # 📋 Tabela de títulos inadimplentes (VL_PAGO = 0)
    query_titulos_inad = f"""
    SELECT 
        D.DUPLICATA,
        B.NOME_BANCO,
        V.DATA AS DATA_VENCIMENTO,
        F.VL_TITULO,
        O.DESC_OCORRENCIA
    FROM FACTCNAB F
    JOIN DIMTITULOS D ON F.ID_DUPLICATA = D.ID_DUPLICATA
    JOIN DIMBANCOS B ON F.ID_BANCO = B.ID_BANCO
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_inad}
    AND F.VL_PAGO = 0
    ORDER BY V.DATA
    """

    conn = get_connection()
    df_titulos_inad = pd.read_sql(query_titulos_inad, conn, params=params_inad)
    conn.close()

    st.markdown("#### 📋 Títulos Inadimplentes no Período")
    if not df_titulos_inad.empty:
        st.dataframe(df_titulos_inad, use_container_width=True)
    else:
        st.info("Nenhum título inadimplente encontrado para os critérios selecionados.")

    # 📊 Classificação por tempo de inadimplência (faixas)
    query_faixas_inad = f"""
    SELECT 
        CASE
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) BETWEEN 1 AND 7 THEN '1-7 dias'
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) BETWEEN 8 AND 30 THEN '8-30 dias'
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) BETWEEN 31 AND 60 THEN '31-60 dias'
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) > 60 THEN '+60 dias'
            ELSE 'Vencimento futuro ou quitado'
        END AS FAIXA_ATRASO,
        COUNT(*) AS QTDE
    FROM FACTCNAB F
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_inad}
    AND F.VL_PAGO = 0
    AND T.DATA > V.DATA
    GROUP BY 
        CASE
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) BETWEEN 1 AND 7 THEN '1-7 dias'
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) BETWEEN 8 AND 30 THEN '8-30 dias'
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) BETWEEN 31 AND 60 THEN '31-60 dias'
            WHEN DATEDIFF(DAY, V.DATA, T.DATA) > 60 THEN '+60 dias'
            ELSE 'Vencimento futuro ou quitado'
        END
    ORDER BY FAIXA_ATRASO
    """

    conn = get_connection()
    df_faixas_inad = pd.read_sql(query_faixas_inad, conn, params=params_inad)
    conn.close()

    st.markdown("#### 📊 Classificação da Inadimplência por Faixa de Dias")
    if not df_faixas_inad.empty:
        chart_faixa_inad = alt.Chart(df_faixas_inad).mark_bar().encode(
            x=alt.X("FAIXA_ATRASO:N", title="Faixa de Atraso"),
            y=alt.Y("QTDE:Q", title="Quantidade de Títulos"),
            color=alt.Color("FAIXA_ATRASO:N", legend=None),
            tooltip=["FAIXA_ATRASO", "QTDE"]
        ).properties(
            width=700,
            height=400
        )
        st.altair_chart(chart_faixa_inad, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para faixas de inadimplência.")


with aba4:
    st.subheader("✅ Índice de Pontualidade")

    # Filtros SQL
    filtros_where_pontual = "WHERE F.VL_PAGO > 0 AND C.DATA IS NOT NULL AND V.DATA IS NOT NULL AND C.DATA BETWEEN ? AND ?"
    params_pontual = [data_inicio, data_fim]

    if id_banco is not None:
        filtros_where_pontual += " AND F.ID_BANCO = ?"
        params_pontual.append(id_banco)

    if cod_ocorrencia is not None:
        filtros_where_pontual += " AND O.COD_OCORRENCIA = ?"
        params_pontual.append(cod_ocorrencia)

    if semestre != "Todos":
        filtros_where_pontual += f" AND T.SEMESTRE = {semestre}"
    if ano != "Todos":
        filtros_where_pontual += f" AND T.ANO = {ano}"

    # Consulta índice de pontualidade
    query_pontual = f"""
    SELECT 
        T.ANO,
        T.MES,
        FORMAT(C.DATA, 'MM/yyyy') AS MES_ANO,
        B.NOME_BANCO,
        COUNT(*) AS TOTAL_PAGOS,
        COUNT(CASE WHEN C.DATA <= V.DATA THEN 1 END) AS PAGOS_PONTUAIS,
        (COUNT(CASE WHEN C.DATA <= V.DATA THEN 1 END) * 1.0 / COUNT(*)) * 100 AS INDICE_PONTUALIDADE
    FROM FACTCNAB F
    JOIN DIMBANCOS B ON F.ID_BANCO = B.ID_BANCO
    JOIN DIMTEMPO V ON F.DT_VENCIMENTO = V.IDDATA
    JOIN DIMTEMPO C ON F.DT_CREDITO = C.IDDATA
    JOIN DIMTEMPO T ON F.DT_CREDITO = T.IDDATA
    JOIN DIMOCORRENCIAS O ON F.ID_OCORRENCIA = O.ID_OCORRENCIA
    {filtros_where_pontual}
    GROUP BY T.ANO, T.MES, FORMAT(C.DATA, 'MM/yyyy'), B.NOME_BANCO
    ORDER BY T.ANO, T.MES
    """

    conn = get_connection()
    df_pontual = pd.read_sql(query_pontual, conn, params=params_pontual)
    conn.close()

    # KPI: média de pontualidade
    media_pontual = round(df_pontual["INDICE_PONTUALIDADE"].mean(), 2) if not df_pontual.empty else 0

    st.markdown("#### 📌 Índice Médio de Pontualidade no Período")
    st.metric(label="✅ Pontualidade", value=f"{media_pontual:.2f} %")

    # Gráfico de linha
    st.markdown("#### 📈 Evolução Mensal da Pontualidade")
    if not df_pontual.empty:
        chart_pontual = alt.Chart(df_pontual).mark_line(point=True).encode(
            x=alt.X("MES_ANO:N", title="Mês/Ano", sort=None),
            y=alt.Y("INDICE_PONTUALIDADE:Q", title="Pontualidade (%)"),
            color="NOME_BANCO:N",
            tooltip=["NOME_BANCO", "MES_ANO", "INDICE_PONTUALIDADE"]
        ).properties(
            width=800,
            height=400
        )
        st.altair_chart(chart_pontual, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros aplicados.")

    # Tabela detalhada
    st.markdown("#### 📋 Detalhamento por Banco e Mês")
    if not df_pontual.empty:
        st.dataframe(df_pontual, use_container_width=True)
    else:
        st.info("Não há registros para pontualidade com os critérios aplicados.")

