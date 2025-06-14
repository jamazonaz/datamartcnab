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

