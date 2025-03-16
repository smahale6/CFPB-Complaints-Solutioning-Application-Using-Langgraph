USE [Cart2.0]
GO

/****** Object:  Table [dbo].[cart_email]    Script Date: 3/12/2025 4:31:03 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS  [dbo].[cart_email]
Go
CREATE TABLE [dbo].[cart_email](
	[Complaint_ID] [int] NOT NULL,
	[Feedback] [varchar](max) NULL,
	[Email_Response] [varchar](max) NULL,
	[Email_HTML] [varchar](max) NULL,
	[Loaded_By] [varchar](10) NULL,
	[Cart_Log_Id] [int] NULL,
	[Load_Date] [date] NULL,
	[Update_Date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[Complaint_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


