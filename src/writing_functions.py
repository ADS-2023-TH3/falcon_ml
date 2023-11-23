import datetime as dt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_dataframe import set_with_dataframe


"""The following function will connect to a specific sheet of the data workbook"""
def connect_to_sheet(worksheet_name):
    # Define the scope and credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("movierecommender-405816-41309bde9020.json", scope)
    file_id = '1aJPqNvbLqZg1N1iyx6IrGVYxgKypDhRwgfY3Xkw-I4o'
    # Authenticate with Google Sheets
    gc = gspread.authorize(credentials)

    try:
        # Open the Google Sheets file by its file ID
        sh = gc.open_by_key(file_id)

        # Open the specific worksheet by its name
        worksheet = sh.worksheet(worksheet_name)

        # Now, 'worksheet' represents the specific worksheet you want to work with
        return worksheet
    except gspread.exceptions.WorksheetNotFound:
        print(f"Worksheet '{worksheet_name}' not found.")
        return None

def Sheet_to_df(worksheet):
    if worksheet:
        # Read the first row of data as column names
        column_names = worksheet.row_values(1)

        # Read the remaining data from the worksheet, excluding the first row
        data = worksheet.get_all_values()[1:]

        # Create a DataFrame with the data and set column names
        df = pd.DataFrame(data, columns=column_names)

        return df
    else:
        return None
    
"""The following functions will connect to a specific sheet of the data workbook and add a line at the end 
of those sheets"""
    
def add_log(user, input, output):
    worksheet=connect_to_sheet('logs_sheet')
    data = {
    "user": [user],
    "date": [dt.datetime.now().strftime("%Y-%m-%d")],
    "input": [input],
    "output": [output]
    }
    df = pd.DataFrame(data)
    set_with_dataframe(worksheet, df, col=1,row=len(worksheet.get_all_records()) + 2 ,include_column_header=False)

def add_user(user, hash):
    worksheet=connect_to_sheet('users_sheet')
    data = {
    "user": [user],
    "hash": [hash],
    }
    df = pd.DataFrame(data)
    set_with_dataframe(worksheet, df, col=1,row=len(worksheet.get_all_records()) + 2 ,include_column_header=False)


def add_rating(user, movie, rating):
    worksheet=connect_to_sheet('feedback_sheet')
    data = {
    "user": [user],
    "hash": [movie],
    "rating":[rating]
    }
    df = pd.DataFrame(data)
    set_with_dataframe(worksheet, df, col=1,row=len(worksheet.get_all_records()) + 2 ,include_column_header=False)

add_rating('Arturo','Estoriboris','10')