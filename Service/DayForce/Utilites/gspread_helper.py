import os
import gspread
from dotenv import load_dotenv
from gspread_formatting import CellFormat, Color, format_cell_ranges
    
load_dotenv()

class GspreadSheetHelper:

    credential = gspread.service_account(filename='Service\\DayForce\\Utilites\\cred.json')
    file_name = os.environ['FILE_NAME']
    sheet = credential.open(file_name)
    worksheet = sheet.worksheet(os.environ['SHEET_NAME'])

    def getsheet(self, sheet_name):
        """Function to get the worksheet object from the Google Sheet"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            return worksheet
        except Exception as e:
            print(f"Error occurred while fetching the worksheet: {e}")
            return " "

    def start_end_row(self):
        """Function to get the starting and ending row of a column in the worksheet"""
        try:
            start=4
            end=len(self.worksheet.col_values(7))
            if end==1:
                end = 4
            return start,end
        except Exception as e:
            print(f"no data found in the sheet")
            return 4, 4
    

    def data_from_sheet(self, col1, col2):
        """Function to get the data from a specific column in the worksheet"""
        try:
            start=4
            end=len(self.worksheet.col_values(9))
            new_list=self.worksheet.get(f"{col1}{start}:{col2}{end}")
            return start,end,new_list
        except Exception as e:
            print(f"Error occurred while fetching data from the sheet: {e}")
            return 4, 4, []


    def clear_sheet(self,col1,col2):
        """Function to clear the data from a specific column in the worksheet"""
        try:
            start_row, end = self.start_end_row()
            if end < start_row:
                print(f"No data found in the sheet")
                end = 500

            print(f"Clearing data from row {start_row} to {end} in the worksheet.")
            self.formate_sheet(col1, col2, CellFormat(backgroundColor=Color(1, 1, 1)))  # Reset to white background
            self.worksheet.batch_clear([f"{col1}{start_row}:{col2}{end}"])
        except Exception as e:
            print(f"Error occurred while clearing the sheet: {e}")

    
    def update_sheet(self,col1,col2,data):
        """Function to update the data in a specific column in the worksheet"""
        try:
            location = f'{col1}4:{col2}{3 + len(data)}'
            self.worksheet.update(location, data)
        except Exception as e:
            print(f"An error occurred while updating the sheet: {e}")


    def colors_r_g_b(self):
        """Function to get the colors for formatting the cells in the Google Sheet"""
        green = CellFormat(backgroundColor=Color(0.7, 1, 0.7))
        red = CellFormat(backgroundColor=Color(1,0.7,0.7))
        white = CellFormat(backgroundColor=Color(1,1,1))
        return green, red , white
    

    def formate_sheet(self,col1,col2,color):
        """Function to format the cells in the Google Sheet"""
        try:
            start_row, end = self.start_end_row()
            format_cell_ranges(self.worksheet, [(f"{col1}{start_row}:{col2}{end}", color)])
        except Exception as e:
            print(f"An error occurred while formatting the sheet: {e}")
    
    def batch_formate_sheet(self,loc_data):
        """Function to format the cells in the Google Sheet"""
        try:
            format_cell_ranges(self.worksheet,loc_data)
        except Exception as e:
            print(f"An error occurred while formatting the sheet: {e}")



    def get_sheet_data(self, col1, col2,Pad_values=False):
        """Function to get the data from a specific column in the worksheet"""
        try:
            start_row, end = self.start_end_row()
            data = self.worksheet.get(f"{col1}{start_row}:{col2}{end}", pad_values=Pad_values)
            return data
        except Exception as e:
            print(f"Error occurred while fetching data from the sheet: {e}")
            return []