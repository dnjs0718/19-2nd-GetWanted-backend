import xlwt

from django.http import HttpResponse

from .models import Company

def excel_export(request):
    response = HttpResponse(content_type= "application/vns.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'result.xls'
    wb = xlwt.Workbook(encoding='ansi')
    ws = wb.add_sheet('검진리스트')

    row_num = 0
    col_names = ['name', 'address']

    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)

    rows = Company.objects.all().values_list('name','address')

    for row in rows:
        row_num+=1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr)
    
    wb.save(response)

    return response
