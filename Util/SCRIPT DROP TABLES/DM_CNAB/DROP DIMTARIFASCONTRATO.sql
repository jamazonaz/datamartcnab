USE [DM_CNAB]
GO

/****** Object:  Table [dbo].[DIMTARIFASCONTRATO]    Script Date: 12/06/2025 18:26:10 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMTARIFASCONTRATO]') AND type in (N'U'))
DROP TABLE [dbo].[DIMTARIFASCONTRATO]
GO

