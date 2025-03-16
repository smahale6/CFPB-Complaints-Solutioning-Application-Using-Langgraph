USE [Cart2.0]
GO

/****** Object:  Table [dbo].[rpt_cfpb_complaints]    Script Date: 3/12/2025 12:18:40 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS  [dbo].[rpt_cfpb_complaints]
Go
CREATE TABLE [dbo].[rpt_cfpb_complaints](
	[Complaint_ID] [int] NOT NULL,
	[Date_Received] [date] NULL,
	[Product] [varchar](100) NULL,
	[Sub_Product] [varchar](100) NULL,
	[Issue] [varchar](max) NULL,
	[Sub_Issue] [varchar](max) NULL,
	[Complaint_Text] [varchar](max) NULL,
	[Company_Public_Response] [varchar](100) NULL,
	[Company] [varchar](100) NULL,
	[State] [varchar](50) NULL,
	[ZIP_Code] [varchar](15) NULL,
	[Tags] [varchar](100) NULL,
	[Consumer_Consent_Provided] [varchar](100) NULL,
	[Submitted_Via] [varchar](100) NULL,
	[Date_Sent_To_Company] [date] NULL,
	[Company_Response_To_Consumer] [varchar](512) NULL,
	[Timely_Response] [varchar](100) NULL,
	[Consumer_Disputed] [varchar](100) NULL,
	[Summarized_Complaint] [varchar](max) NULL,
	[Total_Regulations] [int] NULL,
	[Regulation_Names] [varchar](max) NULL,
	[Explanations] [varchar](max) NULL,
	[Solutions] [varchar](max) NULL,
	[Feedback] [varchar](max) NULL,
	[Email_Response] [varchar](max) NULL,
	[Email_HTML] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


