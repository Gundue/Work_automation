from datetime import datetime, timedelta
import os
import pandas as pd

place = pd.read_excel("list.xlsx")
folder_path = 'data'
missing_data = []

all_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        all_files.append(file_path)


def calculate_rows(start_date_str, end_date_str):
    # 시작일과 종료일을 datetime 형식으로 변환
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')

    # 1시간 간격으로 루프를 돌며 행 계산 (월요일(0) ~ 금요일(4)까지만)
    current_date = start_date
    row_count = 0
    while current_date <= end_date:
        # if current_date.weekday() < 5:  # 0은 월요일, 4는 금요일
        row_count += 1
        current_date += timedelta(hours=1)

    return row_count


def diff_data(start_date_str, end_date_str, t_data):
    # 시작일과 종료일을 datetime 형식으로 변환
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    start_date = start_date.replace(minute=00, second=00)
    end_date = end_date.replace(minute=00, second=00)
    # 1시간 간격으로 날짜 및 시간 생성
    date_list = pd.date_range(start=start_date, end=end_date, freq='1H')

    # 데이터프레임 생성
    # all_data = pd.DataFrame({'all_data': date_list})
    missing_data = date_list.difference(t_data)
    missing_data = missing_data.to_frame()
    missing_data.columns = ['date']
    return missing_data



for excel_file in all_files:
    df = pd.read_excel(excel_file)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M')
    t_data = df['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H:%M:%S'))
    t_data = t_data.drop_duplicates()
    rows = t_data.count()

    # 시작일과 종료일을 지정
    start_date_str = str(place[place['place'] == df['i_place'][0]]['start_date'].iloc[0])
    end_date_str = str(place[place['place'] == df['i_place'][0]]['end_date'].iloc[0])
    # 함수 호출하여 결과 출력
    result = calculate_rows(start_date_str, end_date_str)

    file_name = os.path.basename(excel_file)
    file_name = file_name.replace(".xlsx", "")

    if(result != rows):
        print("fail")
        print(excel_file)
        print("기준 : ", result, "데이터 : ", rows)
        missing_data.append(file_name)
        diff_data(start_date_str, end_date_str, t_data).to_csv(f'result/{file_name}.csv', encoding='euc-kr', index=False)
    else:
        print("success")
        print("기준 : ", result, "데이터 : ", rows)
        print(file_name)


end = pd.DataFrame(missing_data)
end.columns = ['missing_list']
end.to_csv('누락 목록.csv', encoding='euc-kr', index=False)