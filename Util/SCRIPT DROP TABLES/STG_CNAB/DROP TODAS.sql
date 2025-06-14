USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET]    Script Date: 13/06/2025 08:23:56 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_CRRET]') AND type in (N'U'))
DROP TABLE [dbo].[USR_CRRET]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET_BANCOS]    Script Date: 13/06/2025 08:24:17 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_CRRET_BANCOS]') AND type in (N'U'))
DROP TABLE [dbo].[USR_CRRET_BANCOS]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET_BANCOS_C]    Script Date: 13/06/2025 08:24:30 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_CRRET_BANCOS_C]') AND type in (N'U'))
DROP TABLE [dbo].[USR_CRRET_BANCOS_C]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_CRRET_BANCOS_L]    Script Date: 13/06/2025 08:24:41 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_CRRET_BANCOS_L]') AND type in (N'U'))
DROP TABLE [dbo].[USR_CRRET_BANCOS_L]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_OCORRENCIAS]    Script Date: 13/06/2025 08:25:01 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_OCORRENCIAS]') AND type in (N'U'))
DROP TABLE [dbo].[USR_OCORRENCIAS]
GO

USE [STG_CNAB]
GO

/****** Object:  Table [dbo].[USR_TARIFAS_CONTRATO]    Script Date: 13/06/2025 08:25:37 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USR_TARIFAS_CONTRATO]') AND type in (N'U'))
DROP TABLE [dbo].[USR_TARIFAS_CONTRATO]
GO

