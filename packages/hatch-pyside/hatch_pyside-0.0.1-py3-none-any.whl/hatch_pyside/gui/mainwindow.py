#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import json
import os
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QListWidget

import hatch_pyside
import hatch_pyside.gui.app as app
from hatch_pyside import __version__
from hatch_pyside.gui.ui_about import Ui_About
from hatch_pyside.gui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    files: list[str]
    project_files: list[str]
    dirty: bool
    json_file: Optional[str] = None

    def __init__(self, projects: list[str], folder: str, name: str):
        super().__init__()
        self.setupUi(self)
        self.projects = projects
        self.project = folder
        self.setWindowTitle(f"hatch-pyside - {folder}")
        if len(projects) <= 1:
            self.action_Change_project_folder.setVisible(False)
        self.reload()
        self.proj_name = name

    @Slot()
    def about_qt(self):
        # noinspection PyUnresolvedReferences
        QApplication.instance().aboutQt()

    @Slot()
    def about(self):
        About().exec()

    @Slot()
    def change_project(self):
        self.project = app.choose_project(self.projects)
        self.setWindowTitle(f"hatch-pyside - {self.project}")
        self.reload()

    @Slot()
    def reload(self):
        self.files = [f for f in os.listdir(self.project)
                      if os.path.isfile(os.path.join(self.project, f))]
        for f in self.files:
            if os.path.normcase(f).endswith('.pyproject'):
                with open(Path(self.project) / f) as fd:
                    self.project_files = json.load(fd)['files']
                    self.json_file = f
                    break
        else:
            self.json_file = None
            self.project_files = []
        self.project_files_widget.clear()
        self.files_widget.clear()
        self.project_files_widget.addItems(self.project_files)
        items = [f for f in self.files if f not in self.project_files]
        self.files_widget.addItems(items)
        self.dirty = False

    @Slot()
    def build(self):
        hatch_pyside.build(self.project)
        self.reload()

    @Slot()
    def clean(self):
        hatch_pyside.clean(self.project)
        self.reload()

    @Slot()
    def remove(self):
        self.dirty |= move_sel(self.project_files_widget, self.files_widget)

    @Slot()
    def add(self):
        self.dirty |= move_sel(self.files_widget, self.project_files_widget)

    @Slot()
    def save(self):
        print("Saving")
        self.project_files = sorted(
            [self.project_files_widget.item(row).text()
             for row in range(self.project_files_widget.count())])
        json_file = self.json_file
        if json_file is None:
            json_file = f'{self.proj_name}.pyproject'
        with open(Path(self.project) / json_file, 'w') as fd:
            # noinspection PyTypeChecker
            json.dump({'files': self.project_files}, fd)
            self.json_file = json_file
            self.dirty = False

    def closeEvent(self, event: QCloseEvent):
        if self.dirty:
            buttons = (QMessageBox.StandardButton.Save
                       | QMessageBox.StandardButton.Discard
                       | QMessageBox.StandardButton.Cancel)
            cr = QMessageBox(QMessageBox.Icon.Warning, "Save?",
                           "The project file has unsaved changes"
                           "do you want to quit anyway?",
                           standardButtons=buttons).exec()
            if cr == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif cr == QMessageBox.StandardButton.Save:
                self.save()
        event.accept()


def move_sel(src: QListWidget, dest: QListWidget) -> bool:
    sel = src.selectedItems()
    if len(sel) == 0:
        return False
    for item in dest.selectedItems():
        item.setSelected(False)
    for item in sel:
        it = src.takeItem(src.row(item))
        dest.addItem(it)
        it.setSelected(True)
    return True


def clear_selection(list_widget: QListWidget) -> None:
    for item in list_widget.selectedItems():
        item.setSelected(False)


class About(QDialog, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.version.setText(__version__)
