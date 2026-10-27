from django.db import models

from catalog.models import Component


class Project(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Легко"),
        ("medium", "Середньо"),
        ("hard", "Складно"),
    ]

    title = models.CharField(max_length=200)
    idea = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    time = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


class ProjectComponent(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_components"
    )
    component = models.ForeignKey(
        Component, on_delete=models.PROTECT, related_name="project_components"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.project} - {self.component}"


class Step(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="steps")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    code = models.TextField(blank=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.project} - крок {self.number}"
