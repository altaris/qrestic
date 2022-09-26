# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QProgressBar, QSizePolicy, QSpacerItem, QTabWidget,
    QTableView, QTextEdit, QToolButton, QVBoxLayout,
    QWidget)
from  . import ressources_rc

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(1143, 717)
        font = QFont()
        font.setPointSize(15)
        MainWidget.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(MainWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.w_conf = QWidget(MainWidget)
        self.w_conf.setObjectName(u"w_conf")
        self.verticalLayout_4 = QVBoxLayout(self.w_conf)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.le_configuration_file = QLineEdit(self.w_conf)
        self.le_configuration_file.setObjectName(u"le_configuration_file")
        self.le_configuration_file.setCursor(QCursor(Qt.ForbiddenCursor))
        self.le_configuration_file.setReadOnly(True)

        self.gridLayout.addWidget(self.le_configuration_file, 0, 1, 1, 1)

        self.le_folder = QLineEdit(self.w_conf)
        self.le_folder.setObjectName(u"le_folder")
        self.le_folder.setCursor(QCursor(Qt.ForbiddenCursor))
        self.le_folder.setReadOnly(True)

        self.gridLayout.addWidget(self.le_folder, 1, 1, 1, 1)

        self.pb_configuration_file = QToolButton(self.w_conf)
        self.pb_configuration_file.setObjectName(u"pb_configuration_file")
        icon = QIcon()
        icon.addFile(u":/main/icons/folder.svg", QSize(), QIcon.Normal, QIcon.On)
        self.pb_configuration_file.setIcon(icon)

        self.gridLayout.addWidget(self.pb_configuration_file, 0, 2, 1, 1)

        self.label = QLabel(self.w_conf)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pb_folder = QToolButton(self.w_conf)
        self.pb_folder.setObjectName(u"pb_folder")
        self.pb_folder.setIcon(icon)

        self.gridLayout.addWidget(self.pb_folder, 1, 2, 1, 1)

        self.label_2 = QLabel(self.w_conf)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_3.addWidget(self.w_conf)

        self.line = QFrame(MainWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.w_operations = QWidget(MainWidget)
        self.w_operations.setObjectName(u"w_operations")
        self.verticalLayout_2 = QVBoxLayout(self.w_operations)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.w_buttons = QWidget(self.w_operations)
        self.w_buttons.setObjectName(u"w_buttons")
        self.w_buttons.setMinimumSize(QSize(100, 0))
        self.w_buttons.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout = QVBoxLayout(self.w_buttons)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pb_backup = QToolButton(self.w_buttons)
        self.pb_backup.setObjectName(u"pb_backup")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_backup.sizePolicy().hasHeightForWidth())
        self.pb_backup.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u":/main/icons/upload.svg", QSize(), QIcon.Normal, QIcon.On)
        self.pb_backup.setIcon(icon1)
        self.pb_backup.setIconSize(QSize(32, 32))
        self.pb_backup.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.pb_backup)

        self.pb_restore = QToolButton(self.w_buttons)
        self.pb_restore.setObjectName(u"pb_restore")
        sizePolicy.setHeightForWidth(self.pb_restore.sizePolicy().hasHeightForWidth())
        self.pb_restore.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/main/icons/download.svg", QSize(), QIcon.Normal, QIcon.On)
        self.pb_restore.setIcon(icon2)
        self.pb_restore.setIconSize(QSize(32, 32))
        self.pb_restore.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.pb_restore)

        self.verticalSpacer = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pb_init = QToolButton(self.w_buttons)
        self.pb_init.setObjectName(u"pb_init")
        sizePolicy.setHeightForWidth(self.pb_init.sizePolicy().hasHeightForWidth())
        self.pb_init.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addFile(u":/main/icons/cloud.svg", QSize(), QIcon.Normal, QIcon.On)
        self.pb_init.setIcon(icon3)
        self.pb_init.setIconSize(QSize(32, 32))
        self.pb_init.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.pb_init)

        self.pb_snapshots = QToolButton(self.w_buttons)
        self.pb_snapshots.setObjectName(u"pb_snapshots")
        sizePolicy.setHeightForWidth(self.pb_snapshots.sizePolicy().hasHeightForWidth())
        self.pb_snapshots.setSizePolicy(sizePolicy)
        icon4 = QIcon()
        icon4.addFile(u":/main/icons/database.svg", QSize(), QIcon.Normal, QIcon.On)
        self.pb_snapshots.setIcon(icon4)
        self.pb_snapshots.setIconSize(QSize(32, 32))
        self.pb_snapshots.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.pb_snapshots)


        self.horizontalLayout.addWidget(self.w_buttons)

        self.tab_widget = QTabWidget(self.w_operations)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_results = QWidget()
        self.tab_results.setObjectName(u"tab_results")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_results)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.table_view = QTableView(self.tab_results)
        self.table_view.setObjectName(u"table_view")
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)

        self.horizontalLayout_2.addWidget(self.table_view)

        icon5 = QIcon()
        icon5.addFile(u":/main/icons/list.svg", QSize(), QIcon.Normal, QIcon.On)
        self.tab_widget.addTab(self.tab_results, icon5, "")
        self.tab_raw = QWidget()
        self.tab_raw.setObjectName(u"tab_raw")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_raw)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.te_raw = QTextEdit(self.tab_raw)
        self.te_raw.setObjectName(u"te_raw")
        self.te_raw.setUndoRedoEnabled(False)
        self.te_raw.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.te_raw)

        icon6 = QIcon()
        icon6.addFile(u":/main/icons/align-left.svg", QSize(), QIcon.Normal, QIcon.On)
        self.tab_widget.addTab(self.tab_raw, icon6, "")

        self.horizontalLayout.addWidget(self.tab_widget)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.progress_bar_busy = QProgressBar(self.w_operations)
        self.progress_bar_busy.setObjectName(u"progress_bar_busy")
        self.progress_bar_busy.setMaximum(0)
        self.progress_bar_busy.setValue(-1)
        self.progress_bar_busy.setTextVisible(False)

        self.verticalLayout_2.addWidget(self.progress_bar_busy)

        self.progress_bar = QProgressBar(self.w_operations)
        self.progress_bar.setObjectName(u"progress_bar")

        self.verticalLayout_2.addWidget(self.progress_bar)


        self.verticalLayout_3.addWidget(self.w_operations)


        self.retranslateUi(MainWidget)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"qrestic", None))
        self.pb_configuration_file.setText(QCoreApplication.translate("MainWidget", u"Choose configuration file", None))
        self.label.setText(QCoreApplication.translate("MainWidget", u"Configuration file", None))
        self.pb_folder.setText(QCoreApplication.translate("MainWidget", u"Choose folder", None))
        self.label_2.setText(QCoreApplication.translate("MainWidget", u"Folder", None))
        self.pb_backup.setText(QCoreApplication.translate("MainWidget", u"New backup", None))
        self.pb_restore.setText(QCoreApplication.translate("MainWidget", u"Restore last snapshot", None))
        self.pb_init.setText(QCoreApplication.translate("MainWidget", u"Initialize repository", None))
        self.pb_snapshots.setText(QCoreApplication.translate("MainWidget", u"Show snapshots", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_results), QCoreApplication.translate("MainWidget", u"Results", None))
        self.te_raw.setPlaceholderText(QCoreApplication.translate("MainWidget", u"Logs will appear here", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_raw), QCoreApplication.translate("MainWidget", u"Logs", None))
    # retranslateUi

