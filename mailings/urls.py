from django.urls import path

from . import views
from .apps import MailingsConfig

app_name = MailingsConfig.name

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/detail/<int:pk>", views.MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("messages/update/<int:pk>", views.MessageUpdateView.as_view(), name="message_update"),
    path("messages/delete/<int:pk>", views.MessageDeleteView.as_view(), name="message_delete"),

    path("recipients/", views.RecipientListView.as_view(), name="recipient_list"),
    path("recipients/detail/<int:pk>", views.RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipients/create/", views.RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/update/<int:pk>", views.RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/delete/<int:pk>", views.RecipientDeleteView.as_view(), name="recipient_delete"),
]
