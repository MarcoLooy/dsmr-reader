import warnings

from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig
from django.db import connection
from django.conf import settings

from dsmr_backend.dto import MonitoringStatusIssue
from dsmr_backend.signals import request_status


class BackendAppConfig(AppConfig):
    """ The backend app solely exists for triggering a backend signal. """
    name = 'dsmr_backend'
    verbose_name = _('Backend (dsmr_backend)')

    def ready(self):
        """ Performs an DB engine check, as we maintain some engine specific queries. """
        if (connection.vendor not in settings.DSMRREADER_SUPPORTED_DB_VENDORS):  # pragma: no cover
            # Temporary for backwards compatibility
            warnings.showwarning(
                _(
                    'Unsupported database engine "{}" active, '
                    'some features might not work properly'.format(connection.vendor)
                ),
                RuntimeWarning, __file__, 0
            )


@receiver(request_status)
def on_request_status(**kwargs):
    from dsmr_backend.models.schedule import ScheduledProcess

    issues = []
    offset = timezone.now() - timezone.timedelta(
        minutes=settings.DSMRREADER_STATUS_ALLOWED_SCHEDULED_PROCESS_LAGG_IN_MINUTES
    )
    lagging_processes = ScheduledProcess.objects.filter(
        active=True,
        planned__lt=offset
    )

    for current in lagging_processes:
        issues.append(
            MonitoringStatusIssue(
                __name__,
                'Process behind schedule: {}'.format(current.name),
                current.planned
            )
        )

    return issues
