from onetjobsInf.onet_credentials import get_credentials, get_user_input, check_for_error
import pandas as pd

# This function will return the rows of the table (e.g., skills) specified by the filter
# Returns only the relevant columns
def get_rows(onet_service, table_id, **query_params):
    rows_rslt = onet_service.call(f'/database/rows/{table_id}', **query_params)
    if check_for_error(rows_rslt):
        return None
    rows_df = pd.DataFrame(rows_rslt['row'])
    rows_df = rows_df[['element_name', 'data_value', 'lower_ci_bound', 'upper_ci_bound']]
    return rows_df

#this function gets unique labels from a table that are a combination of scale and element
# it returns a list of unique labels for the specified column (default is 'element_scale') 
def get_elements(onet_service, table_id, colname='element_scale', **query_params):
    rows_rslt = onet_service.call(f'/database/rows/{table_id}', **query_params)
    if check_for_error(rows_rslt):
        return None
    unique_elements = set()
    for row in rows_rslt['row']:
        if colname in row:
            unique_elements.add(row[colname])
    return list(unique_elements)


