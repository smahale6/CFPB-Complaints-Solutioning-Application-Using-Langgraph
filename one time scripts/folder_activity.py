import os

class folder_activity_class:
    
    def create_regulations_folders(self,cart_path):
        regulations_path = os.path.join(cart_path, 'regulations')
        # List of CFPB regulations
        cfpb_regulations = [
                            'Reg_B (Equal Credit Opportunity Act - ECOA)',
                            'Reg_C (Home Mortgage Disclosure Act - HMDA)',
                            'Reg_D (Alternative Mortgage Transaction Parity Act)',
                            'Reg_E (Electronic Fund Transfer Act - EFTA)',
                            'Reg_F (Fair Debt Collection Practices Act - FDCPA)',
                            'Reg_G (S.A.F.E. Mortgage Licensing Act – Federal Registration of Residential Mortgage Loan Originators)',
                            'Reg_H (S.A.F.E. Mortgage Licensing Act – State Compliance and Bureau Registration System)',
                            'Reg_I (Disclosure Requirements for Depository Institutions Lacking Federal Deposit Insurance)',
                            'Reg_J (Land Sales Registration)',
                            'Reg_K (Purchasers’ Revocation Rights, Sales Practices and Standards)',
                            'Reg_L (Protection of Nonpublic Personal Information)',
                            'Reg_M (Consumer Leasing)',
                            'Reg_N (Mortgage Acts and Practices – Advertising Rule)',
                            'Reg_O (Mortgage Assistance Relief Services - MARS Rule)',
                            'Reg_P (Privacy of Consumer Financial Information)',
                            'Reg_V (Fair Credit Reporting - FCRA)',
                            'Reg_X (Real Estate Settlement Procedures Act - RESPA)',
                            'Reg_Z (Truth in Lending Act - TILA)',
                            'Reg_CC (Availability of Funds and Collection of Checks)',
                            'Reg_DD (Truth in Savings Act - TISA)',
                            'Reg_AA (Unfair or Deceptive Acts or Practices)'
                            ]
        
        # Create the 'regulations' folder if it doesn't exist
        if not os.path.exists(regulations_path):
            os.makedirs(regulations_path)
            print("Created the 'regulations' folder.")
        else:
            print("The 'regulatons' folder already exists.")
        
        # Iterate over the list of CFPB regulations
        for regulation in cfpb_regulations:
            print(f"Addressing regulation: {regulation}.")
            # Create a folder for each regulation if it doesn't exist
            regulation_folder_path = os.path.join(regulations_path, regulation)
            
            if not os.path.exists(regulation_folder_path):
                os.makedirs(regulation_folder_path)
                print(f"    Created folder for {regulation}.")
            else:
                print(f"    {regulation} folder already exists.")
            
            # Create the 'archive' folder inside each regulation folder if it doesn't exist
            archive_folder_path = os.path.join(regulation_folder_path, 'archive')
            
            if not os.path.exists(archive_folder_path):
                os.makedirs(archive_folder_path)
                print(f"    Created archive folder inside {regulation}.")
            else:
                print(f"    The archive folder already exists for {regulation}.")
        
        print("Regulation folder structure setup completed.")
        
    def create_vector_db_folder(self,cart_path):
        vector_db_path = os.path.join(cart_path, 'vector_db')
        # Create the 'vector_db' folder if it doesn't exist
        if not os.path.exists(vector_db_path):
            os.makedirs(vector_db_path)
            print("Created the 'vector_db' folder.")
        else:
            print("The 'vector_db' folder already exists.")
        
        
        
if __name__ == "__main__":
    cart_path = r'C:\\GenAI\\CART'
    folder_activity_class_obj = folder_activity_class()
    folder_activity_class_obj.create_regulations_folders(cart_path)
    folder_activity_class_obj.create_vector_db_folder(cart_path)