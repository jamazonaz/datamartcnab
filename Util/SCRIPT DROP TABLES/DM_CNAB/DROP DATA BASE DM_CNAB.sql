USE master;
GO

ALTER DATABASE DM_CNAB 
SET SINGLE_USER 
WITH ROLLBACK IMMEDIATE;
GO

DROP DATABASE DM_CNAB;
GO
