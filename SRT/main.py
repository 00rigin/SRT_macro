from SRT import SRT
from SRT.train import SRTTrain
import time as tt
import random as rd
import sys
import os
from datetime import datetime, timedelta

ID = '아이디/회원번호'
PASSWORD = '비밀번호'
DEPARTURE = '출발지'
ARRIVAL = '도착지'
TARGET_DATE = '20241220'
START_TIME = '170000'
LIMIT_TIME = '200000'

def play_sound():
    sound_file = '../Sound/sound1.mp3'
    os.system(f'afplay {sound_file}')

def search_possible_train(srt, dep, arr, date, time, time_limit) -> list[SRTTrain]:

    search_message = ["[SRT] Searching.","[SRT] Searching..","[SRT] Searching...","[SRT] Searching....","[SRT] Searching....."]
    index = 0

    start_time = datetime.now()
    last_pause = None
    pause_duration = 55
    work_duration = 180  # 3분

    while True:

        # 3분마다 1분 쉬기
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time % work_duration < pause_duration and last_pause != int(elapsed_time / work_duration):
            sys.stdout.write("\r" + str(pause_duration) + "초간 쉬는 중...")
            sys.stdout.flush()
            last_pause = int(elapsed_time / work_duration)
            tt.sleep(pause_duration)
            continue

        tt.sleep(rd.uniform(0.2, 2.5)) #랜덤 타임 휴식 (없으면 밴당함 ㅠ)
        available_train = srt.search_train(dep, arr, date, time, time_limit, True)

        sys.stdout.write("\r" + search_message[index])
        sys.stdout.flush()
        index = (index + 1) % len(search_message)

        if len(available_train) > 0:
            return available_train



def reserve_train_until_success(srt,
                                dep: str,
                                arr: str,
                                date: str | None = None,
                                time: str | None = None,
                                time_limit: str | None = None) -> SRTTrain:
    available_trains = search_possible_train(srt, dep, arr, date, time, time_limit)

    return available_trains[0]


if __name__ == '__main__':
    srt = SRT(ID, PASSWORD)  # 인스턴스 생성
    srt.login()
    dep = DEPARTURE
    arr = ARRIVAL
    date = TARGET_DATE
    time = START_TIME
    limit = LIMIT_TIME

    first_available_train = reserve_train_until_success(srt, dep, arr, date, time, limit)


    reservation = srt.reserve(first_available_train)

    play_sound()
    print("결재를 완료해주세요")

