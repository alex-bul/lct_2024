# imagegen/models.py
from django.contrib.auth.models import User
from django.db import models


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    image = models.TextField()
    channel = models.CharField(max_length=255, blank=True)  # Поле для канала
    product = models.CharField(max_length=255, blank=True)  # Поле для продукта
    gender = models.FloatField(blank=True)  # Поле для "Пол клиента"
    age = models.FloatField(blank=True)  # Поле для "Возраст клиента"
    cnt_tr_all_3m = models.FloatField(blank=True)  # Поле для "Транз. за 3м"
    cnt_tr_top_up_3m = models.FloatField(blank=True)  # Поле для "Пр. оп. за 3м"
    cnt_tr_cash_3m = models.FloatField(blank=True)  # Поле для "Количество операций выдачи наличных за последние 3 месяца"
    cnt_tr_buy_3m = models.FloatField(blank=True)  # Поле для "Количество операций оплаты покупок за последние 3 месяца"
    cnt_tr_mobile_3m = models.FloatField(blank=True)  # Поле для "Количество операций оплаты связи за последние 3 месяца"
    cnt_tr_oil_3m = models.FloatField(blank=True)  # Поле для "Количество операций оплаты на АЗС за последние 3 месяца"
    cnt_tr_on_card_3m = models.FloatField(blank=True)  # Поле для "Количество операций переводов по карте за последние 3 месяца"
    cnt_tr_service_3m = models.FloatField(blank=True)  # Поле для "Количество операций оплаты услуг за последние 3 месяца"
    sum_zp_12m = models.FloatField(blank=True)  # Поле для "Сумма зарплатных поступлений за 12m"
    app_vehicle_ind = models.FloatField(blank=True)  # Поле для "Наличие авто"
    created_at = models.DateTimeField(auto_now_add=True)  # Поле для даты создания

    def __str__(self):
        return f"{self.id} - {self.session.user.username} - {self.channel} - {self.category} - {self.product}"
