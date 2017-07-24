from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.contrib.auth import get_user_model
from lands.models import Meta as BaseProduct
from django.core.urlresolvers import reverse
from datetime import datetime

User = get_user_model()

class OrderManager(models.Manager):
    def create_from_orderitems(self):
        pass

class BaseOrder(models.Model):
    TRANSITION_TARGETS = (
        ('new', _("空订单")),
        ('waiting_payment', _("等待付款")),
        ('check_needed', _("等待对账")),  # 用户支付成功后，但后台验证不通过，需要对账
        ('payment_confirmed', _("确认支付")),
    )

    decimalfield_kwargs = {
        'max_digits': 30,
        'decimal_places': 2,
    }

    number = models.PositiveIntegerField(verbose_name=_("订单标号"), null=True, default=None, unique=True)
    customer = models.ForeignKey(User, verbose_name=_("客户"), related_name="orders")
    status = models.CharField(default='new', max_length=24, verbose_name=_("订单状态"), choices=TRANSITION_TARGETS)
    subtotal = models.DecimalField(_("优惠前总价"), **decimalfield_kwargs)
    total = models.DecimalField(_("优惠后总价"), **decimalfield_kwargs)
    created_at = models.DateTimeField(_("创建日期"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新日期"), auto_now=True)
    is_valid = models.BooleanField(default=True,
                                   help_text=_("如果指定时间内未付款，自动设置成 False, 并释放订单产品"))

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
        return '{0}-{1}'.format(str(self.number)[:4], str(self.number)[4:])

    def get_or_assign_number(self):
        """
        Hook to get or to assign the order number. It shall be invoked, every time an Order
        object is created. If you prefer to use an order number which differs from the primary
        key, then override this method.
        """
        if self.number is None:
            epoch = datetime.now().date()
            epoch = epoch.replace(epoch.year, 1, 1)
            qs = BaseOrder.objects.filter(number__isnull=False, created_at__gt=epoch)
            qs = qs.aggregate(models.Max('number'))

            try:
                epoc_number = int(str(qs['number__max'])[4:]) + 1
                self.number = int('{0}{1:05d}'.format(epoch.year, epoc_number))
            except (KeyError, ValueError):
                # the first order this year
                self.number = int('{0}00001'.format(epoch.year))
            return self.get_number()
        return self.get_number()

    @classmethod
    def resolve_number(cls, number):
        number = number[:4] + number[5:]
        return dict(number=number)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.get_or_assign_number()
        super(BaseOrder, self).save(*args, **kwargs)

class OrderPayment(models.Model):
    """
    A model to hold received payments for a given order
    """
    order = models.ForeignKey(BaseOrder, verbose_name=_("订单"))
    amount = models.CharField(_("支付金额"), max_length=7,
                              help_text=_("How much was paid with this particaular transfer."))
    transaction_id = models.CharField(_("Transaction ID"), max_length=255,
                                      help_text=_("The transaction processor's reference"))
    created_at = models.DateTimeField(_("支付订单创建时间"), auto_now_add=True)
    payment_method = models.CharField(_("支付方式"), max_length=50,
                                      help_text=_("The payment backend used to process the purchase"))

class OrderItemManager(models.Manager):
    pass

class OrderItem(models.Model):
    """
    An item for an order
    """
    order = models.ForeignKey(BaseOrder, related_name='items', verbose_name=_("订单"))
    product = models.ForeignKey(BaseProduct, related_name='order_items', default=1, verbose_name=_("产品"))
    product_code = models.CharField(_("产品编号"), max_length=255, null=True, blank=True,
                                    help_text=_("购买时产品的标号"))
    unit_price = models.DecimalField(_("产品单价"), null=True,
                                      help_text=_("购买时产品的单价"),
                                      **BaseOrder.decimalfield_kwargs)
    quantity = models.SmallIntegerField(_("购买数量"), default=1,
                                     help_text=_("购买时的数量"))
    line_total = models.DecimalField(_("总价"), null=True,
                                      help_text=_("促销时总价"),
                                      **BaseOrder.decimalfield_kwargs)

    objects = OrderItemManager()

    def __str__(self):
        return self.product_code

    def get_api_url(self):
        return reverse('orderitem-detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_code = self.product.num
            self.unit_price = self.product.price
            self.line_total = self.quantity * self.unit_price

        super(OrderItem, self).save(*args, **kwargs)