from io import StringIO

from django.core.management import call_command


class managepy(object):
    def make_migrations(self, app=""):
        """Execute makemigration command"""
        out = StringIO()
        try:
            call_command(F"makemigrations {app}", stdout=out)
        except EOFError as e:
            # Shell display choice for default value
            return 'Some "Field" is missing default value'
        return out.getvalue()

    def migrate(self, app=""):
        """Execute migrate command"""
        out = StringIO()
        call_command(F"migrate {app}", stdout=out)
        return out.getvalue()
