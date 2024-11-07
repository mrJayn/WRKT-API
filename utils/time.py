import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime


def strftimedelta(td: datetime.timedelta):
    """Format a datetime.timedelta to a human readable string."""

    mm, _ss = divmod(td.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%02d minutes" % mm

    def _plural(n):
        return n, abs(n) != 1 and "s" or ""

    if hh > 0:
        s = ("%d hour%s : " % _plural(hh)) + s

    if td.days:
        s = ("%d day%s : " % _plural(td.days)) + s

    return s
