from django.views.generic.base import TemplateView

from dsmr_consumption.models.settings import ConsumptionSettings
from dsmr_datalogger.models.settings import DataloggerSettings
from dsmr_frontend.models.settings import FrontendSettings
from dsmr_weather.models.settings import WeatherSettings
from dsmr_backup.models.settings import BackupSettings, DropboxSettings


class Configuration(TemplateView):
    template_name = 'dsmr_frontend/configuration.html'

    def get_context_data(self, **kwargs):
        context_data = super(Configuration, self).get_context_data(**kwargs)
        context_data['consumption_settings'] = ConsumptionSettings.get_solo()
        context_data['datalogger_settings'] = DataloggerSettings.get_solo()
        context_data['frontend_settings'] = FrontendSettings.get_solo()
        context_data['weather_settings'] = WeatherSettings.get_solo()
        context_data['backup_settings'] = BackupSettings.get_solo()
        context_data['dropbox_settings'] = DropboxSettings.get_solo()
        return context_data