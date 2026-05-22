-- Use the database (this will be handled by Python script)
-- USE Offboarding_user_DB;
-- GO

-- Create table for archived users
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tbl_ArchivedUserDetails' AND xtype='U')
CREATE TABLE tbl_ArchivedUserDetails (
    _id NVARCHAR(100) PRIMARY KEY,
    _rev NVARCHAR(100),
    custom_RegCompanyName NVARCHAR(200),
    frUnindexedString1 NVARCHAR(200),
    frUnindexedString2 NVARCHAR(200),
    frUnindexedString3 NVARCHAR(200),
    frUnindexedString4 NVARCHAR(200),
    frUnindexedString5 NVARCHAR(200),
    frIndexedString11 NVARCHAR(200),
    frIndexedString12 NVARCHAR(200),
    frIndexedString10 NVARCHAR(200),
    frIndexedString19 NVARCHAR(200),
    frIndexedString17 NVARCHAR(200),
    frIndexedString18 NVARCHAR(200),
    frIndexedString15 NVARCHAR(200),
    frIndexedString16 NVARCHAR(200),
    frIndexedString13 NVARCHAR(200),
    frIndexedString14 NVARCHAR(200),
    givenName NVARCHAR(200),
    frIndexedString20 NVARCHAR(200),
    telephoneNumber NVARCHAR(50),
    city NVARCHAR(100),
    displayName NVARCHAR(200),
    accountStatus NVARCHAR(50),
    sn NVARCHAR(200),
    frUnindexedDate1 NVARCHAR(50),
    frIndexedString9 NVARCHAR(200),
    frIndexedString8 NVARCHAR(200),
    frIndexedString7 NVARCHAR(200),
    frIndexedString6 NVARCHAR(200),
    passwordLastChangedTime NVARCHAR(50),
    country NVARCHAR(100),
    mail NVARCHAR(200),
    frIndexedDate5 NVARCHAR(50),
    frIndexedDate4 NVARCHAR(50),
    frIndexedDate3 NVARCHAR(50),
    frIndexedString5 NVARCHAR(200),
    frIndexedString4 NVARCHAR(200),
    frIndexedString3 NVARCHAR(200),
    frIndexedString2 NVARCHAR(200),
    frIndexedString1 NVARCHAR(200),
    frUnindexedInteger3 INT,
    frUnindexedInteger2 INT,
    frUnindexedInteger1 INT,
    description NVARCHAR(MAX),
    frIndexedInteger4 INT,
    frIndexedInteger3 INT,
    frIndexedInteger2 INT,
    frIndexedInteger1 INT,
    frIndexedInteger5 INT,
    userName NVARCHAR(200),
    frIndexedDate2 NVARCHAR(50),
    frIndexedDate1 NVARCHAR(50),
    deletion_count INT DEFAULT 1,
    first_deleted_at DATETIME DEFAULT GETDATE(),
    last_deleted_at DATETIME DEFAULT GETDATE()
);
GO

