USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET]    Script Date: 12/06/2025 18:16:53 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[USR_CRRET](
	[ID] [int] NULL,
	[BANCO] [int] NULL,
	[ARQUIVO] [varchar](200) NULL,
	[DTINCLUIU] [datetime] NULL,
	[EXPORTADO] [varchar](1) NULL
) ON [PRIMARY]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET_BANCOS]    Script Date: 12/06/2025 18:17:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[USR_CRRET_BANCOS](
	[ID_BANCO] [int] NULL,
	[COD_BANCO] [varchar](3) NULL,
	[NOME] [varchar](50) NULL
) ON [PRIMARY]
GO

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

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_OCORRENCIAS]    Script Date: 12/06/2025 18:18:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[USR_OCORRENCIAS](
	[BANCO] [int] NULL,
	[COD_OCORRENCIA] [varchar](2) NULL,
	[DESCRICAO] [varchar](200) NULL
) ON [PRIMARY]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_TARIFAS_CONTRATO]    Script Date: 12/06/2025 18:18:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[USR_TARIFAS_CONTRATO](
	[BANCO] [int] NOT NULL,
	[COD_TARIFA] [varchar](2) NOT NULL,
	[DESC_TARIFA] [varchar](200) NULL,
	[VL_TARIFA] [numeric](22, 6) NOT NULL
) ON [PRIMARY]
GO

