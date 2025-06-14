USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET_BANCOS_C]    Script Date: 12/06/2025 18:17:55 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[USR_CRRET_BANCOS_C](
	[ID_ARQUIVO] [int] NULL,
	[NOME_ARQUIVO] [varchar](200) NULL,
	[ID_BANCO] [int] NULL,
	[DT_GERACAO] [datetime] NULL,
	[COD_BANCO] [varchar](3) NULL,
	[BANCO] [varchar](100) NULL,
	[NUM_RETORNO] [varchar](10) NULL
) ON [PRIMARY]
GO

