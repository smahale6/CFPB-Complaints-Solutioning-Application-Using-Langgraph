USE [CART2.0]
GO

/****** Object:  Table [dbo].[cart_cfpb_complaints_raw]    Script Date: 8/24/2024 6:52:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS [dbo].[cart_email_stage]
CREATE TABLE [dbo].[cart_email_stage]
(
	Complaint_ID int primary Key,
	Feedback varchar(max) null,
	Email_Response varchar(max) null ,
	Email_HTML varchar(max) null,
	Loaded_By            VARCHAR(10),
    Cart_Log_Id          INT
)


