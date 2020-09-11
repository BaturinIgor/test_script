import pandas as pd
import pyproj
import pycrs
import re


def main():
    file = open("result.txt", 'w')
    df = pd.read_csv('2020-09-07.csv')
    file.write("Название файла: 2020-09-07.csv\n")
    file.write('Кол-во строк в файле (не учитывая NULL): ' + str(df['link_id'].count()) + "\n")

    # 1
    file.write("1) Форматирование стобца link_id\n------------------------------------\n")
    file.write("Кол-во NULL в столбце link_id: " + str(df['link_id'].isnull().sum()) + "\n")  # кол-во null

    df = df.dropna(how='any')  # удаление null
    df['link_id'] = df['link_id'].astype("int")  # float->int

    file.write("Количество NULL после удаления их из таблицы: " + str(df['link_id'].isnull().sum()) + "\n")  # кол-во null после удаления
    file.write("Количество дублирующихся значений: " + str(df['link_id'].duplicated().sum()) + "\n")  # кол-во дублирующихся значений

    df['link_id'] = df['link_id'].drop_duplicates()  # удаление дублирующих значений
    file.write("Количество элементов после после форматирования: " + str(df['link_id'].count()) + "\n")  # кол-во после удаления



    # 2
    # print('------------------------------------\n2\n------------------------------------')
    # fromcrs = pycrs.parse.from_epsg_code(4326)
    # fromcrs_proj4 = fromcrs.to_proj4()
    # tocrs = pycrs.parse.from_esri_code(54030)  # Robinson projection from esri code
    # tocrs_proj4 = tocrs.to_proj4()
    # fromproj = pyproj.Proj(fromcrs_proj4)
    # toproj = pyproj.Proj(tocrs_proj4)
    # lng, lat = 406740.98500512, 6201332.77322646  # Williamsburg, Virginia :)
    # print(pyproj.transform(toproj, fromproj, lng, lat))
    # df['x_from'] = df['x_from'].astype("float32")
    #


    # 3
    file.write('------------------------------------\n3) Форматирование столбца avg_speed\n')
    file.write('------------------------------------\n')
    avg_speed_list = df['avg_speed'].str.split(',')

    wrong_avg_speed_values = []
    wrong_values_index = []

    for i, x in enumerate(avg_speed_list):
        for item in x:
            value = item.split('=>')[1]
            time = item.split('=>')[0]
            if int(time) not in range(0, 86401):
                wrong_avg_speed_values.append(value)
                print('time not right')

            if value == 'null':
                wrong_avg_speed_values.append(value)
                wrong_values_index.append(i)

            elif value == 'Infinity':
                wrong_avg_speed_values.append(value)
                wrong_values_index.append(i)

            elif float(value) < 0 or float(value) > 200:
                wrong_avg_speed_values.append(value)
                wrong_values_index.append(i)

    file.write("Неверные значения (null, infinity, <0, >200): " + str(wrong_avg_speed_values) + "\n")

    file.write("Их индексы:" + str(wrong_values_index) + "\n")

    # 4
    file.write('------------------------------------\n4) Форматирование столбца intensity\n')
    file.write('------------------------------------\n')
    intensity_list = df['intensity'].str.split(',')

    wrong_intensity_values = []
    wrong_values_index.clear()

    for i, x in enumerate(intensity_list):
        for item in x:
            value = item.split('=>')[1]
            time = item.split('=>')[0]
            if int(time) not in range(0, 86401):
                wrong_intensity_values.append(value)
                wrong_values_index.append(i)

            if value == 'null':
                wrong_intensity_values.append(value)
                wrong_values_index.append(i)

            elif value == 'Infinity':
                wrong_intensity_values.append(value)
                wrong_values_index.append(i)

    file.write("Неверные значения (null, infinity, <0, >200, time < 0 or time > 86400: " + str(wrong_intensity_values) + "\n")

    file.write("Их индексы: " + str(wrong_values_index) + "\n")


    # 5
    file.write('------------------------------------\n5) Форматирование столбца calendar\n')
    file.write('------------------------------------\n')
    count = 0  # кол-во различных форматов, не удовлетворяющих нужному формату
    file.write("Нужный формат: 2020-07-09\n")
    file.write("Неверные форматы: ")
    for i in df.calendar:
        if not re.match(r'\d{4}-\d{2}-\d{2}', i):
            file.write(str(i) + "\n")  # форматы
            count += 1
    file.write("Количество неверных форматов до преобразования: " + str(count) + "\n")  # кол-во неверных форматов

    regex = ['(\d{2})\.(\d{2})\.(\d{4})', '(\d{2})-(\d{2})-(\d{4})']  # регулярные выражения для дальнейшей замены
    df['calendar'].replace(to_replace=regex, value=r'\3-\2-\1', regex=True, inplace=True)
    count = 0

    for i in df.calendar:
        if not re.match(r'\d{4}-\d{2}-\d{2}', i):
            print(i)
            count += 1
    file.write("Количество неверных форматов после преобразования: " + str(count) + "\n")

    df.calendar = pd.to_datetime(df.calendar, format='%Y-%d-%m')

    file.write('------------------------------------\n')
    file.close()


if __name__ == "__main__":
    main()
