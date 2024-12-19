from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import CACHE_ENABLED
from mailings.models import AttemptMailing, Mailing, Recipient
from users.models import User


def check_photo(photo):
    """
    Проверка веса и формата загружаемой фотографии
    """
    max_size = 5 * 1024 ** 2
    if photo:
        if photo.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5 Мб")
        elif photo.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise ValidationError("Можно загрузить файлы только форматов JPEG, JPG, PNG")
        return photo
    else:
        return False


def get_all_mailings_from_cache():
    """
    Получение списка всех рассылок из кеша / БД
    """
    if not CACHE_ENABLED:
        mailings = Mailing.objects.all()
    else:
        mailings = cache.get("mailings")
        if not mailings:
            mailings = Mailing.objects.all()
            cache.set("mailings", mailings, 5 * 60)
    return mailings.order_by("id")


def get_all_recipients_from_cache():
    """
    Получение списка всех получателей рассылок из кеша / БД
    """
    if not CACHE_ENABLED:
        recipients = Recipient.objects.all()
    else:
        recipients = cache.get("recipients")
        if not recipients:
            recipients = Recipient.objects.all()
            cache.set("recipients", recipients, 5 * 60)
    return recipients.order_by("last_name")


def get_all_users_from_cache():
    """
    Получение списка всех пользователей сервиса рассылок из кеша / БД
    """
    if not CACHE_ENABLED:
        users = User.objects.all()
    else:
        users = cache.get("users")
        if not users:
            users = Recipient.objects.all()
            cache.set("users", users, 5 * 60)
    return users.order_by("id")


def get_recipients_list(mailing: Mailing | None = None):
    """
    Получение списка получателей указанной рассылки
    :param mailing: Рассылка сообщений Mailing
    :return: Список получателей рассылки Recipient
    """
    if mailing:
        recipients = mailing.recipients
    else:
        recipients = get_all_recipients_from_cache()
    return recipients.order_by("last_name")


def send_mailing(mailing_pk: int, user) -> str:
    """
    Отправка рассылки по ключу
    :param mailing_pk: Primary key модели Mailing
    :param user: Текущий пользователь
    :return: Ответ почтового сервера
    """
    mailing = get_object_or_404(Mailing, pk=mailing_pk)
    attempt = AttemptMailing.objects.create(mailing=mailing)
    try:
        send_mail(subject=mailing.message.subject,
                  message=mailing.message.body,
                  from_email=None,
                  recipient_list=[recipient.email for recipient in get_recipients_list(mailing)])
        mailing.status = "started"
        attempt.status = "successful"
        attempt.mail_server_response = "Рассылка успешно отправлена"
    except Exception as e:
        mailing.status = "created"
        attempt.status = "unsuccessful"
        attempt.mail_server_response = e.args[1]
    mailing.save()
    attempt.owner = user
    attempt.save()
    return attempt.mail_server_response


def get_statistic_to_index():
    """
    Сбор статистики для отображения на главной странице
    """
    mailings = get_all_mailings_from_cache()
    mailings_count = mailings.count()
    started_mailings_count = mailings.filter(status="started").count()
    recipients = get_all_recipients_from_cache()
    recipients_count = recipients.count()
    result = {
        "mailings_count": mailings_count,
        "started_mailings_count": started_mailings_count,
        "recipients_count": recipients_count
    }
    return result


def get_personal_statistic(user):
    """
    Сбор статистики для отображения на странице статистики пользователя
    """
    mailings = Mailing.objects.filter(owner=user)
    result = {"mailings": []}
    for mailing in mailings:
        attempts = AttemptMailing.objects.filter(mailing=mailing)
        attempts_count = attempts.count()
        successful_attempts_count = attempts.filter(status="successful").count()
        recipients = get_recipients_list(mailing)
        result["mailings"].append((mailing, (f"было произведено {attempts_count} попыток отправки, "
                                             f"{successful_attempts_count} из них успешны. "
                                             f"В рассылке состояло {len(recipients)} получателей. "
                                             f"Каждый из получателей на данных момент получил "
                                             f"{successful_attempts_count} сообщений.")))
    return result


def add_owner_to_instance(request, form):
    """
    Добавляет в поле owner модели текущего пользователя
    """
    instance = form.save()
    user = request.user
    instance.owner = user
    instance.save()


def get_queryset_for_owner(user, queryset):
    """
    Выборка списка объектов только для их владельцев
    """
    try:
        if user.is_superuser or user.groups.get(name="Managers"):
            return queryset.order_by("id")
    except Group.DoesNotExist:
        return queryset.filter(owner=user).order_by("id")


def check_access_to_view(instance, user):
    """
    Проверка статуса владельца для просмотра объекта
    """
    try:
        if user == instance.owner or user.is_superuser or user.groups.get(name="Managers"):
            return instance
    except Group.DoesNotExist:
        raise PermissionDenied


def check_access_to_delete(instance, user):
    """
    Проверка статуса владельца для удаления объекта
    """
    if user == instance.owner or user.is_superuser:
        return instance
    raise PermissionDenied
