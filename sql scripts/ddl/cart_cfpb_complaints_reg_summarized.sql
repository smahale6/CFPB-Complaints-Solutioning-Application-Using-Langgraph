USE [CART2.0]
GO

/****** Object:  Table [dbo].[cart_cfpb_complaints_reg]    Script Date: 8/24/2024 6:52:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS [dbo].cart_cfpb_complaints_reg_summarized
go
CREATE TABLE [dbo].cart_cfpb_complaints_reg_summarized (
	[Complaint_ID]                  [int] NOT NULL,
	[Complaint_Text]                [varchar](max) NULL,
	[Company]                       [varchar](110) null,
	[State]                         [varchar](110) null,
	[Zip_Code]                      [varchar](10) null,
	[Summarized_Complaint]          [varchar](max) null,
	[Total_Regulations]             [int] NOT NULL,
	[Regulation_Names]              [varchar](max) NOT NULL,
	[Explanations]                  [varchar](max) NOT NULL,
	[Solutions]                     [varchar](max) null ,      
	[Loaded_By]                     [varchar](10) Not NULL,
	[Cart_Log_Id]					[int] NULL,
	[Load_Date]                     [Datetime] not null
	
 CONSTRAINT [PK_comp_reg_summary] PRIMARY KEY CLUSTERED 
(
	[Complaint_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
