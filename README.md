# ANALISE DE RETORNO CNAB PARA MONITORAMENTO DE BOLETOS E AUDITORIA DE RECEBIMENTO

---

## 🧱 Modelagem Dimensional (Star Schema)

- **Fato Principal:** `FACTCNAB`
- **Dimensões:**
  - `DIMBANCOS` – dados do banco
  - `DIMTEMPO` – datas normalizadas
  - `DIMOCORRENCIAS` – códigos e descrições de eventos CNAB
  - `DIMTITULOS` – informações dos boletos (duplicatas)
  - `DIMTARIFASCONTRATO` – valores contratados por banco

---

## 📊 Indicadores Desenvolvidos

| Indicador               | Descrição                                               |
|-------------------------|----------------------------------------------------------|
| Auditoria de Tarifas    | Compara tarifas cobradas com valores contratados        |
| DMR                     | Dias Médios entre vencimento e pagamento                 |
| Inadimplência           | % de títulos vencidos e não pagos                       |
| Pontualidade            | % de títulos pagos até ou antes do vencimento           |
| Classificações          | Agrupamento de pagamentos: Adiantado, No Prazo, Atrasado|

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- Streamlit
- Pandas
- Altair
- PyODBC
- SQL Server

---

## 📦 Como Executar Localmente

```bash
1 - python -m venv v_data_mart
2 - ./v_data_mart/script/activate
3 - pip install -r requirements.txt
4 - streamlit run app.py
