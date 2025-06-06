from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import math

def is_prime(n):
    
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

class PrimeCheckAPIView(APIView):
   
    
    def get(self, request):
        """Handle GET request with query parameter"""
        try:
            number_str = request.query_params.get('number')
            
            if not number_str:
                return Response({
                    'error': 'Missing parameter',
                    'message': 'Please provide a "number" query parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate input
            try:
                number = int(number_str)
            except (ValueError, TypeError):
                return Response({
                    'error': 'Invalid number format',
                    'message': f'"{number_str}" is not a valid integer'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return self._check_prime_number(number)
            
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Handle POST request with JSON body"""
        try:
            serializer = PrimeCheckSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'error': 'Validation error',
                    'message': 'Invalid input data',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            number = serializer.validated_data['number']
            return self._check_prime_number(number)
            
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _check_prime_number(self, number):
        
        if number < 0:
            return Response({
                'error': 'Invalid input',
                'message': 'Number must be non-negative'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if number > 10**12:
            return Response({
                'error': 'Number too large',
                'message': 'Number must be less than 10^12 for performance reasons'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if prime
        prime_result = is_prime(number)
        
        # Return successful response
        response_data = {
            'number': number,
            'is_prime': prime_result,
            'message': f'{number} is {"a prime" if prime_result else "not a prime"} number'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

# Function-based view alternative

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class CachedPrimeCheckAPIView(PrimeCheckAPIView):
    """Cached version of PrimeCheckAPIView for better performance"""
    pass
