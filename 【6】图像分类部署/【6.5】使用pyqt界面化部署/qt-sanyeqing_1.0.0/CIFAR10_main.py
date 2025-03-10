import sys
from PyQt6.QtWidgets import (QApplication, QDialog, QFileDialog,QMessageBox,
                             QGraphicsScene,QGraphicsPixmapItem)
from PyQt6.QtGui import QPixmap
import CIFAR10_class
from PIL import Image

class CIFAR10_classApp(QDialog, CIFAR10_class.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pushButton_input.clicked.connect(self.input_images)
        self.pushButton_run.clicked.connect(self.run_model)
        # 创建标签部件
        self.graphicsView_input.setScene(QGraphicsScene(self))  # 创建场景对象并设置为graphicsView_input的场景

    def input_images(self):
        try:
            global fname
            imgName, imgType = QFileDialog.getOpenFileName(self, "导入图片", "", "*.jpg;;*.png;;All Files(*)")
            pixmap = QPixmap(imgName).scaled(self.graphicsView_input.width(), self.graphicsView_input.height())
            pixmap_item = QGraphicsPixmapItem(pixmap)
            scene = self.graphicsView_input.scene()  # 获取graphicsView_input的场景
            scene.clear()  # 清空场景
            scene.addItem(pixmap_item)  # 添加图像
            fname = imgName


            # 显示导入成功的消息框
            QMessageBox.information(self, "信息提示", "导入成功")
        except Exception as e:
            QMessageBox.critical(self, "错误提示", f"识别过程中出现错误：{str(e)}")

    def run_model(self):
        global fname
        file_name = str(fname)
        img = Image.open(file_name)

        try:
            a, b = predict_(img)
            self.plainTextEdit_result.setPlainText(a)
            self.plainTextEdit_pred.setPlainText(str(b))
            QMessageBox.information(self, "信息提示", "识别成功")


        except Exception as e:

            QMessageBox.critical(self, "错误提示", f"识别过程中出现错误：{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CIFAR10_classApp()
    sys.exit(app.exec())

