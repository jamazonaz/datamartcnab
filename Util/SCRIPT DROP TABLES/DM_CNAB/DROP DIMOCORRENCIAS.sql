USE [DM_CNAB]
GO

/****** Object:  Table [dbo].[DIMOCORRENCIAS]    Script Date: 12/06/2025 18:25:51 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DIMOCORRENCIAS]') AND type in (N'U'))
DROP TABLE [dbo].[DIMOCORRENCIAS]
GO

