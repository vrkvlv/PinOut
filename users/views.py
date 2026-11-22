import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("Невдала реєстрація: %s", list(serializer.errors.keys()))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        logger.info("Зареєстровано користувача %s", user.username)
        return Response(
            {"message": "Користувача успішно зареєстровано."},
            status=status.HTTP_201_CREATED,
        )
