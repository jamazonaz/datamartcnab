USE [DM_CNAB]
GO

/****** Object:  Table [dbo].[DIMTEMPO]    Script Date: 12/06/2025 18:26:29 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMTEMPO]') AND type in (N'U'))
DROP TABLE [dbo].[DIMTEMPO]
GO

