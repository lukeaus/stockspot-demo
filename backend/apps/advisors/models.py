from django.db import models


class Licensee(models.Model):
    """
    Key Assumption:
        - Licensee to Advisor is one-to-many
    """
    name = models.CharField(max_length=255)
    licensee_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Advisor(models.Model):
    name = models.CharField(max_length=255)
    advisor_id = models.CharField(max_length=255)
    licensee = models.ForeignKey(Licensee, related_name='advisors')

    class Meta:
        unique_together = ('advisor_id', 'licensee')

    def __str__(self):
        return '{} - {}'.format(self.name, self.licensee)
