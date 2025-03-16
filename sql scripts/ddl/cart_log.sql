USE [Cart2.0]
GO

/****** Object:  Table [dbo].[cart_log]    Script Date: 2/19/2025 4:18:19 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[cart_log](
	[Cart_Log_Id] [int] IDENTITY(1000,1) NOT NULL,
	[Version] [float] NOT NULL,
	[Cart_Log_Status] [varchar](100) NULL,
	[Total_Complaints] [int] NOT NULL,
	[Reg_B_Count] [int] NOT NULL,
	[Reg_C_Count] [int] NOT NULL,
	[Reg_D_Count] [int] NOT NULL,
	[Reg_E_Count] [int] NOT NULL,
	[Reg_F_Count] [int] NOT NULL,
	[Reg_G_Count] [int] NOT NULL,
	[Reg_H_Count] [int] NOT NULL,
	[Reg_I_Count] [int] NOT NULL,
	[Reg_J_Count] [int] NOT NULL,
	[Reg_K_Count] [int] NOT NULL,
	[Reg_L_Count] [int] NOT NULL,
	[Reg_M_Count] [int] NOT NULL,
	[Reg_N_Count] [int] NOT NULL,
	[Reg_O_Count] [int] NOT NULL,
	[Reg_P_Count] [int] NOT NULL,
	[Reg_V_Count] [int] NOT NULL,
	[Reg_X_Count] [int] NOT NULL,
	[Reg_Z_Count] [int] NOT NULL,
	[Reg_CC_Count] [int] NOT NULL,
	[Reg_DD_Count] [int] NOT NULL,
	[Reg_AA_Count] [int] NOT NULL,
	[Tagged_By] [varchar](100) NOT NULL,
	[Log_Date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[Cart_Log_Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Total_Complaints]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_B_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_C_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_D_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_E_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_F_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_G_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_H_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_I_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_J_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_K_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_L_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_M_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_N_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_O_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_P_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_V_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_X_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_Z_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_CC_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_DD_Count]
GO

ALTER TABLE [dbo].[cart_log] ADD  DEFAULT ((0)) FOR [Reg_AA_Count]
GO


