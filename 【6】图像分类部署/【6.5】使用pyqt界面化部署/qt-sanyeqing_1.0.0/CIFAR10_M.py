import csv
import json
import os
import onnxruntime
import torch

from PyQt6.QtWidgets import (QWidget,
                             QGridLayout, QApplication, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem)

from PyQt6.QtWidgets import *
import sys

from shexiang import process_frame, load_model_and_labels, generate_video
from sanye_pred_shen import shenfen_classify
from sanye_pred_chan import chan_classify
from sanye_pred_zhe import zhechan_classify, get_prediction_img_zidi, get_prediction_img_zidi_onnx
import cv2
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap, QPen, QPainter, QColor, QFont, QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class CustomCameraWindow(QDialog):
    def __init__(self, capture, model, class_indict, parent=None):
        super().__init__(parent)
        self.setWindowTitle('自定义摄像实时预测')
        # 增加状态变量
        self.is_recognition = False
        # 使用给定的模型和标签
        self.model = model
        self.class_indict = class_indict

        # 在现有的窗口标志基础上添加最小化和最大化按钮
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        # 定义 QLabel 作为摄像头的视图显示器
        self.camera_label = QLabel(self)

        # 创建一个 QVBoxLayout 并将 camera_label 添加进去
        self.layout = QVBoxLayout()

        # 创建一个 QLabel 来显示消息
        self.message_label = QLabel(
            "开始识别后，按 'a' 键启动省份识别模型；  按 ’s‘ 键启动浙产识别模型；  按 ‘d’ 键启动产地识别模型", self)

        # 将 message_label 添加到布局中
        self.layout.addWidget(self.message_label)

        # 创建两个新的 QPushButton 实例
        self.start_button_zidi = QPushButton('实时识别')
        self.stop_button_zidi = QPushButton('结束识别')

        # 设置按钮的宽度和样式
        self.start_button_zidi.setFixedWidth(100)
        self.stop_button_zidi.setFixedWidth(100)
        self.start_button_zidi.setStyleSheet('background-color: green; color: white;')
        self.stop_button_zidi.setStyleSheet('background-color: red; color: white;')

        # 创建一个 QHBoxLayout 并将两个按钮添加进去
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button_zidi)
        self.button_layout.addWidget(self.stop_button_zidi)

        # 将 QHBoxLayout 和 QLabel 添加到 QVBoxLayout 中
        self.layout.addWidget(self.camera_label)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        # 连接 QPushButton 的 clicked 信号到新的槽函数

        self.start_button_zidi.clicked.connect(self.start_recognition_zidi)
        self.stop_button_zidi.clicked.connect(self.stop_recognition_zidi)

        # 创建 QTimer 对象
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_camera_zidi)

        # 使用给定的 cv2.VideoCapture 实例
        self.capture = capture

        # 启动 QTimer
        self.timer.start(30)

        # 重写 keyPressEvent 方法

    def keyPressEvent(self, event):
        try:
            # '1'，则切换到模型1和标签1
            if event.key() == Qt.Key.Key_A:
                self.model, self.class_indict = load_model_and_labels('./model_cpu_97.18.onnx',
                                                                      './class_indices_5.json')

            # '2'，则切换到模型2和标签2
            elif event.key() == Qt.Key.Key_S:
                self.model, self.class_indict = load_model_and_labels('./model_cpu_3.onnx',
                                                                      './class_indices_2.json')

            # '3'，则切换到模型3和标签3
            elif event.key() == Qt.Key.Key_D:
                self.model, self.class_indict = load_model_and_labels('./model_cpu_11.onnx',
                                                                      './class_indices_10.json')
        except Exception as e:
            print(f"Error: {e}")

    def display_camera_zidi(self):
        # 使用 opencv 读取摄像头的帧
        ret, frame = self.capture.read()

        # 转换 opencv 帧的颜色空间为 RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 如果处于识别状态，进行识别
        if self.is_recognition:
            try:
                # 调用你的识别代码
                frame = process_frame(frame, 11, self.model, self.class_indict)
            except Exception as e:
                # 显示错误消息
                QMessageBox.critical(self, "错误提示", str(e))
                self.is_recognition = False
                return
        # 从 opencv 帧创建 QImage 对象
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)

        # 从 QImage 创建 QPixmap 对象并设置到 QLabel
        self.camera_label.setPixmap(QPixmap.fromImage(image))

    def start_recognition_zidi(self):
        # 实现开始识别的功能
        self.is_recognition = True

    def stop_recognition_zidi(self):
        # 实现结束识别的功能
        self.is_recognition = False

    def closeEvent(self, event):
        # 停止 QTimer
        self.timer.stop()

        # 释放摄像头资源
        self.capture.release()

        # 删除 camera_window 实例
        self.parent().camera_windows.remove(self)


