__author__ = 'Hongyi'

import xlrd

book = xlrd.open_workbook("C:/Users/Hongyi/Desktop/Graphics.xls")
sheet = book.sheet_by_index(0)

print(sheet.name)
print(sheet.nrows)
print(sheet.ncols)

for row_index in range(sheet.nrows):
    for col_index in range(sheet.ncols):
        print(xlrd.cellname(row_index, col_index), '-', sheet.cell(row_index, col_index).value)
