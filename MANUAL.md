# 地図テーマ編集プラグイン 利用マニュアル

## 起動

プラグインメニューから「地図のテーマ編集」をクリックします。
<BR>
画面右側にウィジェット画面が表示されます。

![](images/image_00.PNG)


## ウィジェット画面詳細

![](images/image_01_a.PNG) 

|    |    |
| ---- | ---- |
| テーマ一覧 | QGISプロジェクトが保持している地図のテーマ内容一覧 |
| 適用 | 一覧で選択したテーマを適用します |
| 追加 | 現在の状態でテーマを追加します |
| コピー | 一覧で選択したテーマをコピーします |
| 削除 | 一覧で選択したテーマを削除します |
| 保存 | 一覧で選択したテーマを現在の状態で保存（変更）します |

※一覧内容はレイヤ欄と一致します。（下記はサンプルです）

![](images/image_01_b.PNG)

## 適用

適用前（地図は[地理院地図](http://cyberjapandata.gsi.go.jp/)）

![](images/image_02.PNG)

ここでは、レイヤ選択状態を例としています。<BR>
「テーマ２」を選択し「適用」ボタンをクリックします。すると、"海岸線"レイヤのみが表示されます。

![](images/image_03.PNG)


「テーマ３」を選択し「適用」ボタンをクリックします。すると、基盤地図レイヤのみが表示されます。

![](images/image_03_b.PNG)



## 追加

「追加」ボタンをクリックすると、下記のような入力ダイアログが表示されます。

![](images/image_08.PNG)

テーマ名を記入して、「OK」ボタンをクリックすると、下記のように追加されます。

![](images/image_08_b.PNG)

![](images/image_08_c.PNG)

未入力の場合は、下記のようなエラーメッセージが表示されます。

![](images/image_08_d.PNG)

## コピー

テーマを選択し「コピー」ボタンをクリックすると、下記のような入力ダイアログが表示されます。

![](images/image_04.PNG)

テーマ名を記入して、「OK」ボタンをクリックすると、下記のように追加されます。

![](images/image_04_b.PNG)


## 削除

テーマを選択し「削除」ボタンをクリックすると、下記のような入力ダイアログが表示されます。

![](images/image_05.PNG)

「OK」ボタンをクリックすると、下記のように削除されます。

![](images/image_05_b.PNG)


## 保存

レイヤの表示状態を変更し、テーマを選択し「保存」ボタンをクリックすると、下記のような入力ダイアログが表示されます。

![](images/image_06.PNG)

「OK」ボタンをクリックすると、内容が変更されます。

## QGIS側の操作とも連動

QGIS側の操作で、テーマを追加・削除などをすると、本プラグインのウィジェット画面にも反映されます。<BR>
例）追加

![](images/image_09_a.PNG)

![](images/image_09_b.PNG)



## プロジェクト変更

プロジェクトを変更すると、テーマ一覧も該当するテーマに変更されます。
<BR>
下記は新規にした場合

![](images/image_07.PNG)