class CameraWindow(QDialog):
    def __init__(self, capture, parent=None):
        super().__init__(parent)

        self.setWindowTitle('摄像实时预测')

        # 增加状态变量
        self.is_recognition = False
        self.ort_session = ''
        self.labels = ''
        # 在现有的窗口标志基础上添加最小化和最大化按钮
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        # 定义 QLabel 作为摄像头的视图显示器
        self.camera_label = QLabel(self)

        # 创建一个 QVBoxLayout 并将 camera_label 添加进去
        self.layout = QVBoxLayout()

        # 创建新的 QPushButton 实例
        self.start_button = QPushButton('实时识别')
        self.stop_button = QPushButton('结束识别')

        # 连接 QPushButton 的 clicked 信号到新的槽函数
        self.start_button.clicked.connect(self.start_recognition)
        self.stop_button.clicked.connect(self.stop_recognition)

        # 设置按钮的宽度和样式
        self.start_button.setFixedWidth(100)
        self.stop_button.setFixedWidth(100)
        self.start_button.setStyleSheet('background-color: green; color: white;')

        self.stop_button.setStyleSheet('background-color: red; color: white;')

        # 创建一个 QLabel 来显示消息
        self.message_label = QLabel(
            "开始识别后，按 'a' 键启动省份识别模型；  按 ’s‘ 键启动浙产识别模型；  按 ‘d’ 键启动产地识别模型",
            self)

        # 将 message_label 添加到布局中
        self.layout.addWidget(self.message_label)

        # 创建一个 QHBoxLayout 并将两个按钮添加进去
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        # 将 QHBoxLayout 和 QLabel 添加到 QVBoxLayout 中
        self.layout.addWidget(self.camera_label)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        # 创建 QTimer 对象
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_camera)

        # 使用给定的 cv2.VideoCapture 实例
        self.capture = capture

        # 启动 QTimer
        self.timer.start(30)

        # 重写 keyPressEvent 方法

    def keyPressEvent(self, event):
        try:
            # '1'，则切换到模型1和标签1
            if event.key() == Qt.Key.Key_A:
                self.ort_session, self.labels = load_model_and_labels('./model_cpu_97.18.onnx',
                                                                      './class_indices_5.json')

            # '2'，则切换到模型2和标签2
            elif event.key() == Qt.Key.Key_S:
                self.ort_session, self.labels = load_model_and_labels('./model_cpu_3.onnx',
                                                                      './class_indices_2.json')

            # '3'，则切换到模型3和标签3
            elif event.key() == Qt.Key.Key_D:
                self.ort_session, self.labels = load_model_and_labels('./model_cpu_11.onnx',
                                                                      './class_indices_10.json')
        except Exception as e:
            print(f"Error: {e}")

    def display_camera(self):
        # 使用 opencv 读取摄像头的帧
        ret, frame = self.capture.read()

        # 转换 opencv 帧的颜色空间为 RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 如果处于识别状态，进行识别
        if self.is_recognition:
            # 调用你的识别代码
            frame = process_frame(frame, 11, self.ort_session, self.labels)

        # 从 opencv 帧创建 QImage 对象
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)

        # 从 QImage 创建 QPixmap 对象并设置到 QLabel
        self.camera_label.setPixmap(QPixmap.fromImage(image))

    def start_recognition(self):
        # 实现开始识别的功能
        self.is_recognition = True
        # 加载初始模型和标签
        self.ort_session, self.labels = load_model_and_labels('./model_cpu_3.onnx', './class_indices_2.json')

    def stop_recognition(self):
        # 实现结束识别的功能
        self.is_recognition = False

    def closeEvent(self, event):
        # 停止 QTimer
        self.timer.stop()

        # 释放摄像头资源
        self.capture.release()

        # 删除 camera_window 实例
        self.parent().camera_windows.remove(self)