-- Create stored procedure for archiving deleted users
CREATE OR ALTER PROCEDURE sp_archive_deleted_users
    @_id NVARCHAR(100) = NULL,
    @_rev NVARCHAR(100) = NULL,
    @custom_RegCompanyName NVARCHAR(200) = NULL,
    @frUnindexedString1 NVARCHAR(200) = NULL,
    @frUnindexedString2 NVARCHAR(200) = NULL,
    @frUnindexedString3 NVARCHAR(200) = NULL,
    @frUnindexedString4 NVARCHAR(200) = NULL,
    @frUnindexedString5 NVARCHAR(200) = NULL,
    @frIndexedString11 NVARCHAR(200) = NULL,
    @frIndexedString12 NVARCHAR(200) = NULL,
    @frIndexedString10 NVARCHAR(200) = NULL,
    @frIndexedString19 NVARCHAR(200) = NULL,
    @frIndexedString17 NVARCHAR(200) = NULL,
    @frIndexedString18 NVARCHAR(200) = NULL,
    @frIndexedString15 NVARCHAR(200) = NULL,
    @frIndexedString16 NVARCHAR(200) = NULL,
    @frIndexedString13 NVARCHAR(200) = NULL,
    @frIndexedString14 NVARCHAR(200) = NULL,
    @givenName NVARCHAR(200) = NULL,
    @frIndexedString20 NVARCHAR(200) = NULL,
    @telephoneNumber NVARCHAR(50) = NULL,
    @city NVARCHAR(100) = NULL,
    @displayName NVARCHAR(200) = NULL,
    @accountStatus NVARCHAR(50) = NULL,
    @sn NVARCHAR(200) = NULL,
    @frUnindexedDate1 NVARCHAR(50) = NULL,
    @frIndexedString9 NVARCHAR(200) = NULL,
    @frIndexedString8 NVARCHAR(200) = NULL,
    @frIndexedString7 NVARCHAR(200) = NULL,
    @frIndexedString6 NVARCHAR(200) = NULL,
    @passwordLastChangedTime NVARCHAR(50) = NULL,
    @country NVARCHAR(100) = NULL,
    @mail NVARCHAR(200) = NULL,
    @frIndexedDate5 NVARCHAR(50) = NULL,
    @frIndexedDate4 NVARCHAR(50) = NULL,
    @frIndexedDate3 NVARCHAR(50) = NULL,
    @frIndexedString5 NVARCHAR(200) = NULL,
    @frIndexedString4 NVARCHAR(200) = NULL,
    @frIndexedString3 NVARCHAR(200) = NULL,
    @frIndexedString2 NVARCHAR(200) = NULL,
    @frIndexedString1 NVARCHAR(200) = NULL,
    @frUnindexedInteger3 INT=0,
    @frUnindexedInteger2 INT=0,
    @frUnindexedInteger1 INT=0,
    @description NVARCHAR(MAX) = NULL,
    @frIndexedInteger4 INT=0,
    @frIndexedInteger3 INT=0,
    @frIndexedInteger2 INT=0,
    @frIndexedInteger1 INT=0,
    @frIndexedInteger5 INT=0,
    @userName NVARCHAR(200) = NULL,
    @frIndexedDate2 NVARCHAR(50) = NULL,
    @frIndexedDate1 NVARCHAR(50) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM tbl_ArchivedUserDetails WHERE _id = @_id)
    BEGIN
        -- Increment deletion count and update last deleted time
        UPDATE tbl_ArchivedUserDetails
        SET deletion_count = deletion_count + 1,
            last_deleted_at = GETDATE(),
            _rev = @_rev,
            custom_RegCompanyName = @custom_RegCompanyName,
            frUnindexedString1 = @frUnindexedString1,
            frUnindexedString2 = @frUnindexedString2,
            frUnindexedString3 = @frUnindexedString3,
            frUnindexedString4 = @frUnindexedString4,
            frUnindexedString5 = @frUnindexedString5,
            frIndexedString11 = @frIndexedString11,
            frIndexedString12 = @frIndexedString12,
            frIndexedString10 = @frIndexedString10,
            frIndexedString19 = @frIndexedString19,
            frIndexedString17 = @frIndexedString17,
            frIndexedString18 = @frIndexedString18,
            frIndexedString15 = @frIndexedString15,
            frIndexedString16 = @frIndexedString16,
            frIndexedString13 = @frIndexedString13,
            frIndexedString14 = @frIndexedString14,
            givenName = @givenName,
            frIndexedString20 = @frIndexedString20,
            telephoneNumber = @telephoneNumber,
            city = @city,
            displayName = @displayName,
            accountStatus = @accountStatus,
            sn = @sn,
            frUnindexedDate1 = @frUnindexedDate1,
            frIndexedString9 = @frIndexedString9,
            frIndexedString8 = @frIndexedString8,
            frIndexedString7 = @frIndexedString7,
            frIndexedString6 = @frIndexedString6,
            passwordLastChangedTime = @passwordLastChangedTime,
            country = @country,
            mail = @mail,
            frIndexedDate5 = @frIndexedDate5,
            frIndexedDate4 = @frIndexedDate4,
            frIndexedDate3 = @frIndexedDate3,
            frIndexedString5 = @frIndexedString5,
            frIndexedString4 = @frIndexedString4,
            frIndexedString3 = @frIndexedString3,
            frIndexedString2 = @frIndexedString2,
            frIndexedString1 = @frIndexedString1,
            frUnindexedInteger3 = @frUnindexedInteger3,
            frUnindexedInteger2 = @frUnindexedInteger2,
            frUnindexedInteger1 = @frUnindexedInteger1,
            description = @description,
            frIndexedInteger4 = @frIndexedInteger4,
            frIndexedInteger3 = @frIndexedInteger3,
            frIndexedInteger2 = @frIndexedInteger2,
            frIndexedInteger1 = @frIndexedInteger1,
            frIndexedInteger5 = @frIndexedInteger5,
            userName = @userName,
            frIndexedDate2 = @frIndexedDate2,
            frIndexedDate1 = @frIndexedDate1
        WHERE _id = @_id;
    END
    ELSE
    BEGIN
        -- Insert new record
        INSERT INTO tbl_ArchivedUserDetails (
            _id, _rev, custom_RegCompanyName, frUnindexedString1, frUnindexedString2, frUnindexedString3,
            frUnindexedString4, frUnindexedString5, frIndexedString11, frIndexedString12, frIndexedString10,
            frIndexedString19, frIndexedString17, frIndexedString18, frIndexedString15, frIndexedString16,
            frIndexedString13, frIndexedString14, givenName, frIndexedString20, telephoneNumber, city,
            displayName, accountStatus, sn, frUnindexedDate1, frIndexedString9, frIndexedString8,
            frIndexedString7, frIndexedString6, passwordLastChangedTime, country, mail, frIndexedDate5,
            frIndexedDate4, frIndexedDate3, frIndexedString5, frIndexedString4, frIndexedString3,
            frIndexedString2, frIndexedString1, frUnindexedInteger3, frUnindexedInteger2, frUnindexedInteger1,
            description, frIndexedInteger4, frIndexedInteger3, frIndexedInteger2, frIndexedInteger1,
            frIndexedInteger5, userName, frIndexedDate2, frIndexedDate1
        )
        VALUES (
            @_id, @_rev, @custom_RegCompanyName, @frUnindexedString1, @frUnindexedString2, @frUnindexedString3,
            @frUnindexedString4, @frUnindexedString5, @frIndexedString11, @frIndexedString12, @frIndexedString10,
            @frIndexedString19, @frIndexedString17, @frIndexedString18, @frIndexedString15, @frIndexedString16,
            @frIndexedString13, @frIndexedString14, @givenName, @frIndexedString20, @telephoneNumber, @city,
            @displayName, @accountStatus, @sn, @frUnindexedDate1, @frIndexedString9, @frIndexedString8,
            @frIndexedString7, @frIndexedString6, @passwordLastChangedTime, @country, @mail, @frIndexedDate5,
            @frIndexedDate4, @frIndexedDate3, @frIndexedString5, @frIndexedString4, @frIndexedString3,
            @frIndexedString2, @frIndexedString1, @frUnindexedInteger3, @frUnindexedInteger2, @frUnindexedInteger1,
            @description, @frIndexedInteger4, @frIndexedInteger3, @frIndexedInteger2, @frIndexedInteger1,
            @frIndexedInteger5, @userName, @frIndexedDate2, @frIndexedDate1
        );
    END

END;
GO

-- Placeholder for second table (to be defined later)
-- IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tbl_SecondTable' AND xtype='U')
-- CREATE TABLE tbl_SecondTable (
--     id INT PRIMARY KEY IDENTITY,
--     -- Add columns as needed
-- );
-- GO</content>
<parameter name="filePath">/home/vboxuser/Code_To_Share/SQL/create_offboarding_db.sql