"""Модели каталога — категории и товары магазина."""

from django.db import models
from django.db.models import F


class Category(models.Model):
    """Категория товаров. Отображается на главной странице магазина."""

    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.ImageField(
        upload_to='categories/icons/%Y/%m/',
        blank=True, null=True,
        verbose_name="Иконка категории",
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар магазина. Поддерживает складской учёт и два способа хранения изображений."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products', verbose_name="Категория",
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)

    # Изображение хранится на диске 
    image = models.ImageField(
        upload_to='products/%Y/%m/%d', blank=True,
        verbose_name="Изображение (файл)",
    )
    # Изображение хранится в БД 
    image_data = models.BinaryField(
        blank=True, null=True, verbose_name="Изображение (в БД)",
    )

    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена",
    )
    stock_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во на складе",
    )
    available = models.BooleanField(
        default=True, verbose_name="В наличии",
        help_text="Автоматически отключается при 0 на складе",
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


    def has_stock(self, quantity=1):
        """Проверить наличие количества единиц товара на складе."""
        return self.__class__.objects.filter(
            id=self.id, available=True, stock_quantity__gte=quantity,
        ).exists()

    def reduce_stock_atomic(self, quantity):
        """Списание со склада в одной транзакции.
        Защита от параллельных запросов на покупки.
        Возвращает ``True`` если списание прошло, ``False`` — если нет.
        """
        updated_rows = self.__class__.objects.filter(
            id=self.id,
            available=True,
            stock_quantity__gte=quantity,  
        ).update(
            stock_quantity=F('stock_quantity') - quantity,
        )

        if updated_rows == 0:
            return False

        # Отключить товар если на складе закончился
        current = (
            self.__class__.objects.filter(id=self.id)
            .values_list('stock_quantity', 'available')[0]
        )
        if current[0] <= 0 and current[1]:
            self.__class__.objects.filter(
                id=self.id, available=True,
            ).update(available=False)

        # Обновляем количество товара на складе
        self.stock_quantity = max(0, getattr(self, 'stock_quantity', quantity) - quantity)
        if self.stock_quantity <= 0:
            self.available = False

        return True

    def reduce_stock(self, quantity):
        """Алиас для обратной совместимости. 
        
        См. :meth:`reduce_stock_atomic`."""
        return self.reduce_stock_atomic(quantity)

    def restore_stock(self, quantity):
        """Возврат товаров на склад при отмене заказа."""
        rows = self.__class__.objects.filter(id=self.id).update(
            stock_quantity=F('stock_quantity') + quantity,
        )
        # Включить товар обратно если он был скрыт из-за пустого склада
        if rows:
            current = (
                self.__class__.objects.filter(id=self.id)
                .values_list('stock_quantity', 'available')[0]
            )
            if current[0] > 0 and not current[1]:
                self.__class__.objects.filter(
                    id=self.id, available=False,
                ).update(available=True)

        self.stock_quantity = getattr(self, 'stock_quantity', 0) + quantity
        if self.stock_quantity > 0:
            self.available = True


class SiteSettings(models.Model):
    """Одиночная запись с общими настройками магазина.

    Хранит фоновое изображение и параметры его отображения."""

    BACKGROUND_POSITION_CHOICES = [
        ('center', 'По центру'),
        ('top left', 'Сверху слева'),
        ('top center', 'Сверху по центру'),
        ('top right', 'Сверху справа'),
        ('bottom left', 'Снизу слева'),
        ('bottom center', 'Снизу по центру'),
        ('bottom right', 'Снизу справа'),
    ]

    BACKGROUND_SIZE_CHOICES = [
        ('cover', 'Покрытие — заполнить весь экран'),
        ('contain', 'Вместить целиком'),
        ('100% 100%', 'Растянуть на 100% × 100%'),
    ]

    BACKGROUND_ATTACH_CHOICES = [
        ('fixed', 'Фиксированная'),
        ('scroll', 'Двигается с прокруткой'),
    ]

    # Фоновое изображение для записи в БД
    background_image = models.BinaryField(
        blank=True, null=True, verbose_name="Фоновое изображение",
        help_text=(
            "Загрузите картинку для фона сайта. "
            "Рекомендуемый размер: 1920×1080 px, форматы JPG/PNG."
        ),
    )

    # Размер и масштабирование фона
    background_size = models.CharField(
        max_length=15, choices=BACKGROUND_SIZE_CHOICES,
        default='cover', verbose_name="Масштаб фона",
    )

    # Позиция где разместить фон относительно viewport
    background_position = models.CharField(
        max_length=14, choices=BACKGROUND_POSITION_CHOICES,
        default='center', verbose_name="Позиция фона",
    )

    # Поведение при прокрутке
    background_attach = models.CharField(
        max_length=10, choices=BACKGROUND_ATTACH_CHOICES,
        default='fixed', verbose_name="Тип привязки фона",
    )

   # Насколько затемнить фон поверх контента (0-100 %)
    overlay_opacity = models.PositiveIntegerField(
        default=60, verbose_name="Затемнение, %",
        help_text=(
            "Наложение тёмного слоя поверх картинки. "
            "0 = картинка полностью яркая, 100 = чёрный экран."
        ),
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    @classmethod
    def get(cls):
        """Вернет единственную запись, создав её при необходимости."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    @property
    def has_image(self):
        """Проверка на загруженное фоновое изображение."""
        return bool(self.background_image)

    @property
    def overlay_alpha(self):
        """Alpha-значение для CSS rgba (0.0 – 1.0), строка с точкой."""
        return f'{self.overlay_opacity / 100:.2f}'
