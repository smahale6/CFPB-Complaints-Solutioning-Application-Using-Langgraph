USE [Cart2.0]
GO
/****** Object:  StoredProcedure [dbo].[uspload_cart_cfpb_complaints_raw]    Script Date: 3/12/2025 12:12:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[uspload_rpt_cfpb_complaints]
As
BEGIN


Drop Table If EXISTS #rpt_cfpb_complaints
SELECT 
       [Complaint_ID]                 = cfpb.[Complaint_ID]
      ,[Date_Received]				  = cfpb.[Date_Received]
      ,[Product]					  = cfpb.[Product]
      ,[Sub_Product]				  = cfpb.[Sub_Product]
      ,[Issue]						  = cfpb.[Issue]
      ,[Sub_Issue]					  = cfpb.[Sub_Issue]
      ,[Complaint_Text]				  = cfpb.[Complaint_Text]
      ,[Company_Public_Response]	  = cfpb.[Company_Public_Response]
      ,[Company]					  = cfpb.[Company]
      ,[State]						  = cfpb.[State]
      ,[ZIP_Code]					  = cfpb.[ZIP_Code]
      ,[Tags]						  = cfpb.[Tags]
      ,[Consumer_Consent_Provided]	  = cfpb.[Consumer_Consent_Provided]
      ,[Submitted_Via]				  = cfpb.[Submitted_Via]
      ,[Date_Sent_To_Company]		  = cfpb.[Date_Sent_To_Company]
      ,[Company_Response_To_Consumer] = cfpb.[Company_Response_To_Consumer]
      ,[Timely_Response]			  = cfpb.[Timely_Response]
      ,[Consumer_Disputed]			  = cfpb.[Consumer_Disputed]
      ,[Summarized_Complaint]         = reg.[Summarized_Complaint]
      ,[Total_Regulations]			  = reg.[Total_Regulations]
      ,[Regulation_Names]			  = reg.[Regulation_Names]
      ,[Explanations]				  = reg.[Explanations]
      ,[Solutions]					  = reg.[Solutions]
	  ,[Feedback]                     = email.[Feedback]       
      ,[Email_Response]				  = email.[Email_Response]	
      ,[Email_HTML]					  = email.[Email_HTML]		
  Into #rpt_cfpb_complaints
  FROM [dbo].[cart_cfpb_complaints_raw]                      cfpb   with (nolock)
       left join [dbo].[cart_cfpb_complaints_reg_summarized] reg    with (nolock) on cfpb.[Complaint_ID] = reg.[Complaint_ID]
	   left join [dbo].[cart_email]                          email  with (nolock) on cfpb.[Complaint_ID] = email.[Complaint_ID]
        
Truncate Table dbo.rpt_cfpb_complaints
Insert into dbo.rpt_cfpb_complaints
Select * from #rpt_cfpb_complaints


Drop Table If EXISTS #rpt_cfpb_complaints
End