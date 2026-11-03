from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response({"message": "Користувача успішно зареєстровано."}, status=status.HTTP_201_CREATED)
