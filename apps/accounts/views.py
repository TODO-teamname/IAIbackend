from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status, generics 
# Create your views here.

class RegisterView(generics.CreateAPIView):
    """Creates a user"""
    serializer_class = RegisterSerializer

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        #print(request.data)
        if serializer.is_valid(raise_exception=True):
            #print(serializer.errors)
            user=serializer.save()  
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:    
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
