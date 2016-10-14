from django.db import models
from django.conf import settings

class ThemeManager(models.Manager):
    def by_author(self, user):
        """
        A convenience method for retrieving the themes a user has authored.
        Since the only time we'll be retrieving themes by author is when
        they're being edited, this also limits the query to those themes
        that haven't yet been submitted for review.
        """
        return self.filter(author=self, status=self.model.EDITING)

    def get_current_theme(self, user):
        field_name = getattr(settings, 'THEME_PROFILE_FIELD', 'theme')
        return getattr(user.get_profile(), field_name)
