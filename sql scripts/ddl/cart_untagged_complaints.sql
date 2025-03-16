/****** Object:  Table [dbo].[cart_untagged_complaints]    Script Date: 3/15/2025 2:55:05 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[cart_untagged_complaints](
	[Complaint_ID] [int] NOT NULL,
	[Complaint_Text] [text] NULL,
	[Company] [varchar](100) NULL,
	[State] [varchar](50) NULL,
	[ZIP_Code] [varchar](15) NULL,
	[Product] [varchar](500) NULL,
	[Sub_Product] [varchar](500) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


