-- This stored procedure archives a user by copying their record from the active
-- user table to the archive table, and then deleting them from the active table.
-- This operation is performed in a single transaction.
CREATE OR REPLACE FUNCTION sp_archive_deleted_users(p_user_id TEXT)
RETURNS VOID AS $$
BEGIN
    -- Raise a notice for debugging purposes to track which user is being processed.
    RAISE NOTICE 'Archiving user ID: %', p_user_id;

    -- Copy the full user record from the active table to the archive table.
    -- The archived_at timestamp is set automatically by the table's default.
    INSERT INTO tbl_archivedalphauserdetails (
        _id, _rev, custom_regcompanyname, frunindexedstring1, frunindexedstring2, frunindexedstring3,
        frunindexedstring4, frunindexedstring5, frindexedstring11, frindexedstring12, frindexedstring10,
        frindexedstring19, frindexedstring17, frindexedstring18, frindexedstring15, frindexedstring16,
        frindexedstring13, frindexedstring14, givenname, frindexedstring20, telephonenumber, city,
        displayname, accountstatus, sn, frunindexeddate1, frindexedstring9, frindexedstring8,
        frindexedstring7, frindexedstring6, passwordlastchangedtime, country, mail, frindexeddate5,
        frindexeddate4, frindexeddate3, frindexedstring5, frindexedstring4, frindexedstring3,
        frindexedstring2, frindexedstring1, frunindexedinteger3, frunindexedinteger2, frunindexedinteger1,
        description, frindexedinteger4, frindexedinteger3, frindexedinteger2, frindexedinteger1,
        frindexedinteger5, username, frindexeddate2, frindexeddate1, last_modified, operation_type
    )
    SELECT
        _id, _rev, custom_regcompanyname, frunindexedstring1, frunindexedstring2, frunindexedstring3,
        frunindexedstring4, frunindexedstring5, frindexedstring11, frindexedstring12, frindexedstring10,
        frindexedstring19, frindexedstring17, frindexedstring18, frindexedstring15, frindexedstring16,
        frindexedstring13, frindexedstring14, givenname, frindexedstring20, telephonenumber, city,
        displayname, accountstatus, sn, frunindexeddate1, frindexedstring9, frindexedstring8,
        frindexedstring7, frindexedstring6, passwordlastchangedtime, country, mail, frindexeddate5,
        frindexeddate4, frindexeddate3, frindexedstring5, frindexedstring4, frindexedstring3,
        frindexedstring2, frindexedstring1, frunindexedinteger3, frunindexedinteger2, frunindexedinteger1,
        description, frindexedinteger4, frindexedinteger3, frindexedinteger2, frindexedinteger1,
        frindexedinteger5, username, frindexeddate2, frindexeddate1, last_modified, operation_type
    FROM tbl_alphauserdetails
    WHERE _id = p_user_id;

    -- Delete the user from the active table now that they are archived.
    DELETE FROM tbl_alphauserdetails
    WHERE _id = p_user_id;

END;
$$ LANGUAGE plpgsql;