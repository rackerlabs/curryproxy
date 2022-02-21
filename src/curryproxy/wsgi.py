# Included for convenience. Loads conf files from the default location
# of /etc/curryproxy.
#
# Example usage: `gunicorn curryproxy.wsgi:app`
#
# FIXME: Not sure how to appropriately test this; presumably
# /etc/curryproxy isn't guaranteed to be available in tox tests. Maybe a
# chroot?

from curryproxy import CurryProxy

app = CurryProxy()
