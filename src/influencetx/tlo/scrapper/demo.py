from get_witnesses_for_bill import get_witnesses_for_bill 

# Retrieved from db
bill_id = "HB 864"
session = "86"

witness_sections = get_witnesses_for_bill(bill_id, session)
import pprint; pprint.pprint(witness_sections)
