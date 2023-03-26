# initial imports
import pandas as pd
import shutil
import json
import time
import os

# libraries from google
from google.colab import auth
auth.authenticate_user()
import gspread
from gspread_dataframe import set_with_dataframe
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

def export_to_google_sheet(worksheet_name = 'twitter file to sheets', file_name = 'tweets.js'):

    # try to open the worksheet in your google drive
    try:
        worksheet = gc.open(worksheet_name).sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        worksheet = gc.create(worksheet_name).sheet1

    # clear the worksheet completely before filling
    worksheet.clear()

    # replace .js to .txt
    file_name = file_name.replace('/content/', '').replace('.js', '')
    shutil.copy(f'/content/{file_name}.js', f'/content/{file_name}.txt')

    # replace first line
    with open(f'/content/{file_name}.txt', 'r') as f:
        content = f.read()
        content = content.replace('window.YTD.tweets.part0 = ', '')
    with open(f'/content/{file_name}.txt', 'w') as f:
        f.write(content)
    time.sleep(1)

    # replace .txt to .json
    os.rename(f'/content/{file_name}.txt', f'/content/{file_name}.json')

    # set column titles
    with open(f'/content/{file_name}.json', 'r') as f:
        dados_json = json.load(f)

    df = pd.json_normalize(dados_json)

    # export data to worksheet
    set_with_dataframe(worksheet, df)

### CALL IT ###

# .js file from Twitter to a Google Sheets
export_to_google_sheet(
    worksheet_name = 'twitter file to sheets',    # write and it will be created in your Drive
    file_name = 'tweets.js')                      # write your file's name (you must upload it)
