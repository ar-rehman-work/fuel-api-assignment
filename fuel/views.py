from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from fuel.serializers import RegisterSerializer

class RegisterView(APIView):
    """
    Public POST endpoint to create a new user account.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        return Response({"message": "User created successfully.", "username": user.username}, status=status.HTTP_201_CREATED)
