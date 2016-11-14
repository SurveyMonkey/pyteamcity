import dateutil.parser

from .. import exceptions


def parse_date_string(date_string):
    return dateutil.parser.parse(date_string)


def raise_on_status(res):
    if not res.ok:
        raise exceptions.HTTPError(
            status_code=res.status_code, reason=res.reason, text=res.text
        )