class Tab(QWidget):
    def __init__(self, classify_func, model_path, json_path, parent=None, camera_windows=None):
        super().__init__(parent)

        # 创建一个变量来跟踪拍照识别窗口的状态
        self.player = None
        self.snapshot_dialog = None

        # 定义 QLabel 作为摄像头的视图显示器
        self.class_indict = None
        self.model = None
        self.model_path = model_path
        self.json_path = json_path
        self.camera_label = QLabel(self)
        self.capture = None
        self.camera_windows = camera_windows if camera_windows is not None else []
        # 创建一个 cv2.VideoCapture 实例
        self.camera_capture = None

        self.fname = None
        self.pixmap = None
        self.batch_processing = False
        self.camera = None

        self.layout = QGridLayout(self)
        self.label_image = QLabel(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.label_image)
        self.table_predict_result = QTableWidget(0, 2, self)
        self.button_search_image = QPushButton('选择图片', self)
        self.button_run = QPushButton('运行', self)
        self.button_batch_process = QPushButton('批量处理', self)
        self.button_open_camera = QPushButton('打开摄像头', self)
        self.button_snapshot = QPushButton('拍照识别', self)
        self.button_submit_video = QPushButton('提交视频', self)

        self.init_tab(self.layout, self.scroll_area, self.table_predict_result, self.button_search_image,
                      self.button_run, self.button_batch_process, self.button_open_camera, self.button_snapshot,
                      self.button_submit_video)
        self.button_search_image.clicked.connect(lambda: self.openimage())
        self.button_run.clicked.connect(lambda: self.dan_run(classify_func))
        self.button_batch_process.clicked.connect(lambda: self.batch_process(classify_func))
        self.button_open_camera.clicked.connect(lambda: self.open_camera())
        self.button_snapshot.clicked.connect(self.snapshot_recognition)
        self.button_submit_video.clicked.connect(self.submit_video)

        self.setLayout(self.layout)

    def init_tab(self, layout, scroll_area, table_predict_result, button_search_image, button_run,
                 button_batch_process, button_open_camera, button_snapshot, button_submit_video):
        layout.addWidget(scroll_area, 1, 1, 6, 2)
        layout.addWidget(button_search_image, 1, 3, 1, 1)
        layout.addWidget(button_run, 2, 3, 1, 1)
        layout.addWidget(button_batch_process, 3, 3, 1, 1)
        layout.addWidget(table_predict_result, 8, 1, 1, 4)
        layout.addWidget(button_open_camera, 4, 3, 1, 1)  # 改变这里的数字可以改变按钮的位置
        layout.addWidget(button_snapshot, 5, 3, 1, 1)
        layout.addWidget(button_submit_video, 6, 3, 1, 1)
        table_predict_result.setMinimumHeight(100)
        table_predict_result.setMaximumHeight(800)
        table_predict_result.setHorizontalHeaderLabels(["预测类别", "置信度"])
        layout.setRowStretch(1, 6)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        # layout.setRowStretch(5, 1)
        # layout.setRowStretch(6, 1)
        # layout.setRowStretch(7, 1)
        # layout.setRowStretch(8, 1)

        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)

    def submit_video(self):
        try:
            # 弹出一个文件选择对话框来选择视频文件
            fname, _ = QFileDialog.getOpenFileName(self, '选择视频', '.', 'Video files(*.mp4 *.avi);;All Files(*)')

            if fname:
                self.model, self.class_indict = load_model_and_labels(self.model_path, self.json_path)
                # 使用你的模型对视频进行预测，并将预测结果保存到新的视频文件
                output_fname = generate_video(fname, 11, self.model, self.class_indict)
                # 弹出一个消息框提示视频处理成功
                QMessageBox.information(self, "提示", "处理后的视频保存成功")
                # # 使用一个播放器显示预测结果视频
                # self.player = QMediaPlayer(self)
                # self.player.setMedia(QMediaContent(QUrl.fromLocalFile(output_fname)))
                # video_widget = QVideoWidget(self)
                #
                # # 设置视频窗口的最小和最大尺寸
                # video_widget.setMinimumSize(100, 100)  # 设置最小尺寸为 100x100 像素
                # video_widget.setMaximumSize(500, 500)  # 设置最大尺寸为 500x500 像素
                #
                # # 使视频窗口有一个最小化按钮和一个最大化/全屏按钮
                # video_widget.setWindowFlags(
                #     Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
                #
                # self.player.setVideoOutput(video_widget)
                # self.layout.addWidget(video_widget, 1, 1, 6, 2)
                # self.player.play()
                # video_widget.show()  # 确保视频窗口是可见的
        except Exception as e:
            # 如果出现任何错误，显示一个错误消息框
            QMessageBox.critical(self, "Error", str(e))

    def snapshot_recognition(self):
        # 检查摄像头是否已经打开
        if not self.camera_capture or not self.camera_capture.isOpened():
            QMessageBox.warning(self, "警告", "请先打开摄像头")
            return

        try:
            # 使用 opencv 读取摄像头的帧
            ret, frame = self.camera_capture.read()
            # 转换 opencv 帧的颜色空间为 RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.model, self.class_indict = load_model_and_labels(self.model_path, self.json_path)
            # 调用你的识别代码
            frame = process_frame(frame, 11, self.model, self.class_indict)
            # 从 opencv 帧创建 QImage 对象
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
            # 创建一个新的 QDialog 实例
            self.snapshot_dialog = QDialog(self)
            self.snapshot_dialog.setWindowTitle('拍照识别结果')
            # 设置窗口关闭事件的处理函数
            self.snapshot_dialog.finished.connect(self.on_snapshot_dialog_closed)

            # 创建一个 QLabel 用于显示提示信息
            info_label = QLabel(
                "请打开摄像头后，再进行拍照识别；而且要注意在当前页面打开的摄像头，也只能点击当前页面的拍照识别",
                self.snapshot_dialog)

            # 创建一个 QLabel 作为图片的显示器
            image_label = QLabel(self.snapshot_dialog)
            # 从 QImage 创建 QPixmap 对象并设置到 QLabel
            image_label.setPixmap(QPixmap.fromImage(image))

            # 创建一个 QVBoxLayout 并将 QLabel 添加进去
            layout = QVBoxLayout()
            layout.addWidget(info_label)  # 将提示信息添加到布局中
            layout.addWidget(image_label)
            self.snapshot_dialog.setLayout(layout)
            self.snapshot_dialog.show()
        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"拍照识别过程中出现错误：{str(e)}")

    def on_snapshot_dialog_closed(self):
        # 将 snapshot_dialog 设置为 None
        self.snapshot_dialog = None
        # 检查是否需要释放摄像头
        self.check_release_camera()

    def check_release_camera(self):
        # 如果没有打开的 CameraWindow 且没有打开的拍照识别窗口，那么释放摄像头
        if not self.camera_windows and not self.snapshot_dialog:
            if self.camera_capture and self.camera_capture.isOpened():
                self.camera_capture.release()
                self.camera_capture = None  # 将 camera_capture 设置为 None

    def open_camera(self):
        # 检查是否已经打开摄像头窗口
        if self.camera_windows:
            QMessageBox.information(self, "Information", "摄像头已经打开")
        else:
            # 创建一个新的 cv2.VideoCapture 实例
            self.camera_capture = cv2.VideoCapture(0)
            # 创建一个新的 CameraWindow 实例并显示它
            camera_window = CameraWindow(self.camera_capture, self)
            camera_window.show()
            # 将新的 CameraWindow 实例添加到列表中
            self.camera_windows.append(camera_window)
            # 在关闭 CameraWindow 时，检查是否需要释放摄像头
            camera_window.finished.connect(self.check_release_camera)

    def resizeEvent(self, event):
        height = event.size().height() * 0.5
        self.table_predict_result.setFixedHeight(int(height))
        super().resizeEvent(event)

    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "选择图片", "", "All Files (*)")

        self.pixmap = QPixmap(imgName)
        self.fname = imgName
        max_size = 450
        if self.pixmap.width() > max_size or self.pixmap.height() > max_size:
            self.label_image.setPixmap(self.pixmap.scaled(
                max_size, max_size, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.label_image.setPixmap(self.pixmap)

        QMessageBox.information(self, "信息提示", "导入图像成功")

    def batch_process(self, classify_func):
        imgNames, imgType = QFileDialog.getOpenFileNames(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        self.batch_processing = True

        dialog = QDialog(self)
        dialog.setWindowTitle("批量处理结果")
        dialog_layout = QVBoxLayout(dialog)
        # 添加最小化和最大化按钮
        dialog.setWindowFlags(
            dialog.windowFlags() | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        batch_result_table = QTableWidget(0, 5, self)
        self.batch_result_table = batch_result_table  # 保存到实例变量
        batch_result_table.setHorizontalHeaderLabels(["序号", "文件名", "Top 1", "Top 2", "Top 3"])

        stacked_widget = QStackedWidget(dialog)
        for i, imgName in enumerate(imgNames):
            self.pixmap = QPixmap(imgName)
            self.fname = imgName
            max_size = 450
            if self.pixmap.width() > max_size or self.pixmap.height() > max_size:
                self.pixmap = self.pixmap.scaled(max_size, max_size, Qt.AspectRatioMode.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(self.pixmap)
            label_info = QLabel(f"图片序号{i + 1}")
            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(label_info)
            widget = QWidget()
            widget.setLayout(vbox)
            stacked_widget.addWidget(widget)

            prediction_results = self.run(classify_func)

            batch_result_table.insertRow(i)
            batch_result_table.setItem(i, 0, QTableWidgetItem(f"图片{i + 1}"))
            batch_result_table.setItem(i, 1, QTableWidgetItem(imgName))  # 插入文件名
            for j, result in enumerate(prediction_results[:3]):
                class_name = result["name"]
                score = f"{result['score']:.4f}"
                batch_result_table.setItem(i, j + 2, QTableWidgetItem(f"{class_name}, 置信度{score}"))

        prev_button = QPushButton("上一张", dialog)
        next_button = QPushButton("下一张", dialog)
        prev_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(max(0, stacked_widget.currentIndex() - 1)))
        next_button.clicked.connect(
            lambda: stacked_widget.setCurrentIndex(min(stacked_widget.count() - 1, stacked_widget.currentIndex() + 1)))

        save_button = QPushButton("下载表格文件", dialog)
        save_button.clicked.connect(self.save_table)

        dialog_layout.addWidget(stacked_widget)
        dialog_layout.addWidget(prev_button)
        dialog_layout.addWidget(next_button)
        dialog_layout.addWidget(save_button)
        dialog_layout.addWidget(batch_result_table)

        dialog.setLayout(dialog_layout)
        dialog.show()

        self.batch_processing = False

    def save_table(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "CSV Files (*.csv);")

        if path:
            with open(path, mode='w', newline='') as file:
                writer = csv.writer(file)
                headers = ["序号", "文件名", "Top 1", "Top 2", "Top 3"]  # 更改为你的列标题
                writer.writerow(headers)
                for row in range(self.batch_result_table.rowCount()):
                    rowdata = []
                    for column in range(self.batch_result_table.columnCount()):
                        item = self.batch_result_table.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

            # 弹出信息框
            QMessageBox.information(self, "信息提示", "文件保存成功")

    def dan_run(self, classify_func):
        if self.fname is None or not os.path.isfile(self.fname):
            QMessageBox.warning(self, "警告", "请先选择图片")
            return

        file_name = self.fname

        with open(file_name, 'rb') as f:
            img_bytes = f.read()

        try:
            prediction_result = classify_func(img_bytes)

            if not self.batch_processing:
                # 在单一图片识别时，清空主窗口的表格
                self.table_predict_result.setRowCount(0)
                for result in prediction_result["result"]:
                    class_name = result["name"]
                    score = f"{result['score']:.4f}"

                    row_position = self.table_predict_result.rowCount()
                    self.table_predict_result.insertRow(row_position)
                    self.table_predict_result.setItem(row_position, 0, QTableWidgetItem(class_name))
                    self.table_predict_result.setItem(row_position, 1, QTableWidgetItem(score))

                self.table_predict_result.resizeColumnsToContents()
                self.table_predict_result.resizeRowsToContents()

                QMessageBox.information(self, "信息提示", "识别成功")

            return prediction_result["result"]

        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"识别过程中出现错误：{str(e)}")

    def run(self, classify_func):
        if self.fname is None or not os.path.isfile(self.fname):
            QMessageBox.warning(self, "警告", "请先选择图片")
            return

        file_name = self.fname

        with open(file_name, 'rb') as f:
            img_bytes = f.read()

        try:
            prediction_result = classify_func(img_bytes)

            if not self.batch_processing:
                self.table_predict_result.setRowCount(0)
                for result in prediction_result["result"]:
                    class_name = result["name"]
                    score = f"{result['score']:.4f}"

                    row_position = self.table_predict_result.rowCount()
                    self.table_predict_result.insertRow(row_position)
                    self.table_predict_result.setItem(row_position, 0, QTableWidgetItem(class_name))
                    self.table_predict_result.setItem(row_position, 1, QTableWidgetItem(score))

                self.table_predict_result.resizeColumnsToContents()
                self.table_predict_result.resizeRowsToContents()

                QMessageBox.information(self, "信息提示", "识别成功")

            return prediction_result["result"]

        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"识别过程中出现错误：{str(e)}")


class CustomTab(Tab):
    def __init__(self, parent=None, camera_windows=None):
        super().__init__(None, parent, camera_windows)

        self.model_path = None
        self.class_path = None
        self.model = None
        self.class_indict = None

        self.button_search_image_zi = QPushButton('选择图片', self)
        self.button_search_image_zi.setMaximumWidth(100)

        self.button_search_model = QPushButton('选择模型', self)
        self.button_search_model.setMaximumWidth(100)  # 将按钮的最大宽度设置为100像素
        # 为其他按钮也设置最大宽度
        self.button_search_class = QPushButton('选择类别文件', self)
        self.button_search_class.setMaximumWidth(100)
        self.button_run_zi = QPushButton('识别', self)
        self.button_run_zi.setMaximumWidth(100)
        self.button_batch_process_zi = QPushButton('批量处理', self)
        self.button_batch_process_zi.setMaximumWidth(100)
        self.text_model_path = QLineEdit(self)
        self.text_model_path.setFixedWidth(150)
        self.text_class_path = QLineEdit(self)
        self.text_class_path.setFixedWidth(150)
        self.button_open_camera_zi = QPushButton('打开摄像头', self)
        self.button_open_camera_zi.setMaximumWidth(100)
        self.button_snapshot_zi = QPushButton('拍照识别', self)
        self.button_snapshot_zi.setMaximumWidth(100)
        self.button_submit_video_zidi = QPushButton('提交视频', self)
        self.button_submit_video_zidi.setMaximumWidth(100)

        self.layout.addWidget(self.button_search_model, 1, 0, 1, 1)
        self.layout.addWidget(self.text_model_path, 2, 0, 1, 1)  # 将文件路径显示框放在对应按键的下方
        self.layout.addWidget(self.button_search_class, 3, 0, 1, 1)
        self.layout.addWidget(self.text_class_path, 4, 0, 1, 1)  # 将文件路径显示框放在对应按键的下方
        self.layout.addWidget(self.button_search_image_zi, 5, 0, 1, 1)
        self.layout.addWidget(self.button_run_zi, 6, 0, 1, 1)
        self.layout.addWidget(self.button_batch_process_zi, 7, 0, 1, 1)
        self.layout.addWidget(self.button_open_camera_zi, 8, 0, 1, 1)
        self.layout.addWidget(self.button_snapshot_zi, 9, 0, 1, 1)
        self.layout.addWidget(self.button_submit_video_zidi, 10, 0, 1, 1)

        self.button_search_image_zi.clicked.connect(self.openimage)
        self.button_search_model.clicked.connect(self.open_model)
        self.button_search_class.clicked.connect(self.open_class)
        self.button_run_zi.clicked.connect(self.run)
        self.button_batch_process_zi.clicked.connect(self.batch_process)
        self.button_open_camera_zi.clicked.connect(self.open_camera_zidi)
        self.button_snapshot_zi.clicked.connect(self.snapshot_recognition_zidi)
        self.button_submit_video_zidi.clicked.connect(self.submit_video_zidi)

        self.button_search_image.deleteLater()
        self.button_run.deleteLater()  # 移除按钮
        self.button_batch_process.deleteLater()  # 移除按钮
        self.button_open_camera.deleteLater()  # 移除按钮
        self.button_snapshot.deleteLater()
        self.button_submit_video.deleteLater()

    def submit_video_zidi(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return
        try:
            # 弹出一个文件选择对话框来选择视频文件
            fname, _ = QFileDialog.getOpenFileName(self, '选择视频', '.', 'Video files(*.mp4 *.avi);;All Files(*)')

            if fname:
                # self.model, self.class_indict = load_model_and_labels(self.model_path, self.json_path)
                # 使用你的模型对视频进行预测，并将预测结果保存到新的视频文件
                output_fname = generate_video(fname, 11, self.model, self.class_indict)
                # 弹出一个消息框提示视频处理成功
                QMessageBox.information(self, "提示", "处理后的视频保存成功")
                # # 使用一个播放器显示预测结果视频
                # self.player = QMediaPlayer(self)
                # self.player.setMedia(QMediaContent(QUrl.fromLocalFile(output_fname)))
                # video_widget = QVideoWidget(self)
                #
                # # 设置视频窗口的最小和最大尺寸
                # video_widget.setMinimumSize(100, 100)  # 设置最小尺寸为 100x100 像素
                # video_widget.setMaximumSize(500, 500)  # 设置最大尺寸为 500x500 像素
                #
                # # 使视频窗口有一个最小化按钮和一个最大化/全屏按钮
                # video_widget.setWindowFlags(
                #     Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
                #
                # self.player.setVideoOutput(video_widget)
                # self.layout.addWidget(video_widget, 1, 1, 6, 2)
                # self.player.play()
                # video_widget.show()  # 确保视频窗口是可见的
        except Exception as e:
            # 如果出现任何错误，显示一个错误消息框
            QMessageBox.critical(self, "Error", str(e))

    def snapshot_recognition_zidi(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return
            # 检查摄像头是否已经打开
        if not self.camera_capture or not self.camera_capture.isOpened():
            QMessageBox.warning(self, "警告", "请先打开摄像头")
            return
        try:
            if self.camera_capture.isOpened():
                # 使用 opencv 读取摄像头的帧
                ret, frame = self.camera_capture.read()
                # 转换 opencv 帧的颜色空间为 RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 调用你的识别代码
                frame = process_frame(frame, 11, self.model, self.class_indict)
                # 从 opencv 帧创建 QImage 对象
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
                # 创建一个新的 QDialog 实例
                self.snapshot_dialog = QDialog(self)
                self.snapshot_dialog.setWindowTitle('拍照识别结果')
                # 设置窗口关闭事件的处理函数
                self.snapshot_dialog.finished.connect(self.on_snapshot_dialog_closed)

                # 创建一个 QLabel 用于显示提示信息
                info_label = QLabel(
                    "请打开摄像头后，再进行拍照识别；而且要注意在当前页面打开的摄像头，也只能点击当前页面的拍照识别",
                    self.snapshot_dialog)

                # 创建一个 QLabel 作为图片的显示器
                image_label = QLabel(self.snapshot_dialog)
                # 从 QImage 创建 QPixmap 对象并设置到 QLabel
                image_label.setPixmap(QPixmap.fromImage(image))

                # 创建一个 QVBoxLayout 并将 QLabel 添加进去
                layout = QVBoxLayout()
                layout.addWidget(info_label)  # 将提示信息添加到布局中
                layout.addWidget(image_label)
                self.snapshot_dialog.setLayout(layout)
                self.snapshot_dialog.show()
        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"拍照识别过程中出现错误：{str(e)}")

    def on_snapshot_dialog_closed(self):
        # 将 snapshot_dialog 设置为 None
        self.snapshot_dialog = None
        # 检查是否需要释放摄像头
        self.check_release_camera()

    def check_release_camera(self):
        # 如果没有打开的 CameraWindow 且没有打开的拍照识别窗口，那么释放摄像头
        if not self.camera_windows and not self.snapshot_dialog:
            if self.camera_capture and self.camera_capture.isOpened():
                self.camera_capture.release()

    def open_camera_zidi(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return
        if any(window.capture.isOpened() for window in self.camera_windows):
            QMessageBox.information(self, "Information", "摄像头已经打开")
        else:
            # 创建一个新的 cv2.VideoCapture 实例
            self.camera_capture = cv2.VideoCapture(0)
            # 创建一个新的 CameraWindow 实例并显示它

            camera_window = CustomCameraWindow(self.camera_capture, self.model, self.class_indict, self)
            camera_window.show()

            # 将新的 CameraWindow 实例添加到列表中
            self.camera_windows.append(camera_window)
            # 在关闭 CameraWindow 时，检查是否需要释放摄像头
            camera_window.finished.connect(self.check_release_camera)

    def open_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "选择模型", "", "Model Files (*.pth *.onnx);")

        # 如果用户取消了文件选择，那么就直接返回
        if not model_path:
            return

        self.text_model_path.setText(model_path)
        self.model_path = model_path
        try:
            # 获取文件扩展名
            _, ext = os.path.splitext(model_path)

            # 加载模型
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            if ext.lower() == ".pth":
                self.model = torch.load(model_path, map_location=device)
            elif ext.lower() == ".onnx":
                self.model = onnxruntime.InferenceSession(model_path)
            else:
                QMessageBox.warning(self, "警告", "未知的模型文件类型")
                return



        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"加载模型时出现错误：{str(e)}")
            return
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return

    def open_class(self):
        class_path, _ = QFileDialog.getOpenFileName(self, "选择类别json文件", "", "JSON Files (*.json);")

        # 如果用户取消了文件选择，那么就直接返回
        if not class_path:
            return

        self.text_class_path.setText(class_path)
        self.class_path = class_path

        try:

            # 获取文件扩展名
            _, ext = os.path.splitext(class_path)

            if ext.lower() == ".json":
                # load class info
                json_file = open(class_path, 'rb')
                self.class_indict = json.load(json_file)
            else:
                QMessageBox.warning(self, "警告", "未知的模型文件类型")
                return

        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"加载模型时出现错误：{str(e)}")
            return

        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return

    def run(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return
        if self.fname is None or not os.path.isfile(self.fname):
            QMessageBox.warning(self, "警告", "请先选择图片")
            return
        file_name = self.fname
        with open(file_name, 'rb') as f:
            img_bytes = f.read()
        try:
            # 检查模型类型
            if isinstance(self.model, torch.nn.Module):
                # 使用 PyTorch 进行预测
                prediction_result = get_prediction_img_zidi(image_bytes=img_bytes, model_zidi=self.model,
                                                            json_zidi=self.class_indict)
            elif isinstance(self.model, onnxruntime.InferenceSession):
                # 使用 ONNX Runtime 进行预测
                prediction_result = get_prediction_img_zidi_onnx(image_bytes=img_bytes, model_zidi=self.model,
                                                                 json_zidi=self.class_indict)
            else:
                QMessageBox.warning(self, "警告", "未知的模型类型")
                return

            if not self.batch_processing:
                # 在单一图片识别时，清空主窗口的表格
                self.table_predict_result.setRowCount(0)
                for result in prediction_result["result"]:
                    class_name = result["name"]
                    score = f"{result['score']:.4f}"

                    row_position = self.table_predict_result.rowCount()
                    self.table_predict_result.insertRow(row_position)
                    self.table_predict_result.setItem(row_position, 0, QTableWidgetItem(class_name))
                    self.table_predict_result.setItem(row_position, 1, QTableWidgetItem(score))

                self.table_predict_result.resizeColumnsToContents()
                self.table_predict_result.resizeRowsToContents()

                QMessageBox.information(self, "信息提示", "识别成功")

            return prediction_result["result"]

        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"识别过程中出现错误：{str(e)}")

    def batch_run(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return
        if self.fname is None or not os.path.isfile(self.fname):
            QMessageBox.warning(self, "警告", "请先选择图片")
            return
        file_name = self.fname
        with open(file_name, 'rb') as f:
            img_bytes = f.read()
        try:
            # 检查模型类型
            if isinstance(self.model, torch.nn.Module):
                # 使用 PyTorch 进行预测
                prediction_result = get_prediction_img_zidi(image_bytes=img_bytes, model_zidi=self.model,
                                                            json_zidi=self.class_indict)
            elif isinstance(self.model, onnxruntime.InferenceSession):
                # 使用 ONNX Runtime 进行预测
                prediction_result = get_prediction_img_zidi_onnx(image_bytes=img_bytes, model_zidi=self.model,
                                                                 json_zidi=self.class_indict)
            else:
                QMessageBox.warning(self, "警告", "未知的模型类型")
                return

            if not self.batch_processing:
                # 在单一图片识别时，清空主窗口的表格
                self.table_predict_result.setRowCount(0)
                for result in prediction_result["result"]:
                    class_name = result["name"]
                    score = f"{result['score']:.4f}"

                    row_position = self.table_predict_result.rowCount()
                    self.table_predict_result.insertRow(row_position)
                    self.table_predict_result.setItem(row_position, 0, QTableWidgetItem(class_name))
                    self.table_predict_result.setItem(row_position, 1, QTableWidgetItem(score))

                self.table_predict_result.resizeColumnsToContents()
                self.table_predict_result.resizeRowsToContents()

                QMessageBox.information(self, "信息提示", "识别成功")

            return prediction_result["result"]

        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"识别过程中出现错误：{str(e)}")

    def batch_process(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.class_path is None or not os.path.isfile(self.class_path):
            QMessageBox.warning(self, "警告", "请先选择类别json文件")
            return
        imgNames, imgType = QFileDialog.getOpenFileNames(self, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        self.batch_processing = True

        dialog = QDialog(self)
        dialog.setWindowTitle("批量处理结果")
        dialog_layout = QVBoxLayout(dialog)
        # 添加最小化和最大化按钮
        dialog.setWindowFlags(
            dialog.windowFlags() | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        batch_result_table = QTableWidget(0, 5, self)
        self.batch_result_table = batch_result_table  # 保存到实例变量
        batch_result_table.setHorizontalHeaderLabels(["序号", "文件名", "Top 1", "Top 2", "Top 3"])

        stacked_widget = QStackedWidget(dialog)
        for i, imgName in enumerate(imgNames):
            self.pixmap = QPixmap(imgName)
            self.fname = imgName
            max_size = 450
            if self.pixmap.width() > max_size or self.pixmap.height() > max_size:
                self.pixmap = self.pixmap.scaled(max_size, max_size, Qt.AspectRatioMode.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(self.pixmap)
            label_info = QLabel(f"图片序号{i + 1}")
            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(label_info)
            widget = QWidget()
            widget.setLayout(vbox)
            stacked_widget.addWidget(widget)

            prediction_results = self.batch_run()

            batch_result_table.insertRow(i)
            batch_result_table.setItem(i, 0, QTableWidgetItem(f"图片{i + 1}"))
            batch_result_table.setItem(i, 1, QTableWidgetItem(imgName))  # 插入文件名
            for j, result in enumerate(prediction_results[:3]):
                class_name = result["name"]
                score = f"{result['score']:.4f}"
                batch_result_table.setItem(i, j + 2, QTableWidgetItem(f"{class_name}, 置信度{score}"))

        prev_button = QPushButton("上一张", dialog)
        next_button = QPushButton("下一张", dialog)
        prev_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(max(0, stacked_widget.currentIndex() - 1)))
        next_button.clicked.connect(
            lambda: stacked_widget.setCurrentIndex(min(stacked_widget.count() - 1, stacked_widget.currentIndex() + 1)))

        save_button = QPushButton("下载表格文件", dialog)
        save_button.clicked.connect(self.save_table)

        dialog_layout.addWidget(stacked_widget)
        dialog_layout.addWidget(prev_button)
        dialog_layout.addWidget(next_button)
        dialog_layout.addWidget(save_button)
        dialog_layout.addWidget(batch_result_table)

        dialog.setLayout(dialog_layout)
        dialog.show()

        self.batch_processing = False


class LoadingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('程序加载中,请等待👻👻...')
        self.setFixedSize(420, 270)

        # 创建一个QLabel对象用于显示图片
        self.label = QLabel(self)

        # 创建QPixmap对象并加载图片文件
        self.pixmap = QPixmap("sanye.png")  # 请替换为你的图片文件路径

        # 创建QPainter对象并开始绘制
        painter = QPainter(self.pixmap)

        # 设置画笔颜色和字体
        painter.setPen(QPen(QColor("#fff3cd")))
        font = QFont("Calligraphy", 180)
        font.setWeight(100)
        painter.setFont(font)
        # 在图片上添加文字
        painter.drawText(self.pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "三叶识青")

        # 结束绘制
        painter.end()

        # 将图片缩放到合适的大小
        self.pixmap = self.pixmap.scaled(self.width(), self.height())

        # 将QPixmap对象设置到QLabel
        self.label.setPixmap(self.pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 设置样式表
        self.setStyleSheet("background-color: white; color: white;")
        self.label.setStyleSheet("color: white;")

        self.setModal(True)


class Ui_example(QWidget):
    def __init__(self):
        super().__init__()

        self.loading_window = LoadingWindow(self)
        self.loading_window.show()

        # 设置窗口图标
        self.setWindowIcon(QIcon('./sanyeqing.ico'))
        # 创建并显示等待窗口
        self.article_text_bottom = None

        # 确保主窗口及其内容在处理事件时得到更新
        QApplication.processEvents()

        self.tab_widget = QTabWidget(self)
        # 添加一个列表来存储所有的 CameraWindow 实例
        self.camera_windows = []

        from PyQt6.QtWidgets import QSizePolicy

        # 创建一个新的 QWidget 实例用于展示文章内容
        self.article_tab = QWidget()
        self.article_layout = QVBoxLayout()

        self.article_text_main = QTextEdit()
        self.article_text_main.setReadOnly(True)
        self.article_text_main.setHtml("""
            <center>
                <p><font size="6" color="black">三叶青图像识别软件</font></p>
                <p><font size="5" color="yellow">该软件通过对三叶青块根照片进行产地的鉴定，(但是鉴定效果似乎不太行，模型后续要改善）；后续还要添加三叶青叶片识别</font></p>
                <p><font size="4" color="green">相关软件有：网站——三叶识青：https://www.whtuu.cn  ;  微信小程序——三叶识青：三叶识青</font></p>
                <p  style="margin-top:30px;"><font size="4" color="red">软件使用说明:<br></font>本软件为使用pyqt+opencv开发的图像识别qt界面<br>
                在本软件中，目前共有五个主界面：软件介绍界面、省份识别、浙产识别、产地识别界面以及自定义识别页面。<br>
                其中，软件介绍界面主要是对该软件进行简单介绍并且关联了该项研究的其它软件和开发者信息。<br>
                之后，省份识别、浙产识别、产地识别界面则是共用一个窗口模板，只是将对应的模型文件和json类型文件改变了。<br>
                然后，自定义识别页面支持用户上传自己的模型文件（.onnnx或.pth)以及对应的json类别文件，完成用户自己的图像分类。<br>
                <font  size="4" color="pink">最后，给出一些提示信息：</font><br>
                打开摄像头，点击”实时预测“按钮后，可按'a'键启动省份识别模型；按's'键启动浙产识别模型；按'd'键启动产地识别模型。<br>
                另外只有打开摄像头,才能点击"拍照识别"按钮，并且要注意在当前页面打开的摄像头，也只能点击当前页面的拍照识别。<br>
                提交视频进行预测时，要中断预测，请按'q'键退出。另外预测完后，处理后的视频会自动保存在当前目录下。
                </p>
            </center>
        """)
        self.article_layout.addWidget(self.article_text_main)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.article_layout.addItem(spacer)
        self.article_text_main.setMinimumHeight(400)

        self.article_layout.addWidget(self.article_text_bottom)
        self.article_text_bottom = QTextEdit()
        self.article_text_bottom.setReadOnly(True)
        self.article_text_bottom.setHtml("""
            <p><font size="4" color="yellow">
            <font size='5' color='green'>开发者信息：</font> <br>
            开发者文档：@星云文档（https://xingyun-dev.github.io/）；<br>
            开发者CSDN账号：@星石传说（https://blog.csdn.net/2301_78630677?type=blog）；<br>
            开发者Github账号：@xingyun-dev（https://github.com/xingyun-dev?tab=repositories）；<br>
            
            <font size='5' color='red' margin-top ='10px'>后续安排：</font><br>
            前面提到，模型在实际预测中的表现并不尽如人意，后续的模型要再进行修改；随之这个软件也要进行补充完善。现在这个版本暂时称为：qt-三叶识青-1.0.0;
            </p>
        """)
        self.article_layout.addWidget(self.article_text_bottom)

        self.article_tab.setLayout(self.article_layout)
        self.tab_widget.insertTab(0, self.article_tab, "软件介绍")

        self.shenfen_tab = Tab(shenfen_classify, './model_cpu_97.18.onnx', './class_indices_5.json', self,
                               self.camera_windows)
        self.tab_widget.addTab(self.shenfen_tab, "省份识别")

        self.zhechan_tab = Tab(zhechan_classify, './model_cpu_3.onnx', './class_indices_2.json', self,
                               self.camera_windows)
        self.tab_widget.addTab(self.zhechan_tab, "浙产识别")

        self.chandi_tab = Tab(chan_classify, './model_cpu_11.onnx', './class_indices_10.json', self,
                              self.camera_windows)
        self.tab_widget.addTab(self.chandi_tab, "产地识别")

        self.custom_tab = CustomTab(self, self.camera_windows)
        self.tab_widget.addTab(self.custom_tab, "自定义识别")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

        self.resize(600, 600)
        self.setWindowTitle('三叶青识别')

        # 关闭等待窗口
        self.loading_window.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_example()
    ex.show()
    sys.exit(app.exec())
