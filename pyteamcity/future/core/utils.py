import dateutil.parser
from datetime import timezone

from .. import exceptions


def parse_date_string(date_string):
    if date_string is None:
        return None
    return dateutil.parser.parse(date_string)


def raise_on_status(res):
    if not res.ok:
        raise exceptions.HTTPError(
            status_code=res.status_code, reason=res.reason, text=res.text
        )
