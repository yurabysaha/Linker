import xlsxwriter as xlsxwriter
import user


class Results:

    def __init__(self):
        pass

    def get_result_current_day(self):
        data = user.get_today_connection_results()
        workbook = xlsxwriter.Workbook('../reports/{}.xlsx'.format(data[0]))
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 25)
        worksheet.set_column('D:E', 25)
        format = workbook.add_format({'bold': True})
        green = workbook.add_format({'bold': True, 'bg_color': '#C0EB9F'})

        worksheet.write('A1', "Date", format)
        worksheet.write('B1', "Name", format)
        worksheet.write('C1', "Accept", format)
        worksheet.write('D1', "Send message", format)
        worksheet.write('E1', "Send second message", format)
        worksheet.write('F1', "Finished", format)
        worksheet.write('A2', str(data[0]), format)

        counter = 2
        for item in data[1]:
            worksheet.write('B{}'.format(counter), item[0])
            worksheet.write('C{}'.format(counter), item[1])
            worksheet.write('D{}'.format(counter), item[2])
            worksheet.write('E{}'.format(counter), item[3])
            if item[4] == 1:
                worksheet.write('F{}'.format(counter), item[4], green)
            else:
                worksheet.write('F{}'.format(counter), item[4])
            counter += 1

    def get_all_result(self):
        data = user.get_all_connection_results()
        workbook = xlsxwriter.Workbook('../reports/All_results.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 25)
        worksheet.set_column('D:E', 25)
        format = workbook.add_format({'bold': True})
        green = workbook.add_format({'bold': True, 'bg_color': '#C0EB9F'})
        worksheet.write('A1', "Date", format)
        worksheet.write('B1', "Name", format)
        worksheet.write('C1', "Accept", format)
        worksheet.write('D1', "Send message", format)
        worksheet.write('E1', "Send second message", format)
        worksheet.write('F1', "Finished", format)
        format_dict = {}
        for date, value, accept, mes, second, finish in data:
            try:
                format_dict[date].append([value, accept, mes, second, finish])
            except KeyError:
                format_dict[date] = [[value, accept, mes, second, finish]]

        keys = format_dict.keys()

        row_for_date = 2
        counter = 2
        for each in keys:
            worksheet.write('A{}'.format(row_for_date), each, format)
            index = 0

            for i in format_dict[each]:
                worksheet.write('B{}'.format(counter), i[0])
                worksheet.write('C{}'.format(counter), i[1])
                worksheet.write('D{}'.format(counter), i[2])
                worksheet.write('E{}'.format(counter), i[3])
                if i[4] == 1:
                    worksheet.write('F{}'.format(counter), i[4], green)
                else:
                    worksheet.write('F{}'.format(counter), i[4])

                counter += 1
                index += 1
            row_for_date += counter -1
            counter +=1
