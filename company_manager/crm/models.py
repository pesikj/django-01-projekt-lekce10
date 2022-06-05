from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Address(models.Model):
    street = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

class Company(models.Model):
    status_choices = (
        ("N", _("New")),
        ("L", _("Lead")),
        ("O", _("Opportunity")),
        ("C", _("Active Customer")),
        ("FC", _("Former Customer")),
        ("I", _("Inactive")),
    )
    name = models.CharField(_("Name"), max_length=20)
    status = models.CharField(_("Status"), max_length=2, default="N", choices=status_choices)
    phone_number = models.CharField(_("Phone Number"),max_length=20, null=True, blank=True)
    email = models.CharField(_("Email"),max_length=50, null=True, blank=True)
    identification_number = models.CharField(_("Identification Number"),max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    notes = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

class Contact(models.Model):
    primary_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")


class Opportunity(models.Model):
    status_choices = (
        ("1", "Prospecting"),
        ("2", "Analysis"),
        ("3", "Proposal"),
        ("4", "Negotiation"),
        ("5", "Closed Won"),
        ("0", "Closed Lost"),
    )

    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    sales_manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    primary_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(_("Description"), null=True)
    status = models.CharField(_("Status"), max_length=2, default="1", choices=status_choices)
    value = models.DecimalField(_("Value"), max_digits=10, decimal_places=2, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    # Tvorba atributu přesunuta z lekce do cvičení
    phone_number = models.CharField(max_length=20, blank=True)
    office_number = models.CharField(max_length=10, blank=True)
    manager = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=Opportunity)
def create_opportunity(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Byla vytvořena nová opportunita',
            f'Byla vytvořena opportunita pro zákazníka {instance.company.name}',
            'robot@mojefirma.cz',
            ["sales_manager@czechitas.cz"]
        )
