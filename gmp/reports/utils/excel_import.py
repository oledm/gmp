import xlrd

class ExcelImporter():
    def read(self, filename):
        rb = xlrd.open_workbook(filename, formatting_info=True)
        sheet = rb.sheet_by_index(0)
        rows = []
        for rownum in range(sheet.nrows):
            if rownum == 0:
                header = [r for r in sheet.row_values(rownum)] 
            else:
                rows.append([r for r in sheet.row_values(rownum)])
        return (header, rows)
