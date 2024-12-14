from django.forms import ModelForm

from .models import Message, Mailing, AttemptMailing, Recipient


class MessageForm(ModelForm):
    """
    Форма для создания и редактирования сообщения рассылки
    """
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Тема сообщения"
        })
        self.fields["body"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Текст сообщения",
            "rows": 8
        })


class RecipientForm(ModelForm):
    """
    Форма для создания и редактирования получателя рассылки
    """
    class Meta:
        model = Recipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы при инициализации
        """
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email"
        })
        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Имя"
        })
        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Фамилия"
        })
        self.fields["middle_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Отчество"
        })
        self.fields["comment"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Комментарий",
            "rows": 5
        })
