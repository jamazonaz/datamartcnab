USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET_BANCOS_L]    Script Date: 12/06/2025 18:18:09 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[USR_CRRET_BANCOS_L](
	[ID] [int] NULL,
	[ARQUIVO] [varchar](200) NULL,
	[BANCO] [int] NULL,
	[COD_OCORRENCIA] [varchar](2) NULL,
	[DESC_OCORRENCIA] [varchar](200) NULL,
	[DT_CREDITO] [datetime] NULL,
	[DT_GERACAO] [datetime] NULL,
	[DT_INCLUIUI] [datetime] NULL,
	[DT_OCORRENCIA] [datetime] NULL,
	[DT_VENCIMENTO] [datetime] NULL,
	[ID_DATA] [int] NULL,
	[JUROS_MORA] [float] NULL,
	[LANCAMENTO] [int] NULL,
	[N_DOCUMENTO] [varchar](50) NULL,
	[NOME_BANCO] [varchar](100) NULL,
	[NOSSO_NUMERO] [varchar](50) NULL,
	[TARIFA_COB] [float] NULL,
	[VL_PAGO] [float] NULL,
	[VL_TITULO] [float] NULL
) ON [PRIMARY]
GO

