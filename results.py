import xlsxwriter as xlsxwriter
import user


class Results(object):

    def __init__(self):
        pass

    def get_result_current_day(self):
        data = user.get_today_connection_results()
        workbook = xlsxwriter.Workbook('{}.xlsx'.format(data[0]))
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 30)
        format = workbook.add_format({'bold': True})
        worksheet.write('A2', str(data[0]), format)

        counter = 2
        for item in data[1]:
            worksheet.write('B{}'.format(counter), item[0])
            counter += 1


if __name__ == '__main__':
    Results()

