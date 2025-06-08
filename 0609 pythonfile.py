import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QListWidget, QFileDialog, QStyle, QLabel)
from PyQt6.QtCore import Qt
from pathlib import Path


class MP3Player(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple MP3 Player")
        self.setGeometry(100, 100, 400, 500)  # x, y, width, height

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create Add Files button
        add_button = QPushButton("Add MP3 Files")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_button.clicked.connect(self.add_files)
        layout.addWidget(add_button)

        # Create playlist label
        playlist_label = QLabel("Playlist:")
        playlist_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(playlist_label)

        # Create playlist widget
        self.playlist = QListWidget()
        self.playlist.setStyleSheet("""
            QListWidget {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #ebebeb;
            }
        """)
        self.playlist.itemDoubleClicked.connect(self.play_selected)
        layout.addWidget(self.playlist)

        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select MP3 Files",
            str(Path.home()),
            "MP3 Files (*.mp3);;All Files (*.*)"
        )

        for file_path in files:
            # Add only the filename to display
            file_name = Path(file_path).name
            # Store the full path as item data
            item = self.playlist.addItem(file_name)
            # Store the full path as item data
            last_item = self.playlist.item(self.playlist.count() - 1)
            last_item.setData(Qt.ItemDataRole.UserRole, file_path)

    def play_selected(self, item):
        # Get the full file path from the item data
        file_path = item.data(Qt.ItemDataRole.UserRole)
        # For now, just print the file path
        print(f"Playing: {file_path}")
        # 실제 재생 기능은 나중에 구현할 예정입니다.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MP3Player()
    player.show()
    sys.exit(app.exec())