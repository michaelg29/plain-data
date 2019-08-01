create table dbo.Users (
	ID int NOT NULL PRIMARY KEY IDENTITY(0, 1),
	LastName varchar(255) NOT NULL,
	FirstName varchar(255) NOT NULL,
	Username varchar(255) NOT NULL,
	Password varchar(255) NOT NULL,
	Email varchar(255) NOT NULL,
	Flags varchar(255) NOT NULL
);

select * from dbo.Users