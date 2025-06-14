
--CRIAR NA BASE DE DADOS DM_CNAB
USE DM_CNAB;
GO

CREATE OR ALTER PROCEDURE EXPORTA_STG_DM_CNAB
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRAN -- Transação global, segura

        -- Bloco 1: DIMTEMPO
        DECLARE @DataAtual DATE = '2000-01-01';
        DECLARE @DataFinal DATE = '2030-12-31';
        WHILE @DataAtual <= @DataFinal
        BEGIN
            INSERT INTO DIMTEMPO (
                IDDATA, [DATA], ANO, MES, DIA, SEMESTRE, TRIMESTRE, NOME_MES, NOME_DIA_SEMANA, EH_FINAL_DE_SEMANA
            )
            VALUES (
                CAST(CONVERT(VARCHAR(8), @DataAtual, 112) AS INT),
                @DataAtual,
                YEAR(@DataAtual),
                MONTH(@DataAtual),
                DAY(@DataAtual),
                CASE WHEN MONTH(@DataAtual) <= 6 THEN 1 ELSE 2 END,
                DATEPART(QUARTER, @DataAtual),
                DATENAME(MONTH, @DataAtual),
                DATENAME(WEEKDAY, @DataAtual),
                CASE WHEN DATENAME(WEEKDAY, @DataAtual) IN ('Sábado', 'Domingo') THEN 1 ELSE 0 END
            );
            SET @DataAtual = DATEADD(DAY, 1, @DataAtual);
        END

        -- Bloco 2: DIMBANCOS
        INSERT INTO DIMBANCOS (ID_BANCO, CODIGO_BANCO, NOME_BANCO)
        SELECT ID_BANCO, COD_BANCO, NOME
        FROM STG_CNAB.DBO.USR_CRRET_BANCOS;

        -- Bloco 3: DIMOCORRENCIAS
        INSERT INTO DIMOCORRENCIAS (ID_OCORRENCIA, ID_BANCO, COD_OCORRENCIA, DESC_OCORRENCIA)
        SELECT
            ROW_NUMBER() OVER (ORDER BY BANCO, COD_OCORRENCIA),
            BANCO, 
            COD_OCORRENCIA,
            DESCRICAO
        FROM STG_CNAB.DBO.USR_OCORRENCIAS;

        -- Bloco 4: DIMTARIFASCONTRATO
        INSERT INTO DIMTARIFASCONTRATO (ID_CONTRATO, ID_BANCO, COD_OCORRENCIA, VL_TARIFA_CONTRATO)
        SELECT
            ROW_NUMBER() OVER (ORDER BY UO.BANCO, UO.COD_OCORRENCIA),
            UO.BANCO,
            UO.COD_OCORRENCIA,
            UT.VL_TARIFA
        FROM STG_CNAB.DBO.USR_OCORRENCIAS UO
        INNER JOIN STG_CNAB.DBO.USR_TARIFAS_CONTRATO UT  
            ON UT.BANCO = UO.BANCO AND UT.COD_TARIFA = UO.COD_OCORRENCIA;

        -- Bloco 5: DIMTITULOS
        INSERT INTO DIMTITULOS (ID_DUPLICATA, DUPLICATA, NOSSO_NUMERO)
        SELECT DISTINCT
            LANCAMENTO,
            TRIM(N_DOCUMENTO),
            MAX(RIGHT(REPLICATE('0', 20) + CAST(TRIM(NOSSO_NUMERO) AS VARCHAR(20)), 20))
        FROM STG_CNAB.DBO.USR_CRRET_BANCOS_L
        GROUP BY LANCAMENTO, TRIM(N_DOCUMENTO);

        -- Bloco 6: DIMARQUIVO
        INSERT INTO DIMARQUIVO (ID_ARQUIVO, NOMEARQUIVO, ID_BANCO, CODIGO_BANCO, NOME_BANCO, DTGERACAO, DTINCLUIU)
        SELECT
            c.ID_ARQUIVO,
            c.NOME_ARQUIVO,
            c.ID_BANCO,
            c.COD_BANCO,
            c.BANCO,
            c.DT_GERACAO,
            cr.DTINCLUIU
        FROM STG_CNAB.DBO.USR_CRRET cr
        LEFT JOIN STG_CNAB.DBO.USR_CRRET_BANCOS_C c ON c.ID_ARQUIVO = cr.ID
        WHERE c.ID_ARQUIVO IS NOT NULL;

        -- Bloco 7: FACTCNAB
        ;WITH oco AS (
            SELECT
                ROW_NUMBER() OVER (ORDER BY BANCO, COD_OCORRENCIA) AS ID_OCORRENCIA,
                BANCO,
                COD_OCORRENCIA
            FROM STG_CNAB.DBO.USR_OCORRENCIAS
        )
        INSERT INTO FACTCNAB (
            ID_ARQUIVO, ID_BANCO, DT_GERACAO, DT_OCORRENCIA, DT_CREDITO, DT_VENCIMENTO, 
            ID_DUPLICATA, ID_OCORRENCIA, ID_CONTRATO, VL_TITULO, VL_JUROS_MORA, VL_PAGO, VL_TARIFA, VL_DESCONTO
        )
        SELECT
            l.ID,
            l.BANCO,
            CONVERT(INT, REPLACE(CONVERT(DATE, l.DT_GERACAO), '-', '')),
            CONVERT(INT, REPLACE(CONVERT(DATE, l.DT_OCORRENCIA), '-', '')),
            CONVERT(INT, REPLACE(CONVERT(DATE, l.DT_CREDITO), '-', '')),
            CONVERT(INT, REPLACE(CONVERT(DATE, l.DT_VENCIMENTO), '-', '')),
            l.LANCAMENTO,
            oco.ID_OCORRENCIA,
            oco.ID_OCORRENCIA,
       l.VL_TITULO,
            l.JUROS_MORA,
            l.VL_PAGO,
            l.TARIFA_COB,
            0
        FROM STG_CNAB.DBO.USR_CRRET_BANCOS_L l
        INNER JOIN oco 
            ON oco.BANCO = l.BANCO AND oco.COD_OCORRENCIA = l.COD_OCORRENCIA;

        COMMIT TRAN -- Fecha a única transação
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRAN;

        -- Opcional: registrar erro
        -- PRINT ERROR_MESSAGE();

        THROW; -- Relança o erro
    END CATCH
END