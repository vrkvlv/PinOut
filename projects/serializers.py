from rest_framework import serializers

from .models import Project, ProjectComponent, Step


class ProjectComponentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="component.id", read_only=True)
    name = serializers.CharField(source="component.name", read_only=True)

    class Meta:
        model = ProjectComponent
        fields = ["id", "name", "quantity"]


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ["number", "title", "text", "image_url", "code"]


class ProjectSerializer(serializers.ModelSerializer):
    components = ProjectComponentSerializer(
        source="project_components", many=True, read_only=True
    )
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "idea", "difficulty", "time", "components", "steps"]
