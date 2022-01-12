try:
    # A legacy compatibility wrapper for Unicode handling on Python 2.
    # "ugettext_lazy" has been removed since Django 4.0.
    from django.utils.translation import ugettext_lazy as gettext_lazy
except ImportError:
    # Django 4.0
    from django.utils.translation import gettext_lazy
