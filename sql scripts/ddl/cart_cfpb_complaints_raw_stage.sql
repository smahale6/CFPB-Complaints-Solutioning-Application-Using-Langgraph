USE [CART2.0]
GO

/****** Object:  Table [dbo].[cart_cfpb_complaints_stage]    Script Date: 8/24/2024 6:52:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS [dbo].[cart_cfpb_complaints_raw_stage]
Go
CREATE TABLE [dbo].[cart_cfpb_complaints_raw_stage](
	[Complaint_ID] [int] Not Null,
	[Date_received] [date] Null,
	[Product] [nvarchar](max) Null,
	[Sub_product] [nvarchar](max) Null,
	[Issue] [nvarchar](max) Null,
	[Sub_issue] [nvarchar](max) Null,
	[Consumer_complaint_narrative] [text] Null,
	[Company_public_response] [nvarchar](max) Null,
	[Company] [nvarchar](max) Null,
	[State] [nvarchar](max) Null,
	[ZIP_code] [nvarchar](max) Null,
	[Tags] [nvarchar](max) Null,
	[Consumer_consent_provided] [nvarchar](max) Null,
	[Submitted_via] [nvarchar](max) Null,
	[Date_sent_to_company] [date] Null,
	[Company_response_to_consumer] [nvarchar](max) Null,
	[Timely_response] [nvarchar](max) Null,
	[Consumer_disputed] [nvarchar](max) Null,
	[Loaded_By] [varchar](100) Null,
	[Cart_Log_Id] int not null
 CONSTRAINT [PK_complaints_stage] PRIMARY KEY CLUSTERED 
(
	[Complaint_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


