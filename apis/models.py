from django.db import models


# Create your models here.
class Killer(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    speed = models.FloatField(verbose_name="이동 속도(m/s)", default=4.6)
    terror_radius = models.PositiveIntegerField(default=32, verbose_name="공포범위(m/s)")
    img_url = models.URLField(verbose_name="이미지 url", blank=True)
    note = models.TextField(verbose_name='비고', blank=True)
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self):
        return self.name


class Survivor(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    speed = models.FloatField(verbose_name='이동 속도(m/s)', default=4.0)
    img_url = models.URLField(verbose_name="이미지 url", blank=True)
    note = models.TextField(verbose_name='비고', blank=True)
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    killer = models.OneToOneField(Killer, on_delete=models.CASCADE, null=True, blank=True)
    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.killer is not None:
            return self.killer.name
        return self.survivor.name


class Perk(models.Model):
    """
    title, title_kor, description, 살인마/생존자, img_url,
    """

    CATEGORY = (("Killer", "Killer"), ("Survivor", "Survivor"))
    name = models.CharField(max_length=256, unique=True, verbose_name="영문 퍽 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 퍽 이름")
    description = models.TextField()
    owner = models.ForeignKey(
        Owner, on_delete=models.SET_NULL, null=True, verbose_name="퍽 소유자"
    )
    killer_or_survivor = models.CharField(max_length=256, choices=CATEGORY, default="Killer")
    img_url = models.URLField(verbose_name="이미지 url", blank=True)
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    dt_modified = models.DateTimeField(auto_now=True, verbose_name="date modified")

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self):
        return self.name


# models.SET_NULL = 참조된 객체가 지워지면 null 상태로 둔다.
# models.PROTECT = 참조된 객체가 지워지지 않도록 PROTECT 상태로 둔다.
# models.CASCADE = 참조된 객체가 지워지면 함께 지운다.

class Item(models.Model):
    NORMAL, UNUSUAL, RARE, VERY_RARE, GREATLY_RARE, EVENT = 1, 2, 3, 4, 5, 6
    RARITY = (
        (NORMAL, "평범한"),
        (UNUSUAL, "평범하지 않은"),
        (RARE, "희귀한"),
        (VERY_RARE, "아주 희귀한"),
        (GREATLY_RARE, "굉장히 희귀한"),
        (EVENT, "이벤트"),
    )
    name = models.CharField(max_length=100, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    durability = models.IntegerField(default=0, verbose_name="내구도")
    rarity = models.IntegerField(choices=RARITY, default=1, verbose_name="희귀도")
    description = models.TextField(verbose_name="설명")
    item_category = models.ForeignKey(
        ItemCategory,
        verbose_name="아이템 카테고리",
        null=True,
        on_delete=models.SET_NULL,
    )
    img_url = models.URLField(verbose_name="이미지 url", blank=True)
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self):
        return self.name


class ItemAddon(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    description = models.TextField(verbose_name="설명")
    item_category = (
        models.ForeignKey(
            ItemCategory,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            verbose_name="아이템 카테고리",
        ),
    )
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    perk = models.OneToOneField(Perk, null=True, blank=True, on_delete=models.CASCADE)
    killer = models.OneToOneField(Killer, null=True, blank=True, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, null=True, blank=True, on_delete=models.CASCADE)
    item_addon = models.OneToOneField(ItemAddon, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.perk:
            return self.perk.title
        elif self.item:
            return self.item.name
        return self.item_addon.name
