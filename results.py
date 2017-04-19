import xlsxwriter as xlsxwriter
import user


class Results:

    def __init__(self):
        pass

    def get_result_current_day(self):
        data = user.get_today_connection_results()
        workbook = xlsxwriter.Workbook('../reports/{}.xlsx'.format(data[0]))
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 30)
        format = workbook.add_format({'bold': True})
        worksheet.write('A2', str(data[0]), format)

        counter = 2
        for item in data[1]:
            worksheet.write('B{}'.format(counter), item[0])
            counter += 1

    def get_all_result(self):
        data = user.get_all_connection_results()
        workbook = xlsxwriter.Workbook('../reports/All_results.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 30)
        format = workbook.add_format({'bold': True})

        format_dict = {}
        for date, value in data:
            try:
                format_dict[date].append(value)
            except KeyError:
                format_dict[date] = [value]

        # print (ddd)

        keys = format_dict.keys()
        row_for_date = 1
        counter = 1
        for each in keys:
            worksheet.write('A{}'.format(row_for_date), each, format)
            index = 0

            for i in format_dict[each]:
                name = i
                worksheet.write('B{}'.format(counter), name)
                counter += 1
                index += 1
            row_for_date += counter
            counter +=1
