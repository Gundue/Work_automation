import glob

import numpy as np
import pandas as pd
from scipy.stats import gmean, gstd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def cal_figures(files, sensor, count=1):
    # writer = pd.ExcelWriter(f"end/{sensor}.xlsx", engine='xlsxwriter')
    finish = pd.DataFrame()
    for file in files:
        count = 1
        df = pd.read_csv(file)
        name = file.split("\\")[1]
        name = name.split('.')[0]
        df['date'] = df['date'].replace(':', ' ', regex=True)
        df['date'] = df['date'].str.split(' ').str[0] + " " + df['date'].str.split(' ').str[1].replace('24', '00',
                                                                                                       regex=True)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')

        first = df.query('"2022-11-07 00:00:00" < date < "2022-11-12"')
        second = df.query('"2022-11-14 00:00:00" < date < "2022-11-19"')
        third = df.query('"2022-11-21 00:00:00" < date < "2022-11-26"')
        fourth = df.query('"2022-11-28 00:00:00" < date < "2022-12-03"')

        arr = [first, second, third, fourth]

        tuples = [(parsing[name], str(week) + "주차") for week in range(1, 5)]
        index = pd.MultiIndex.from_tuples(tuples, names=['school', 'week'])

        weekList = []

        for i in arr:
            weekList.append([round(i[sensor].dropna().mean(), 1), round(i[sensor].dropna().std(), 1),
                 round(gmean(i[sensor].dropna()), 1), round(gstd(i[sensor].dropna()), 1), round(np.median(i[sensor].dropna()),1)])

        end = pd.DataFrame(weekList, columns=['표본 평균', '표본 표준편차', '기하 평균', '기하 표준편차', '중위수'], index=index)
        finish = finish.append(end)

    # writer.save()
    return finish


if __name__ == '__main__':
    # 디렉토리 내의 모든 csv 파일 가져오기
    files = [path for path in glob.glob(f'data/*.csv', recursive=True)]

    figure_df = cal_figures(files, 'pm10')

    figure_df.to_csv('result.csv', encoding='cp949')
