import pyautogui as pg
import os

# 앱 실행
os.startfile('.lnk')
pg.sleep(30)
# 전체화면 변경
print('f11')
pg.press('f11')

# 30개반 이미지
for i in range(1, 31):
    print(i)
    # 이미지를 못 찾을 시 아래로 스크롤
    while pg.locateOnScreen(f'ban/{i}.PNG', confidence=0.8) is None:
        pg.scroll(-100)
        pg.sleep(3)
        if pg.locateOnScreen(f'ban/{i}.PNG', confidence=0.8) is not None:
            break

    ban = pg.locateOnScreen(f'ban/{i}.PNG', confidence=0.8)
    print(ban)
    pg.moveTo(ban)
    pg.click()
    pg.sleep(5)

    # 그래프 줌 아웃하여 24시간 그래프 보기
    gragh = pg.locateOnScreen('year.PNG')
    pg.moveTo(gragh)
    pg.keyDown('ctrl')
    pg.mouseDown(button='left')

    for j in range(20):
        pg.scroll(-2000)

    pg.keyUp('ctrl')
    pg.mouseUp(button='left')
    
    # 캡처 버튼 클릭
    capture = pg.locateOnScreen('capture.PNG')
    pg.moveTo(capture)
    pg.click()
    pg.hotkey('ctrl', 'shift', 's')

    pg.sleep(5)

    # 뒤로가기 버튼 클릭
    location = pg.locateOnScreen('found.PNG')
    pg.moveTo(location)
    pg.click()

    pg.sleep(5)





















