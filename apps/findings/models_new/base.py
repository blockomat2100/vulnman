from django.db import models
from vulnman.models import VulnmanModel


SEVERITY_CHOICES = [
    ("critical", 4),
    ("high", 3),
    ("medium", 2),
    ("low", 1),
    ("informational", 0)
]


class VulnerabilityCategory(VulnmanModel):
    name = models.CharField(max_length=128, unique=True)


class VulnerabilityReference(VulnmanModel):
    url = models.URLField()


class CWEEntry(VulnmanModel):
    entry = models.CharField(max_length=32, unique=True)


class BaseVulnerability(VulnmanModel):
    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES)
    name = models.CharField(max_length=256)
    # mitigation = models.TextField()
    description = models.TextField()
    recommendation = models.TextField()
    vulnerability_id = models.CharField(max_length=256)
    cwe_ids = models.ManyToManyField(CWEEntry)
    categories = models.ManyToManyField(VulnerabilityCategory)
    # references = models.ForeignKey(VulnerabiltiyReference)

    class Meta:
        abstract = True