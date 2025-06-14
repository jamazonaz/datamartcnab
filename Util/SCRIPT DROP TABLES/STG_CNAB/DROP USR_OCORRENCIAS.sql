USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_OCORRENCIAS]    Script Date: 13/06/2025 08:25:01 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_OCORRENCIAS]') AND type in (N'U'))
DROP TABLE [dbo].[USR_OCORRENCIAS]
GO

