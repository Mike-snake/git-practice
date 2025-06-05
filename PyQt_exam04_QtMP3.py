import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import os

form_class = uic.loadUiType("QtMP3.ui")[0]

class ExampleApp(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mediaPlayer = QMediaPlayer() # QMediaPlayer 객체 생성
        self.current_media_path = None # 현재 재생 중인 미디어 파일 경로

        # --- UI 위젯 연결 (파이큐티의 버턴을 서로 연결/인공지능 코드/교수님 코드랑 다른부분)
        self.fileNameLabel = self.findChild(QLabel, 'fileNameLabel')
        self.openFileButton = self.findChild(QPushButton, 'openFileButton')
        self.playMusicButton = self.findChild(QPushButton, 'playMusicButton')
        self.pauseplayButton = self.findChild(QPushButton, 'pauseplayButton')
        self.stopplayButton = self.findChild(QPushButton, 'stopplayButton')

        # 실질적인 액션이 이루어 지는 코드부분
        self.openFileButton.clicked.connect(self.open_file)             # 파일오픈 버튼
        self.playMusicButton.clicked.connect(self.play_music)           # 플레이 버튼
        self.pauseplayButton.clicked.connect(self.toggle_play_pause)    # 일시정지 버튼
        self.stopplayButton.clicked.connect(self.stop_play_music)       # 스탑 버튼

        # self.progressBar.setEnabled(False)  # 처음에는 진행바 비활성화
        # self.progressBar.sliderMoved.connect(self.set_position)  # 슬라이더 이동 시 재생 위치 변경

        # 미디어 플레이어의 상태 변화 감지 (재생 버튼 활성화/비활성화 제어)
        # self.mediaPlayer.setVolume(self.volumeSlider.value())

        # self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        # self.mediaPlayer.positionChanged.connect(self.position_changed)
        # self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.mediaStatusChanged.connect(self.media_status_changed)  # 미디어 상태 변화 감지



    def open_file(self):
        # MP3 파일 열기 다이얼로그
        file_path, _ = QFileDialog.getOpenFileName(self, "MP3 파일 선택", "", "MP3 Files (*.mp3);;All Files (*)")

        if file_path:
            self.current_media_path = file_path
            # 파일 이름을 레이블에 표시
            self.fileNameLabel.setText(os.path.basename(file_path))

            # 선택된 파일을 미디어 플레이어에 설정
            content = QMediaContent(QUrl.fromLocalFile(file_path))
            self.mediaPlayer.setMedia(content)

            # self.playMusicButton.setText("▶")  # 새 파일 로드 시 재생 버튼 텍스트 초기화
            # self.playMusicButton.setEnabled(True)  # 재생/일시정지 버튼 활성화
            # self.endplayButton.setEnabled(True)  # 정지 버튼 활성화
            # self.progressBar.setEnabled(True)  # 진행바 활성화
            # self.mediaPlayer.play()  # 파일을 열면 자동으로 재생 시작


            # 파일이 로드되면 재생 버튼 활성화 (재생 준비 상태일 때 활성화 되도록 media_status_changed에서 처리)
            # self.playButton.setEnabled(True)
            # self.endplayButton.setEnabled(True)
            # self.playButton.setText("▶")  # 혹시 재생 중이더라도 텍스트는 '재생'으로 초기화
            # self.endplayButton.setText("■")
            print(f"선택된 파일: {self.current_media_path}")

    def play_music(self):

        # 파일이 로드되어 있고, 현재 재생 중이 아니면 재생 시작
        if self.current_media_path and self.mediaPlayer.state() != QMediaPlayer.PlayingState:
            self.mediaPlayer.play()
            self.playMusicButton.setText("재생 중...")  # 재생 시작을 알리는 텍스트
            print("음악 재생 시작")
        elif self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            print("이미 재생 중입니다.")
        else:
            print("재생할 파일이 선택되지 않았습니다.")

    def stop_play_music(self):
        self.mediaPlayer.stop()

    # def set_volume(self, volume):
    #     self.mediaPlayer.setVolume(volume)


    def toggle_play_pause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()




    def position_changed(self, position):
        # 재생 위치가 변경될 때마다 진행바와 현재 시간 업데이트
        self.progressBar.setValue(position)
        self.currentTimeLabel.setText(self.format_time(position))

    def duration_changed(self, duration):
        # 미디어의 총 길이가 변경될 때마다 진행바의 최대값과 총 시간 업데이트
        self.progressBar.setRange(0, duration)
        self.totalTimeLabel.setText(self.format_time(duration))


    def format_time(self, milliseconds):
        # 밀리초를 "분:초" 형식으로 변환
        total_seconds = int(milliseconds / 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"



    def media_state_changed(self, state):
        if self.current_media_path is None: # 파일이 로드되지 않았으면 아무것도 하지 않음
            self.playMusicButton.setEnabled(False)
            self.pauseplayButton.setEnabled(False)
            self.stopplayButton.setEnabled(False)
            return

        if state == QMediaPlayer.PlayingState:
            self.playPauseButton.setText("일시정지")
            self.stopButton.setEnabled(True)
        elif state == QMediaPlayer.PausedState:
            self.playPauseButton.setText("재생")
            self.stopButton.setEnabled(True)
        else: # QMediaPlayer.StoppedState
            self.playPauseButton.setText("재생")
            self.stopButton.setEnabled(False)
            # 재생이 끝나면 진행바와 시간 초기화
            self.progressBar.setValue(0)
            self.currentTimeLabel.setText("00:00")






    def media_status_changed(self, status):
        # 미디어 플레이어의 상태에 따라 재생 버튼의 활성화 여부와 텍스트를 제어
        if status == QMediaPlayer.MediaStatus.NoMedia:
            # 미디어가 없으면 재생 버튼 비활성화
            self.playButton.setEnabled(False)
            self.playButton.setText("재생")
        elif status == QMediaPlayer.MediaStatus.LoadedMedia:
            # 미디어가 로드되면 재생 버튼 활성화
            self.playMusicButton.setEnabled(True)
            self.playMusicButton.setText("▶")
            self.pauseplayButton.setEnabled(False)
            self.pauseplayButton.setText("❚❚")
            self.stopplayButton.setEnabled(False)
            self.stopplayButton.setText("■")

        elif status == QMediaPlayer.MediaStatus.EndOfMedia:
            # 재생이 끝나면 버튼 텍스트를 '재생'으로 바꾸고 비활성화
            self.playButton.setText("재생")
            self.playButton.setEnabled(False) # 다음 파일을 선택해야 다시 재생 가능
            print("재생이 종료되었습니다.")
        # 다른 상태들 (BufferingMedia, LoadingMedia, InvalidMedia 등)은 필요에 따라 추가 처리 가능


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ExampleApp()
    main_window.show()
    sys.exit(app.exec_())