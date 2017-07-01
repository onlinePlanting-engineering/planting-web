from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.contrib.auth import get_user_model
from lands.models import Meta as BaseProduct
from django.core.urlresolvers import reverse

User = get_user_model()

class OrderManager(models.Manager):
    pass

class BaseOrder(models.Model):
    TRANSITION_TARGETS = {
        'new': _("New order without content"),
        'created': _("Order freshly created"),
        'payment_confirmed': _("Parment confirmed"),
    }
    decimalfield_kwargs = {
        'max_digits': 30,
        'decimal_places': 2,
    }

    customer = models.ForeignKey(User, verbose_name=_("Customer"), related_name="orders")
    status = models.CharField(default='new', max_length=24, verbose_name=_("Status"))
    subtotal = models.DecimalField(_("Subtotal"), **decimalfield_kwargs)    # 优惠前价格
    total = models.DecimalField(_("Tocal"), **decimalfield_kwargs)          # 优惠后价格
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True)
    is_valid = models.BooleanField(default=True,
                                   help_text=_("will be set to be false automatically if not paid within 45 minutes"))

    objects = OrderManager()

    def __str__(self):
        return self.get_number()

    def __repr__(self):
        return "<{}(pk={})>".format(self.__class__.__name__, self.pk)

    def get_api_url(self):
        return reverse("orders-api:thread", kwargs={'pk': self.id})

    def get_number(self):
        """
        Hook to get the order number.
        """
        return str(self.pk)

    def get_or_assign_number(self):
        """
        Hook to get or to assign the order number. It shall be invoked, every time an Order
        object is created. If you prefer to use an order number which differs from the primary
        key, then override this method.
        """
        return self.get_number()

class OrderPayment(models.Model):
    """
    A model to hold received payments for a given order
    """
    order = models.ForeignKey(BaseOrder, verbose_name=_("Order"))
    amount = models.CharField(_("Amount paid"), max_length=7,
                              help_text=_("How much was paid with this particaular transfer."))
    transaction_id = models.CharField(_("Transaction ID"), max_length=255,
                                      help_text=_("The transaction processor's reference"))
    created_at = models.DateTimeField(_("Received at"), auto_now_add=True)
    payment_method = models.CharField(_("Payment method"), max_length=50,
                                      help_text=_("The payment backend used to process the purchase"))

class OrderItem(models.Model):
    """
    An item for an order
    """
    order = models.ForeignKey(BaseOrder, related_name='items', verbose_name=_("Order"))
    product = models.ForeignKey(BaseProduct, related_name='order_items', default=1, verbose_name=_("Product"))
    product_name = models.CharField(_("Product name"), max_length=255, null=True, blank=True,
                                    help_text=_("Product name at the moment of purchase."))
    product_code = models.CharField(_("Product code"), max_length=255, null=True, blank=True,
                                    help_text=_("Product code at the moment of purchase."))
    unit_price = models.DecimalField(_("Unit price"), null=True,
                                      help_text=_("Products unit price at the moment of purchase."),
                                      **BaseOrder.decimalfield_kwargs)
    quantity = models.SmallIntegerField(_("Quantity"), default=1,
                                     help_text=_("The quantity of the same product purchased"))
    line_total = models.DecimalField(_("Line Total"), null=True,
                                      help_text=_("Line total on the invoice at the moment of purchase."),
                                      **BaseOrder.decimalfield_kwargs)

    def __str__(self):
        return self.product_name

    def get_api_url(self):
        return reverse('orderitem-detail', kwargs={'pk': self.id})