import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="jobsearach-mysql-server-jobs.h.aivencloud.com",
  password="AVNS_ro5gQNnPaH3uQNf_sw7",
  read_timeout=timeout,
  port=16459,
  user="avnadmin",
  write_timeout=timeout,
)
  
try:
  cursor = connection.cursor()
  cursor.execute("show databases")
  print(cursor.fetchall())
finally:
  connection.close()