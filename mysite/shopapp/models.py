from django.db import models

class User(models.Model):
    class Meta:
        db_table = "account_user"

    user_id = models.CharField(verbose_name="会員ID", max_length=128, primary_key=True, db_index=True)
    password = models.CharField(verbose_name="パスワード", max_length=255)
    name = models.CharField(verbose_name="名前", max_length=127)
    address = models.CharField(verbose_name="住所", max_length=255)

class Category(models.Model):
    class Meta:
        db_table = "shopping_category"
    
    category_id = models.IntegerField(verbose_name="カテゴリID", primary_key=True)
    name = models.CharField(verbose_name="カテゴリ名", max_length=255)

class Item(models.Model):
    class Meta:
        db_table = "shopping_item"
    
    item_id = models.IntegerField(verbose_name="商品ID", primary_key=True)
    name = models.CharField(verbose_name="商品名", max_length=127)
    manufacturer = models.CharField(verbose_name="メーカー名", max_length=31)
    color = models.CharField(verbose_name="商品の色", max_length=15)
    price = models.IntegerField(verbose_name="価格")
    stock = models.IntegerField(verbose_name="在庫数")
    recommended = models.BooleanField(verbose_name="オススメ", default=False)
    category = models.ForeignKey(Category, verbose_name='カテゴリID', on_delete=models.CASCADE)
    
class Cart(models.Model):
    class Meta:
        db_table = "shopping_itemincart"
    
    amount = models.IntegerField(verbose_name="数量")
    booked_date = models.DateTimeField(verbose_name="登録日", auto_now_add=True)
    item = models.ForeignKey(Item, verbose_name='商品ID', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='会員ID', on_delete=models.CASCADE)
    
class Purchase(models.Model):
    class Meta:
        db_table = "shopping_purchase"
    
    purcharse_id = models.IntegerField(verbose_name="注文ID", primary_key=True)
    destination = models.CharField(verbose_name="配送先", max_length=255)
    booked_date = models.DateTimeField(verbose_name="注文日", auto_now_add=True)
    cancel = models.BooleanField(verbose_name='キャンセル', default=False)
    user = models.ForeignKey(User, verbose_name='注文者', on_delete=models.CASCADE)

class Detail(models.Model):
    class Meta:
        db_table = "shopping_purchasedetail"
    
    purchase_detail_id = models.IntegerField(verbose_name="注文詳細ID", primary_key=True)
    amount = models.IntegerField(verbose_name="注文数")
    item = models.ForeignKey(Item, verbose_name='商品ID', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, verbose_name='注文ID', on_delete=models.CASCADE)

class Admin(models.Model):
    class Meta:
        db_table = "administrator_admin"
    
    admin_id = models.CharField(verbose_name="管理者ID",max_length=127, primary_key=True)
    password = models.CharField(verbose_name="パスワード", max_length=255)