from django.db import models
from django.core.validators import RegexValidator


GOVERNORATE_CHOICES = [
    ("الوسطى", "الوسطى"),
    ("رفح", "رفح"),
    ("خان يونس", "خان يونس"),
]


class Makhbaz(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم المخبز", null=True, blank=True)
    governorate = models.CharField(
        max_length=50,
        choices=GOVERNORATE_CHOICES,
        verbose_name="المحافظة",
        null=True,
        blank=True
    )

    address = models.CharField(max_length=300, verbose_name="العنوان بالتفصيل", null=True, blank=True)
    owner_name = models.CharField(max_length=200, verbose_name="اسم صاحب المخبز", null=True, blank=True)
    owner_id = models.CharField(
        max_length=9,
        validators=[RegexValidator(r'^\d{9}$', "رقم الهوية يجب أن يكون 9 أرقام")],
        verbose_name="رقم هوية صاحب المخبز",
        null=True, blank=True
    )
    mobile_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', "رقم الجوال يجب أن يكون 10 أرقام")],
        verbose_name="رقم الجوال",
        null=True, blank=True
    )
    coordinates = models.CharField(
        max_length=50,
        verbose_name="إحداثيات الموقع",
        null=True, blank=True
    )

    OVEN_TYPE_CHOICES = [
        ("فرن طينة", "مخبز بدائي (فرن طينة)"),
        ("يدوي دوار", "يدوي دوار"),
        ("نص آلي", "نص آلي"),
        ("آلي", "آلي"),
    ]
    oven_type = models.CharField(
        max_length=20,
        choices=OVEN_TYPE_CHOICES,
        verbose_name="نوع الفرن / المخبز",
        null=True, blank=True
    )

    production_capacity = models.PositiveIntegerField(
        verbose_name="القدرة الإنتاجية اليومية (كيلو)",
        null=True, blank=True
    )

    CONTRACT_TYPE_CHOICES = [
        ("مجاني", "مخبز مجاني"),
        ("مدعم", "مخبز مدعوم"),
    ]
    contract_type = models.CharField(
        max_length=10,
        choices=CONTRACT_TYPE_CHOICES,
        verbose_name="طبيعة التعاقد",
        null=True, blank=True
    )

    STATUS_CHOICES = [
        ("فعال", "فعال"),
        ("متوقف", "متوقف"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name="حالة المخبز",
        null=True, blank=True
    )

    created_at = models.DateField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return self.name if self.name else "مخبز غير مسمى"


class Taslima_makhbaz(models.Model):
    taslima_date = models.DateField(verbose_name="تاريخ التسليم")
    
    # مواد التسليم للمخابز كأعداد صحيحة
    flour = models.PositiveIntegerField(null=True, blank=True, verbose_name="طحين (كيلو)")
    yeast = models.PositiveIntegerField(null=True, blank=True, verbose_name="خميرة (علبة)")
    salt = models.PositiveIntegerField(null=True, blank=True, verbose_name="ملح (كيلو)")
    sugar = models.PositiveIntegerField(null=True, blank=True, verbose_name="سكر (كيلو)")
    cooking_oil = models.PositiveIntegerField(null=True, blank=True, verbose_name="زيت قلي (لتر)")
    wood = models.PositiveIntegerField(null=True, blank=True, verbose_name="حطب (كيلو)")
    gas = models.PositiveIntegerField(null=True, blank=True, verbose_name="غاز (كيلو)")
    
    additions = models.TextField(null=True, blank=True, verbose_name="إضافات")
    
    until_date = models.DateField(null=True, blank=True, verbose_name="حتى تاريخ")

    # كل تسليمة مرتبطة بمخبز واحد
    makhbaz = models.ForeignKey(
        Makhbaz,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='taslimat',
        verbose_name="المخبز"
    )
    
    def __str__(self):
        return f"تسليمة بتاريخ {self.taslima_date} للمخبز: {self.makhbaz.name if self.makhbaz else 'غير محدد'}"




# ====================================================





class Takiya(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="اسم المطبخ / التكية",
        null=True, blank=True
    )

    GOVERNORATE_CHOICES = [
        ("رفح", "رفح"),
        ("خان يونس", "خان يونس"),
        ("الوسطى", "المحافظة الوسطى"),
    ]
    governorate = models.CharField(
        max_length=50,
        choices=GOVERNORATE_CHOICES,
        verbose_name="المحافظة",
        null=True, blank=True
    )

    address = models.CharField(
        max_length=300,
        verbose_name="العنوان بالتفصيل",
        null=True, blank=True
    )

    owner_name = models.CharField(
        max_length=200,
        verbose_name="اسم صاحب التكية",
        null=True, blank=True
    )

    owner_id = models.CharField(
        max_length=9,
        validators=[RegexValidator(r'^\d{9}$', "رقم الهوية يجب أن يكون 9 أرقام")],
        verbose_name="رقم هوية صاحب التكية",
        null=True, blank=True
    )

    mobile_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', "رقم الجوال يجب أن يكون 10 أرقام")],
        verbose_name="رقم الجوال",
        null=True, blank=True
    )

    coordinates = models.CharField(
        max_length=50,
        verbose_name="إحداثيات الموقع",
        null=True, blank=True
    )

    # العدد الكلي للقدور
    total_pots = models.PositiveIntegerField(
        verbose_name="إجمالي عدد القدور",
        null=True, blank=True
    )

    # عدد القدور لكل سعة
    pots_80 = models.PositiveIntegerField(
        verbose_name="عدد القدور سعة 80 لتر",
        null=True, blank=True
    )
    pots_100 = models.PositiveIntegerField(
        verbose_name="عدد القدور سعة 100 لتر",
        null=True, blank=True
    )
    pots_120 = models.PositiveIntegerField(
        verbose_name="عدد القدور سعة 120 لتر",
        null=True, blank=True
    )
    pots_150 = models.PositiveIntegerField(
        verbose_name="عدد القدور سعة 150 لتر",
        null=True, blank=True
    )
    pots_200 = models.PositiveIntegerField(
        verbose_name="عدد القدور سعة 200 لتر",
        null=True, blank=True
    )

    daily_capacity = models.PositiveIntegerField(
        verbose_name="القدرة الإنتاجية اليومية (بالقدر)",
        null=True, blank=True
    )

    STATUS_CHOICES = [
        ("فعال", "فعال"),
        ("متوقف", "متوقف"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name="حالة التكية",
        null=True, blank=True
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    def __str__(self):
        return self.name if self.name else "تكية غير مسماة"
    


class Taslima_takiya(models.Model):
    taslima_date = models.DateField(verbose_name="تاريخ التسليم")

    # مواد التسليم للتكيات كأعداد صحيحة
    salt = models.PositiveIntegerField(null=True, blank=True, verbose_name="ملح (كيلو)")
    macaroni = models.PositiveIntegerField(null=True, blank=True, verbose_name="معكرونة (كيلو)")
    rice = models.PositiveIntegerField(null=True, blank=True, verbose_name="رز (كيلو)")
    oil = models.PositiveIntegerField(null=True, blank=True, verbose_name="زيت (لتر)")
    peas = models.PositiveIntegerField(null=True, blank=True, verbose_name="بازيلا (علبة 400 جم)")
    lentils = models.PositiveIntegerField(null=True, blank=True, verbose_name="عدس مجروش (كيلو)")
    beans = models.PositiveIntegerField(null=True, blank=True, verbose_name="لوبيا حب (كيلو)")
    sauce = models.PositiveIntegerField(null=True, blank=True, verbose_name="صلصة (علبة 800 جم)")
    luncheon = models.PositiveIntegerField(null=True, blank=True, verbose_name="لانشون (علبة 300 جم)")
    maggi_spice = models.PositiveIntegerField(null=True, blank=True, verbose_name="بهار ماجي (كيلو)")
    vegetable_soup = models.PositiveIntegerField(null=True, blank=True, verbose_name="شوربة خضار (كيلو)")
    seven_spices = models.PositiveIntegerField(null=True, blank=True, verbose_name="٧ بهارات (كيلو)")
    ghee = models.PositiveIntegerField(null=True, blank=True, verbose_name="سمنة (علبة)")
    bulgur = models.PositiveIntegerField(null=True, blank=True, verbose_name="برغل (كيلو)")

    vegetable = models.TextField(null=True, blank=True, verbose_name="خضار")
    amount_of_vegetables = models.PositiveIntegerField(null=True, blank=True, verbose_name="كمية الخضار")

    additions = models.TextField(null=True, blank=True, verbose_name="إضافات")
    
    until_date = models.DateField(null=True, blank=True, verbose_name="حتى تاريخ")


    # كل تسليمة مرتبطة بتكية واحدة
    takiya = models.ForeignKey(
        Takiya,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='taslimat',
        verbose_name="التكية"
    )

    def __str__(self):
        return f"تسليمة بتاريخ {self.taslima_date} للتكية: {self.takiya.name if self.takiya else 'غير محدد'}"

