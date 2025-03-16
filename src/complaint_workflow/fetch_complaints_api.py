import requests
import pandas as pd
import logging
from logger import Logger

import warnings
warnings.filterwarnings('ignore')

class fetch_compalints_class:
    def __init__(self):
        self.api_url = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/'
        self.logger = Logger()

    def get_cfpb_complaints(self, employee_id, cart_log_id, date_received_min, date_received_max, company="NAVY FEDERAL CREDIT UNION", total_records=500):
        """
        Fetches CFPB complaints with valid narratives and avoids duplicates.
        
        :param employee_id: ID of the employee fetching data
        :param cart_log_id: Log ID for tracking
        :param date_received_min: Start date for complaints
        :param date_received_max: End date for complaints
        :param company: Name of the company (Default: NAVY FEDERAL CREDIT UNION)
        :param total_records: Number of complaints to fetch (Default: 500)
        :return: DataFrame of complaints
        """
        print(f"  - Date Range: {date_received_min} to {date_received_max}")
        print(f"  - Company: {company}")
        print(f"  - Total Records Requested: {total_records}")

        print(f"🔍 Fetching {total_records} complaints for {company} from {date_received_min} to {date_received_max}")
        logging.info(f"Fetching {total_records} complaints for {company} from {date_received_min} to {date_received_max}")

        fetched_complaints = []
        fetched_ids = set()
        batch_size = 50
        from_value = 0  

        # Using requests.Session() for efficiency
        with requests.Session() as session:
            session.headers.update({
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            })

            while len(fetched_complaints) < total_records:
                params = {
                    "size": batch_size,
                    "from": from_value,
                    "company": company,
                    "date_received_min": date_received_min,
                    "date_received_max": date_received_max
                }

                try:
                    response = session.get(self.api_url, params=params, timeout=10, verify=False)
                    response.raise_for_status()  # Raise an error for failed requests

                    data = response.json()

                    if 'hits' not in data or 'hits' not in data['hits']:
                        print("⚠️ No valid complaints found in response.")
                        logging.info("No valid complaints found in response.")
                        break

                    complaints = data['hits']['hits']
                    if not complaints:
                        print("⚠️ No more complaints available from API.")
                        logging.info("No more complaints available from API.")
                        break

                    for complaint in complaints:
                        complaint_narrative = complaint['_source'].get('complaint_what_happened', "").strip()
                        complaint_id = complaint['_id']

                        if complaint_narrative and complaint_id not in fetched_ids:
                            fetched_complaints.append({
                                "Complaint_ID":                     complaint_id,
                                "Date_received":                    complaint['_source'].get('date_received', None),
                                "Product":                          complaint['_source'].get('product', None),
                                "Sub_product":                      complaint['_source'].get('sub_product', None),
                                "Issue":                            complaint['_source'].get('issue', None),
                                "Sub_issue":                        complaint['_source'].get('sub_issue', None),
                                "Consumer_complaint_narrative":     complaint_narrative,
                                "Company_public_response":          complaint['_source'].get('company_public_response', None),
                                "Company":                          complaint['_source'].get('company', None),
                                "State":                            complaint['_source'].get('state', None),                       
                                "ZIP_code":                         complaint['_source'].get('zip_code', None),
                                "Tags":                             complaint['_source'].get('tags', None),
                                "Consumer_consent_provided":        complaint['_source'].get('consumer_consent_provided', None),
                                "Submitted_via":                    complaint['_source'].get('submitted_via', None),
                                "Date_sent_to_company":             complaint['_source'].get('date_sent_to_company', None),
                                "Company_response_to_consumer":     complaint['_source'].get('company_response_to_consumer', None),
                                "Timely_response":                  complaint['_source'].get('timely', None),
                                "Consumer_disputed":                complaint['_source'].get('consumer_disputed', None)
                            })
                            fetched_ids.add(complaint_id)

                        if len(fetched_complaints) >= total_records:
                            break

                    from_value += batch_size  

                except requests.exceptions.RequestException as e:
                    print(f"API Request Failed: {str(e)}")
                    logging.error(f"API Request Failed: {str(e)}")
                    break

        if fetched_complaints:
            df = pd.DataFrame(fetched_complaints)
            df['Loaded_By'] = employee_id
            df['Cart_Log_Id'] = cart_log_id
            print(f"Successfully fetched {len(df)} complaints.")
            logging.info(f"Successfully fetched {len(df)} complaints.")
            return df
        else:
            print("No valid complaints found after multiple attempts.")
            logging.info("No valid complaints found after multiple attempts.")
            return pd.DataFrame()

# ✅ Running standalone for testing
if __name__ == "__main__":
    import pyodbc

    employee_id = 'c6400'
    cart_log_id = 1001
    total_records = 10  
    date_received_min = "2024-01-01"
    date_received_max = "2024-12-31"
    company = "BANK OF AMERICA, NATIONAL ASSOCIATION"

    fetch_complaints_obj = fetch_compalints_class()
    cart_cfpb_complaints_raw_df = fetch_complaints_obj.get_cfpb_complaints(employee_id, cart_log_id, date_received_min, date_received_max, company, total_records)

