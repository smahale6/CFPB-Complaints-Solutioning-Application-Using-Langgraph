USE [Cart2.0]
GO

/****** Object:  Table [dbo].[Fairlens_User_Profile]    Script Date: 2/13/2025 8:36:30 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS  [dbo].[CART_User_Profile]
Go
CREATE TABLE [dbo].[CART_User_Profile](
	[User_ID] [varchar](100) NOT NULL,
	[Password] [varchar](100) NULL,
	[First_Name] [varchar](100) NOT NULL,
	[Last_Name] [varchar](100) NOT NULL,
	[Email_Address] [varchar](100) NOT NULL,
	[Permissions] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Email_Address] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[User_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[CART_User_Profile] ADD  DEFAULT ((0)) FOR [Permissions]
GO


