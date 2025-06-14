--limpar a base de dados DM_CNAB
USE DM_CNAB;
GO

delete from FACTCNAB;

delete from DIMTEMPO;

delete from DIMTARIFASCONTRATO;

delete from DIMOCORRENCIAS;

delete from DIMARQUIVO;

delete from DIMBANCOS;

delete from DIMTITULOS;



--CONSULTA BASE DE DADOS
select * from DIMARQUIVO;

select * from DIMBANCOS;

select * from DIMOCORRENCIAS;

select * from DIMTARIFASCONTRATO;

select * from DIMTEMPO;

select * from DIMTITULOS;

select * from FACTCNAB;




