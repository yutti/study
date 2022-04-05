### インポート
import csv
import mysql.connector
 
### ファイルオープン
file = open("bme280_db.csv", "r")
 
### ファイル読み込み
members = csv.reader(file)
 
### DB接続
cnx = mysql.connector.connect(host='localhost', user='root', password='', database='bme280db')
 
### カーソル作成
cursor = cnx.cursor()
 
### INSERT文作成
sql = "INSERT INTO weather_forecast ( date_time, pressure, temperature, humidity) VALUES (%s, %s, %s, %s)"
 
### データ挿入
data_count = 0
for value in members:
        if not data_count == 0:
        ### データ挿入実行
            cursor.execute(sql, value)
        data_count += 1

### コミット
cnx.commit()
 
### カーソルクローズ
cursor.close()
 
### DB切断
cnx.close()
 
### ファイルクローズ
file.close()
