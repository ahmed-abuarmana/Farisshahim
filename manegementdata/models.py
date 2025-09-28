from django.db import models

class Makhbaz(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم المخبز")
    owner_name = models.CharField(max_length=200, verbose_name="اسم المالك")
    address = models.CharField(max_length=300, verbose_name="العنوان")
    mobile_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    created_at = models.DateField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return self.name


class Takiya(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم التكية")
    owner_name = models.CharField(max_length=200, verbose_name="اسم المالك")
    address = models.CharField(max_length=300, verbose_name="العنوان")
    mobile_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    created_at = models.DateField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return self.name


class Taslima(models.Model):
    taslima_date = models.DateField(verbose_name="تاريخ التسليم")
    flour = models.IntegerField(null=True, blank=True, verbose_name="طحين")
    salt = models.IntegerField(null=True, blank=True, verbose_name="ملح")
    yeast = models.IntegerField(null=True, blank=True, verbose_name="خميرة")
    oil = models.IntegerField(null=True, blank=True, verbose_name="زيت")
    wood = models.IntegerField(null=True, blank=True, verbose_name="حطب")
    rice = models.IntegerField(null=True, blank=True, verbose_name="رز")
    beans = models.IntegerField(null=True, blank=True, verbose_name="فاصولياء")
    lentils_red = models.IntegerField(null=True, blank=True, verbose_name="عدس أحمر")
    lentils_black = models.IntegerField(null=True, blank=True, verbose_name="عدس أسود")
    pasta = models.IntegerField(null=True, blank=True, verbose_name="معكرونة")

    # كل تسليمة إما لمخبز أو لتكية (واحدة فقط)
    makhbaz = models.ForeignKey(
        Makhbaz,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='taslimat',
        verbose_name="المخبز"
    )
    takiya = models.ForeignKey(
        Takiya,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='taslimat',
        verbose_name="التكية"
    )

    def __str__(self):
        return f"تسليمة بتاريخ {self.taslima_date}"
