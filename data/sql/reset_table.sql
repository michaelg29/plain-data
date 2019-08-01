delete from dbo.Users where ID >= 0
DBCC CHECKIDENT ('dbo.Users', RESEED, -1);
select * from dbo.Users