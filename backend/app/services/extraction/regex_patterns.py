FACTURE_PATTERNS = {


"reference":

r"(FACTURE|FAC)\s*N[°O]?\s*[:\-]?\s*([A-Z0-9\-]+)",


"date":

r"\d{2}/\d{2}/\d{4}",


"total_ht":

r"TOTAL\s*HT\s*[:\-]?\s*(\d+[.,]\d+)",


"total_ttc":

r"TOTAL\s*TTC\s*[:\-]?\s*(\d+[.,]\d+)"


}