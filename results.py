import datetime
import xlsxwriter as xlsxwriter
from user import User


class Results:

    def __init__(self):
        self.file_name = ''
        self.counter = 2

    def get_result_current_day(self):
        data = User().get_today_connection_results()
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
        data = User().get_all_connection_results()
        workbook = xlsxwriter.Workbook('../reports/All_results.xlsx')
        worksheet = workbook.add_worksheet('results')
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
        all_connected = User().count_connections()[1][0]
        all_accepted = User().count_accepted()[1][0]
        chart_cheet = workbook.add_worksheet("Chart")
        chart = workbook.add_chart({'type': 'pie'})

        data = [
            ['Send requests', 'Accept requests'],
            [all_connected, all_accepted],
        ]

        chart_cheet.write_column('A1', data[0])
        chart_cheet.write_column('B1', data[1])

        chart.add_series({
            'categories': '=Chart!$A$1:$A$2',
            'values': '=Chart!$B$1:$B$2',
            'points': [
                {'fill': {'color': 'gray'}},
                {'fill': {'color': 'green'}},
            ],
        })

        chart_cheet.insert_chart('C3', chart)

        workbook.close()

    def create_file(self):
        file_name = str(datetime.datetime.today().replace(microsecond=0)).replace(':', '-')
        self.file_name = file_name
        self.wb = xlsxwriter.Workbook('../reports/{}.xlsx'.format(self.file_name))
        worksheet = self.wb.add_worksheet('feed')
        worksheet.set_column('A:B', 100)
        worksheet.set_column('B:C', 50)
        format = self.wb.add_format({'bold': True})

        worksheet.write('A1', "Text", format)
        worksheet.write('B1', "Link", format)

    def update_file(self, text, link):
        worksheet = self.wb.get_worksheet_by_name('feed')
        format = self.wb.add_format()
        format.set_text_wrap()
        worksheet.write('A{}'.format(self.counter), text, format)
        worksheet.write('B{}'.format(self.counter), link)
        self.counter += 1

