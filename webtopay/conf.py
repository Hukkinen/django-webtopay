from django.conf import settings


class WebToPaySettingsError(Exception):
    "Raised when WebToPay settings are incorrect"

# Mandatory part
try:
    WTP_PASSWORD = settings.WEBTOPAY_PASSWORD
except:
    raise WebToPaySettingsError("Please provide WEBTOPAY_PASSWORD in settings")

CHECK_SS1 = getattr(settings, 'WEBTOPAY_CHECK_SS1', True)
CHECK_SS2 = getattr(settings, 'WEBTOPAY_CHECK_SS2', True)
SUBMIT_TARGET_BLANK = getattr(settings, 'WEBTOPAY_SUBMIT_TARGET_BLANK', False)

POSTBACK_ENDPOINT = getattr(
    settings, "WEBTOPAY_POSTBACK_ENDPOINT", "https://www.mokejimai.lt/pay/"
)
