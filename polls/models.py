from django.db import models

# python manage.py makemigrations polls
# python manage.py sqlmigrate polls 0001
# python manage.py migrate

# Create your models here.
class Question(models.Model):
    room = models.CharField(max_length=4)
    ChName = models.CharField(max_length=20)
    begin_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    rent_amt = models.IntegerField(default=0)

 
# 房屋租賃契約書
class DTSF01(models.Model):
	ROOM = models.CharField(max_length=3)
	BEGIN_DATE = models.CharField(max_length=10)
	NAME = models.CharField(max_length=20)
	END_DATE = models.CharField(max_length=10)
	CELL_PHONE = models.CharField(max_length=10)
	RENT_AMT = models.IntegerField(default=0)
	DIPOSIT = models.IntegerField(default=0)
	PUB_DASHBOARD = models.CharField(max_length=3,blank=True)
	THIS_DEGREES = models.IntegerField(default=0)
	TIMES = models.FloatField(default=0.0)
	ADDRESS = models.CharField(max_length=50)
	STATUS = models.CharField(max_length=1)

	def __str__(self):
		return self.ROOM + self.NAME

# 繳費紀錄表
class DTSF02(models.Model):
	DTSF01 = models.ForeignKey(DTSF01, on_delete=models.CASCADE)
	INPUT_DATE = models.CharField(max_length=10)
	# ROOM = models.CharField(max_length=3)
	# NAME = models.CharField(max_length=20)
	LAST_DEGREES = models.IntegerField(default=0)
	THIS_DEGREES = models.IntegerField(default=0)
	RENT_AMT = models.IntegerField(default=0)
	PUB_ELECTRIC_AMT = models.IntegerField(default=0)
	ELECTRIC_AMT =  models.IntegerField(default=0)
	DIPOSIT_AMT =  models.IntegerField(default=0)
	TOTAL_AMT =  models.IntegerField(default=0)
	MESSAGE = models.CharField(max_length=200)
	IS_CONF = models.BooleanField(default=False)


# 公共電表基本資料
class DTSF03(models.Model):
	DASHBOARD = models.CharField(max_length=3)
	THIS_DEGREES = models.IntegerField(default=0)
	TIMES = models.FloatField(default=0.0)
	AVG_NUM = models.IntegerField(default=0)

# 公共電表度數紀錄表
class DTSF04(models.Model):
	DASHBOARD = models.CharField(max_length=3) # 電表
	INPUT_DATE = models.CharField(max_length=10) # 輸入日期
	LAST_DEGREES = models.IntegerField(default=0) # 上次度數
	THIS_DEGREES = models.IntegerField(default=0) #	本次度數
	ELECTRIC_AMT =  models.IntegerField(default=0) # 總電費金額
	AVG_AMT =  models.IntegerField(default=0) # 平均分攤金額 
	
	def __str__(self):
		return "<" + self.DASHBOARD + ">" + self.INPUT_DATE
