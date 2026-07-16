import gspread
from gspread_formatting import CellFormat, Color, format_cell_ranges

class GspreadSheetHelper:
    credential = gspread.service_account(filename='Service\\DayForce\\Utilites\\cred.json')
    sheet = credential.open("10. codebotforT1_sfadmin_REC_Workbook")

    def getsheet(self, sheet_name):
        """Function to get the worksheet object from the Google Sheet"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            return worksheet
        except Exception as e:
            print(f"Error occurred while fetching the worksheet: {e}")
            return " "

    def start_end_row(self, worksheet):
        """Function to get the starting and ending row of a column in the worksheet"""
        try:
            start=4
            end=len(worksheet.col_values(7))
            if end==1:
                end = 4
            return start,end
        except Exception as e:
            print(f"no data found in the sheet")
            return 4, 4
    

    def data_from_sheet(self, worksheet, col1, col2):
        """Function to get the data from a specific column in the worksheet"""
        try:
            start=4
            end=len(worksheet.col_values(9))
            new_list=worksheet.get(f"{col1}{start}:{col2}{end}")
            return start,end,new_list
        except Exception as e:
            print(f"Error occurred while fetching data from the sheet: {e}")
            return 4, 4, []


    def clear_sheet(self, worksheet):
        """Function to clear the data from a specific column in the worksheet"""
        try:
            start_row, end = self.start_end_row(worksheet)
            if end < start_row:
                print(f"No data found in the sheet")
                end = 500

            print(f"Clearing data from row {start_row} to {end} in the worksheet.")
            worksheet.batch_clear([f"A{start_row}:K{end}"])
        except Exception as e:
            print(f"Error occurred while clearing the sheet: {e}")

    
    def update_sheet(self,worksheet,col1,col2,data):
        """Function to update the data in a specific column in the worksheet"""
        try:
            location = f'{col1}4:{col2}{3 + len(data)}'
            worksheet.update(location, data)
        except Exception as e:
            print(f"An error occurred while updating the sheet: {e}")


    def colors_r_g_b(self):
        """Function to get the colors for formatting the cells in the Google Sheet"""
        green = CellFormat(backgroundColor=Color(0.7, 1, 0.7))
        red = CellFormat(backgroundColor=Color(1,0.7,0.7))
        white = CellFormat(backgroundColor=Color(1,1,1))
        return green, red , white