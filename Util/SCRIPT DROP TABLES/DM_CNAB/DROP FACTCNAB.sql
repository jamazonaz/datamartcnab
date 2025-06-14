USE [DM_CNAB]
GO

/****** Object:  Table [dbo].[FACTCNAB]    Script Date: 12/06/2025 18:27:06 ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[FACTCNAB]') AND type in (N'U'))
DROP TABLE [dbo].[FACTCNAB]
GO

