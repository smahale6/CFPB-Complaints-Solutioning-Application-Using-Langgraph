SELECT 'TRUNCATE TABLE ' + TABLE_SCHEMA + '.' + TABLE_NAME + ';' 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE';


TRUNCATE TABLE dbo.cart_email_stage;
TRUNCATE TABLE dbo.cart_email;
TRUNCATE TABLE dbo.cart_cfpb_complaints_reg_summarized;
TRUNCATE TABLE dbo.cart_cfpb_complaints_reg_stage;
TRUNCATE TABLE dbo.cart_cfpb_complaints_reg;
TRUNCATE TABLE dbo.cart_cfpb_complaints_raw_stage;
TRUNCATE TABLE dbo.cart_cfpb_complaints_raw;
TRUNCATE TABLE dbo.rpt_cfpb_complaints;
TRUNCATE TABLE dbo.cart_untagged_complaints;
TRUNCATE TABLE dbo.cart_log;