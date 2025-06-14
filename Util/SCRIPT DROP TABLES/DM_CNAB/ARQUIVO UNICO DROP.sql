--1
USE [DM_CNAB]
GO
/****** Object:  Table [dbo].[FACTCNAB]    Script Date: 12/06/2025 18:27:06 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[FACTCNAB]') AND type in (N'U'))
DROP TABLE [dbo].[FACTCNAB];
GO
/****** Object:  Table [dbo].[DIMTEMPO]    Script Date: 12/06/2025 18:26:29 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMTEMPO]') AND type in (N'U'))
DROP TABLE [dbo].[DIMTEMPO];
GO
/****** Object:  Table [dbo].[DIMTARIFASCONTRATO]    Script Date: 12/06/2025 18:26:10 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMTARIFASCONTRATO]') AND type in (N'U'))
DROP TABLE [dbo].[DIMTARIFASCONTRATO];
GO
/****** Object:  Table [dbo].[DIMOCORRENCIAS]    Script Date: 12/06/2025 18:25:51 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMOCORRENCIAS]') AND type in (N'U'))
DROP TABLE [dbo].[DIMOCORRENCIAS];
GO
/****** Object:  Table [dbo].[DIMBANCOS]    Script Date: 12/06/2025 18:25:33 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMBANCOS]') AND type in (N'U'))
DROP TABLE [dbo].[DIMBANCOS];
GO
/****** Object:  Table [dbo].[DIMTITULOS]    Script Date: 12/06/2025 18:26:44 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMTITULOS]') AND type in (N'U'))
DROP TABLE [dbo].[DIMTITULOS];
GO
/****** Object:  Table [dbo].[DIMARQUIVO]    Script Date: 12/06/2025 18:25:20 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMARQUIVO]') AND type in (N'U'))
DROP TABLE [dbo].[DIMARQUIVO];
GO



