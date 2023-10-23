import xlsxwriter

class Writer:

    def __init__(self, fileName, dataArray):
        fileName = fileName.split('.')[0]
        # Create a workbook
        workbook = xlsxwriter.Workbook(f'{fileName}.xlsx')

        # Create a worksheet
        worksheet = workbook.add_worksheet('Questions')

        for row_num, row_data in enumerate(dataArray):
            for col_num, col_data in enumerate(row_data):
                worksheet.write(row_num, col_num, col_data)
        
        workbook.close()