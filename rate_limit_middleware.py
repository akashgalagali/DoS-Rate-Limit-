import time
from collections import defaultdict
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

RATE_LIMIT = 3  # Set the maximum number of allowed requests
TIME_WINDOW = 1  # Define the time window (in seconds) for enforcing the rate limit
BLOCK_DURATION = 20  # Specify the duration (in seconds) for which an IP will be blocked

# Store request timestamps and block information
request_log = defaultdict(list)
blocked_ips = {}

class RateLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        print("Initializing Middleware")
        self.get_response = get_response

    def __call__(self, request):
        print("Rate limit is initiated on IP ",self.get_client_ip(request))
        current_time = time.time()
        client_ip = self.get_client_ip(request)
        
        # Check if the IP is blocked
        if client_ip in blocked_ips:
            block_time = blocked_ips[client_ip]
            if current_time - block_time > BLOCK_DURATION:
                # Unblock after block_duration
                del blocked_ips[client_ip]
                request_log[client_ip] = []  # Clear request logs
            else:
                # return 429 for block list IPs
                return JsonResponse({"error": "IP blocked due to rate limit"}, status=429)

        # Filter requests older than time window
        request_log[client_ip] = [timestamp for timestamp in request_log[client_ip] if current_time - timestamp < TIME_WINDOW]

        # Block IP if rate limit is exceeded
        if len(request_log[client_ip]) >= RATE_LIMIT:
            blocked_ips[client_ip] = current_time  # Record block start time
            return JsonResponse({"error": "Rate limit exceeded, IP blocked for 10 minutes"}, status=429)

        # Log this request
        request_log[client_ip].append(current_time)

        # Proceed with the response
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        #Extract the client's IP address from the request.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip