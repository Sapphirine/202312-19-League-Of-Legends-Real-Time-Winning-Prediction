from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd


# df = pd.DataFrame([
#     "time",
#     "firstBlood",
#     "firstTower",
#     "firstInhibitor",
#     "firstDragon",
#     "tower_amount",
#     "inhibs_amount",
#     "Dragons_Amount",
#     "riftHeralds_amount",
#     "Kills_Diff",
#     "Death_Diff",
#     "Assist_Diff",
#     "Lv_Diff",
#     "cs_Diff",
#     "jg_cs_Diff",
#     "win_probability",
# ])

credentials = service_account.Credentials.from_service_account_file(
    'e6893final-53e7e65dd00e.json')
project_id = 'E6893Final'
client = bigquery.Client(credentials=credentials, project=project_id)

table_id = 'lol_live_data.live_data'

def upload_to_bigquery(df):
    # Assuming df is your DataFrame and it's properly formatted for BigQuery.
    df.to_gbq(table_id, project_id=project_id, if_exists='append', credentials=credentials)