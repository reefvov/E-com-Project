# E-com-Project


---------- ต้องมี python ในเครื่อง -----------
เปิด cmd
pip python (น่าจะมีอยู่แล้ว)


---------- สร้าง environment ------------
pip install virtualenv
สร้างfolderเปล่าชื่อDjangoProject แล้วกดเข้าไปในfolder
พิมพ์ cmd ในช่องdirectoryแล้ว Enter   #(จะขึ้นหน้าจอ cmd ที่มีpathเป็นfolder ของproject)
mkvirtaulenv env    #(env = ชื่อ environment จะใช้ชื่ออื่นก็ได้)
workon env

---------- ติดตั้ง django ----------------
pip install django
django-adminstartproject shop


----------- คัดลอกไฟล์ ----------------
เปิดไฟล์ที่โหลดมาจาก github
ลากไฟล์ทั้ง 2 ไฟล์ (shop และ .vscode) มาใส่ โฟล์เดอร์ DjangoProject
ถ้าคอมแจ้งเตือนชื่อไฟล์ซ้ำกัน เลือกแทนที่ไฟล์เก่าไปเลย

---------- ใช้ vscode -----------------
เปิด vscode 
เปิดfolder DjangoProject
ตั้งค่าให้ autosave (File --> Auto Save)

---------- เชื่อมต่อ DB ----------------
ติดตั้ง postgresql
เปิด pgAdmin4
สร้าง server ชื่อ ECOM_SERVER
ใช้ Hostname เป็น localhost
ตั้ง port เป็น 5432
ใช้ ีuser เป็น postgres
password เป็น 1234
สร้าง database ชื่อ ECOM_DB

---------- pip เพิ่มเติม --------------
เปิด vscode ที่พักไว้
เลือก run ไฟล์ไหนก็ได้ที่เป็น .py  #(ตรง terminalจะแจ้งเจ๊งตัวแดงบาน)
ไปที่ส่วน terminal ด้านล้างใน vscode
เช็คด้วยว่า terminal เปลี่ยนจาก powershell เป็น python รึยัง
พิมพ์ในterminalตามนี้
cd shop    แล้วกดEnter
หลังจากนั้นpip ที่ละตัว
pip install django-crispy-forms
pip install psycopg2
python -m pip install Pillow
pip install django-mptt


----------- Migration DB ----------
พิมพ์ต่อที่ terminal (ทีละบรรทัด)
python manage.py makemigrations
python manage.py migrate


------------- เปิด webapp --------
python manage.py runserver
กดเปิดlink http://127.0.0.1:8000/


---------- complete ------------



