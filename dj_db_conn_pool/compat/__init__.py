try:
    from django.utils.translation import ugettext_lazy as gettext_lazy
except ImportError:
    from django.utils.translation import gettext_lazy
