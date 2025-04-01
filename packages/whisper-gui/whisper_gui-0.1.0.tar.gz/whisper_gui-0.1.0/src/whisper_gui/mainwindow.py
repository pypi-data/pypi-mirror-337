# This Python file uses the following encoding: utf-8
import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QSettings, QPoint, QSize, QProcess

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from .ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.process = None

        # Enable drag & drop
        self.setAcceptDrops(True)

        self.loadSettings()

        # set self encoding to utf-8 on non-windows and cp1252 on windows
        if sys.platform != "win32":
            self.encoding = "utf-8"
        else:
            self.encoding = "cp1252"

    def closeEvent(self, event):
        self.saveSettings()
        if self.process:
            self.process.terminate()
            self.process.waitForFinished()
        event.accept()

    def loadSettings(self):
        self.settings = QSettings("frank_bergmann", "whisper_gui")
        self.ui.txtAudio.setText(self.settings.value("audio_file", ""))
        self.ui.txtVideo.setText(self.settings.value("video_file", ""))
        self.ui.cmbLanguage.setCurrentText(self.settings.value("language", "German"))
        self.ui.cmbModel.setCurrentText(self.settings.value("model", "tiny"))
        self.ui.txtOutputDir.setText(self.settings.value("output_dir", ""))
        # load position and size
        self.move(self.settings.value("pos", QPoint(200, 200)))
        self.resize(self.settings.value("size", QSize(800, 600)))

    def saveSettings(self):
        self.settings.setValue("audio_file", self.ui.txtAudio.text())
        self.settings.setValue("video_file", self.ui.txtVideo.text())
        self.settings.setValue("language", self.ui.cmbLanguage.currentText())
        self.settings.setValue("model", self.ui.cmbModel.currentText())
        self.settings.setValue("output_dir", self.ui.txtOutputDir.text())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())
        self.settings.sync()

    def slotTerminate(self):
        print("Terminate")
        self.process.terminate()
        self.process.waitForFinished()
        self.ui.cmdTerminate.setEnabled(False)
        self.ui.cmdTranscribe.setEnabled(True)
        self.ui.cmdConvertAudio.setEnabled(True)

    def slotOpen(self, file_name=None):
        if not file_name:
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Open File",
                "",
                "Video Files (*.mp4 *.avi *.mkv *.mov);;Audio Files (*.mp3 *.wav *.m4a *.ogg);;All Files (*.*)"
            )
        if file_name:
            if file_name.endswith(".mp4") or file_name.endswith(".avi") or file_name.endswith(".mkv") or file_name.endswith(".mov"):
                self.ui.txtVideo.setText(file_name)
            elif file_name.endswith(".mp3") or file_name.endswith(".wav") or file_name.endswith(".m4a") or file_name.endswith(".ogg"):
                self.ui.txtAudio.setText(file_name)
        print("Open")

    def slotOpenOutputDir(self):
        print("Open Output Dir")
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Open Output Dir",
            self.ui.txtOutputDir.text()
        )
        if output_dir:
            self.ui.txtOutputDir.setText(output_dir)

    def slotSave(self):
        print("Save")

    def slotQuit(self):
        print("Quit")

    def slotOpenAudio(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            self.ui.txtAudio.text(),
            "Audio Files (*.mp3 *.wav *.m4a *.ogg);;All Files (*.*)"
        )
        if file_name:
            self.ui.txtAudio.setText(file_name)
            self.ui.txtVideo.setText("")

    def slotOpenVideo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            self.ui.txtVideo.text(),
            "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*.*)"
        )
        if file_name:
            self.ui.txtVideo.setText(file_name)
            self.ui.txtAudio.setText("")

    def slotConvertAudio(self):
        print("Convert Audio")

        # get the video file
        video_file = self.ui.txtVideo.text()
        if not video_file:
            QMessageBox.warning(self, "Error", "Please select a video file first.")
            return
        
        # create an audio mp3 using ffmpeg
        # target file is original file with different extension
        base_name = video_file[:video_file.rfind(".")] 
        audio_file = base_name + ".mp3"

        # check if audio file already exists
        while os.path.exists(audio_file):
            audio_file = base_name + "_" + str(i) + ".mp3"
            i += 1

        print(f"Converting {video_file} to {audio_file}")

        # run ffmpeg using qprocess
        self.process = QProcess()
        self.process.start("ffmpeg", ["-i", video_file, "-q:a", "0", audio_file])
        self.converted_audio_file = audio_file
        self.process.finished.connect(self.slotConvertAudioFinished)
        self.ui.cmdConvertAudio.setEnabled(False)
        self.ui.cmdTerminate.setEnabled(True)

        self.ui.txtOutput.clear()
        self.ui.txtOutput.appendPlainText("Converting audio...")
        self.ui.txtOutput.appendPlainText("ffmpeg -i " + video_file + " -q:a 0 " + audio_file)

    def slotTranscribe(self):
        print("Transcribe")
        audio_file = self.ui.txtAudio.text()
        if not audio_file:
            QMessageBox.warning(self, "Error", "Please select an audio file first or convert a video file first.")
            return
        
        # run whisper
        self.process = QProcess()

        args = [
            "--language", self.ui.cmbLanguage.currentText(),
            "--model", self.ui.cmbModel.currentText(),
            "--output_format", "txt",
        ]
        if self.ui.txtOutputDir.text():
            args.append("--output_dir")
            args.append(self.ui.txtOutputDir.text())
        args.append(audio_file)

        self.process.start("whisper", args)

        self.ui.txtOutput.clear()
        self.ui.txtOutput.appendPlainText("Transcribing...")
        # add commandline to output
        self.ui.txtOutput.appendPlainText("whisper " + " ".join(args))
        
        self.process.finished.connect(self.slotTranscribeFinished)
        # Connect process signals for progress info
        self.process.readyReadStandardOutput.connect(self.slotTranscribeProgress)
        self.process.readyReadStandardError.connect(self.slotTranscribeError)
        self.ui.cmdTranscribe.setEnabled(False)
        self.ui.cmdTerminate.setEnabled(True)
    
    def slotTranscribeProgress(self):
        print("Transcribe Progress")
        output = self.process.readAllStandardOutput().data().decode(
            encoding=self.encoding,
            errors='replace'
        )
        self.ui.txtOutput.appendPlainText(output)

    def slotTranscribeError(self):
        print("Transcribe Error")
        output = self.process.readAllStandardError().data().decode(
            encoding=self.encoding,
            errors='replace'
        )
        self.ui.txtOutput.appendPlainText(output)

    def slotConvertAudioFinished(self):
        print("Convert Audio Finished")
        self.ui.txtAudio.setText(self.converted_audio_file)
        self.ui.cmdConvertAudio.setEnabled(True)
        self.process = None

    def slotTranscribeFinished(self):
        print("Transcribe Finished")
        output = self.process.readAll().data().decode(
            encoding='utf-8',
            errors='replace'
        )
        self.ui.txtOutput.appendPlainText(output)
        self.ui.cmdTranscribe.setEnabled(True)
        self.process = None

    def dragEnterEvent(self, event):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Handle drag move events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle drop events."""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            # Use the first file dropped
            self.slotOpen(files[0])
            event.acceptProposedAction()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    if len(sys.argv) > 1:
        window.slotOpen(sys.argv[1])
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
