"""Контекстные процессоры главного приложения."""

from .models import SiteSettings


def site_settings(request):
    """Добавляет глобальные настройки сайта в контекст всех шаблонов.

    Передаёт объект ``SiteSettings`` (фон, затемнение и т.д.), чтобы
    шаблон ``base.html`` мог рендерить фоновое изображение.
    """
    return {'site_settings': SiteSettings.get()}
