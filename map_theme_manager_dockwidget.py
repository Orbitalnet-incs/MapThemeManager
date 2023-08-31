# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapThemeManagerDockWidget
                                 A QGIS plugin
 テーマ編集
        copyright            : (C) 2023 by orbitalnet
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtWidgets, uic, Qt
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QBrush

from qgis.core import QgsProject, QgsMapThemeCollection, Qgis
from qgis.gui import *
from qgis.utils import iface

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QListWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'map_theme_manager_dockwidget_base.ui'))


class MapThemeManagerDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(MapThemeManagerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.iface = iface
        
        self.applying_theme_name = ""

        # テーマリストを表示
        self.setProjectThemes()

        # ###################################################
        #connect
        self.btn_apply.clicked.connect(self.btn_apply_clicked) # 適用
        self.btn_insert.clicked.connect(self.btn_insert_clicked) # 追加
        self.btn_copy.clicked.connect(self.btn_copy_clicked) # コピー
        self.btn_delete.clicked.connect(self.btn_delete_clicked) # 削除
        self.btn_save.clicked.connect(self.btn_save_clicked) # 保存

        if Qgis.QGIS_VERSION_INT >= 31400:
            # テーマ名変更
            QgsProject.instance().mapThemeCollection().mapThemeRenamed.connect(self.themeRenamed)

        # テーマリスト変更
        QgsProject.instance().mapThemeCollection().mapThemesChanged.connect(self.themeChanged)

        # プロジェクト変更
        QgsProject.instance().homePathChanged.connect(self.updateThemeList)

        # テーマ変更
        QgsProject.instance().mapThemeCollectionChanged.connect(self.changeMapCollection)
    
        # ###################################################


    def setProjectThemes(self):
        '''
        /***************************************************************************
        プロジェクトのテーマを設定して表示
        ***************************************************************************/
        '''
        # プロジェクトのテーマを取得
        project_themes = QgsProject.instance().mapThemeCollection().mapThemes() 

        for theme in project_themes:
            self.listWidget.addItem(theme)

        # 一覧設定
        self.listWidget.setEditTriggers(QListWidget.NoEditTriggers) # 選択するテーマは編集不可とする
        self.listWidget.setSelectionMode(QListWidget.SingleSelection)   # 選択モードを単一選択
        self.listWidget.setSortingEnabled(False)   # 並べ替えなし


    def btn_apply_clicked(self):
        '''
        /***************************************************************************
        適用をクリック時の処理
        ***************************************************************************/
        '''
        # テーマ一覧が空の場合
        if self.listWidget.currentItem() is None:
            QMessageBox.warning(self, "適用", f"テーマを選択してください。", QMessageBox.Ok)
            return

        # レイヤ情報のルートおよび一覧を取得        
        root = QgsProject.instance().layerTreeRoot()
        model = self.iface.layerTreeView().layerTreeModel()

        # 選択したテーマを取得
        selected_theme = self.listWidget.currentItem()
        if selected_theme == None:
            return

        # 適用
        selected_theme_text = selected_theme.text()
        QgsProject.instance().mapThemeCollection().applyTheme(selected_theme_text, root, model)

        # 適用後の処理
        previous_theme_name = self.applying_theme_name
        if len(previous_theme_name) > 0:
            # 前のテーマの背景をリセット
            self.releaseApplying(previous_theme_name)

        # 背景色を設定
        self.applying_theme_name = selected_theme_text
        self.setAppliedItem(selected_theme)


    def btn_insert_clicked(self):
        '''
        /***************************************************************************
        追加をクリック時の処理
        ***************************************************************************/
        '''

        # 入力ダイアログを表示
        new_theme,ok = QInputDialog.getText(self, "追加", "現在の状態で追加しますか？")        
        if ok == False:
            return
        
        # 入力チェック
        if new_theme == None or new_theme == "":
            QMessageBox.warning(self, "追加", f"テーマ名を入力してください。", QMessageBox.Ok)
            # 再表示
            self.btn_insert_clicked()
            return

        # 存在するテーマの重複管理
        if QgsProject.instance().mapThemeCollection().hasMapTheme(new_theme) == True:
            QMessageBox.warning(self, "追加", f"入力したテーマ名は重複するため、別のテーマ名を入力してください。", QMessageBox.Ok)
            # 再表示
            self.btn_insert_clicked()
            return

        # 現在のテーマの状態
        theme_record =  self.getThemeCurrentState()

        # プロジェクトのテーマ一覧に記入したテーマーを追加
        QgsProject.instance().mapThemeCollection().insert(new_theme, theme_record)


    def btn_copy_clicked(self):
        '''
        /***************************************************************************
        コピーをクリック時の処理
        ***************************************************************************/
        '''

        # テーマ一覧が空の場合はメッセージ表示
        if self.listWidget.currentItem() is None:
            QMessageBox.warning(self, "コピー", f"テーマを選択してください。", QMessageBox.Ok)
            return

        # ダイアログ表示
        new_theme,ok = QInputDialog.getText(self, "コピー", f"{self.listWidget.currentItem().text()} をコピーしますか?")        
        if ok == False:
            return

        # 入力チェック
        if new_theme == None or new_theme == "":
            QMessageBox.warning(self, "追加", f"テーマ名を入力してください。", QMessageBox.Ok)
            # 再表示
            self.btn_copy_clicked()
            return

        # 存在するテーマの重複管理
        if QgsProject.instance().mapThemeCollection().hasMapTheme(new_theme) == True:
            QMessageBox.warning(self, "コピー", f"入力したテーマ名は重複するため、別のテーマ名を入力してください。", QMessageBox.Ok)
            # 再表示
            self.btn_copy_clicked()
            return

        # コピー元テーマの状態を取得
        theme_record =  QgsProject.instance().mapThemeCollection().mapThemeState(self.listWidget.currentItem().text())

        # プロジェクトのテーマ一覧に記入したテーマーを追加
        QgsProject.instance().mapThemeCollection().insert(new_theme, theme_record)
        

    def btn_delete_clicked(self):
        '''
        /***************************************************************************
        削除をクリック時の処理
        ***************************************************************************/
        '''
        # テーマ一覧が空の場合
        if self.listWidget.currentItem() is None:
            QMessageBox.warning(self, "削除", f"テーマを選択してください。", QMessageBox.Ok)
            return
        
        reply = QMessageBox.question(self, "削除", f"{self.listWidget.currentItem().text()} を削除しますか？ ", QMessageBox.Ok, QMessageBox.No)
        if  reply != QMessageBox.Ok:            
            return

        # プアラグイン側に選択したプロジェクトをプロジェクトから削除
        QgsProject.instance().mapThemeCollection().removeMapTheme(self.listWidget.currentItem().text())



    def btn_save_clicked(self):
        '''
        /***************************************************************************
        保存をクリック時の処理
        ***************************************************************************/
        '''
        # テーマ一覧が空の場合
        if self.listWidget.currentItem() is None:
            QMessageBox.warning(self, "保存", f"テーマを選択してください。", QMessageBox.Ok)
            return

        reply = QMessageBox.question(self, "保存", f"{self.listWidget.currentItem().text()} 現在の状態を置き換えますか？ ", QMessageBox.Ok, QMessageBox.No)
        if  reply != QMessageBox.Ok:
            return

        QgsProject.instance().mapThemeCollection().insert(self.listWidget.currentItem().text(), self.getThemeCurrentState())


    def themeChanged(self):
        '''
        /***************************************************************************
        Qgis側に追加、削除、名前の置き換え、スタイルの変更が行われた場合の処理
        ***************************************************************************/
        '''
        themes_array = []
        for row in range(self.listWidget.count()):
            themes_array.append(self.listWidget.item(row).text())
        
        project_themes = QgsProject.instance().mapThemeCollection().mapThemes()

        # テーマの追加・削除がないので何もしない
        if len(set(themes_array) ^ set(project_themes)) == 0:
            return

        # 現在選択中のテーマの名前を退避する
        if self.listWidget.currentItem() is None:
            selected_theme_text = ""
        else:
            selected_theme_text = self.listWidget.currentItem().text()


        # テーマ一覧を更新
        themes = QgsProject.instance().mapThemeCollection().mapThemes()
        self.listWidget.clear()
        for new_themes in themes:
            self.listWidget.addItem(new_themes)

        if len(selected_theme_text) > 0:
            # 作り直したテーマリストに選択テーマがあれば再度選択状態にする
            items_selected = self.listWidget.findItems(selected_theme_text, Qt.MatchExactly)
            if len(items_selected) > 0:
                self.listWidget.setCurrentItem(items_selected[0])

        # 作り直したテーマリストに適用中のテーマがあれば再度適用中にする
        if len(self.applying_theme_name) > 0:
            items_applied = self.listWidget.findItems(self.applying_theme_name, Qt.MatchExactly)
            if len(items_applied) > 0:
                self.setAppliedItem(items_applied[0])
            else:
                self.applying_theme_name = ""


    def getThemeCurrentState(self):
        '''
        /***************************************************************************
        プロジェクトで現在表示しているテーマ状態を取得
        ***************************************************************************/
        '''
        root = QgsProject.instance().layerTreeRoot()
        model = self.iface.layerTreeView().layerTreeModel()
        
        # テーマのスタイルや状態
        return QgsMapThemeCollection.createThemeFromCurrentState(root, model)


    def updateThemeList(self):
        '''
        /***************************************************************************
        プロジェクト変更時テーマリストを更新
        ***************************************************************************/
        '''
        self.listWidget.clear()
        for map_theme in QgsProject.instance().mapThemeCollection().mapThemes():
            self.listWidget.addItem(map_theme)
     

    def changeMapCollection(self):
        '''
        /***************************************************************************
        プラグインを表示したまま新しいプロジェクトを開くと内容がされる
          mapThemesChangedのシグナルと接続することによって
          テーマの追加、削除、保存、名前変更があった場合に対応
        ***************************************************************************/
        '''
        # Qgis側のシステムにテーマリストに変化があった場合
        QgsProject.instance().mapThemeCollection().mapThemesChanged.connect(self.themeChanged)


    def themeRenamed(self,old_themeName:str, new_themeName:str):
        '''
        /***************************************************************************
        mapCollectionのテーマ名が変更の場合
        ***************************************************************************/
        '''
        if old_themeName == new_themeName:
            new_themeName = old_themeName


    def setAppliedItem(self, item):
        '''
        /***************************************************************************
        適用テーマとして背景色を設定
        ***************************************************************************/
        '''
        if item:
            item.setBackground(Qt.yellow)


    def releaseApplying(self, theme_name: str):
        '''
        /***************************************************************************
        塗りつぶした背景をリセット
        ***************************************************************************/
        '''
        items = self.listWidget.findItems(theme_name, Qt.MatchExactly)
        for item in items:
            item.setBackground(QBrush())


    def closeEvent(self, event):
        '''
        /***************************************************************************
        プラグインを閉じる
        ***************************************************************************/
        '''
        self.closingPlugin.emit()
        event.accept()


