USE [DM_CNAB]
GO

/****** Object:  Table [dbo].[DIMBANCOS]    Script Date: 12/06/2025 18:25:33 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMBANCOS]') AND type in (N'U'))
DROP TABLE [dbo].[DIMBANCOS]
GO

