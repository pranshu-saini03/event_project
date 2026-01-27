from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import venue,VenueAvailability
@csrf_exempt
def create_venue(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    if request.role not in ["owner", "admin"]:
        return JsonResponse({"error": "Permission denied"}, status=403)
    data=json.loads(request.body)
    venue1=venue.objects.create(
        owner_id=request.user_id,
        name=data.get('name'),
        state=data.get('state'),
        city=data.get('city')
    )
        # Logic to create a venue
    return JsonResponse(
        {'message': 'Venue created successfully', 
         'venue_id': venue1.id
         }
        ,status=201)

@csrf_exempt
def add_availability(request):
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Only POST method is allowed'},
            status=405
        )
    venue1=venue.objects.get(id=request.GET.get('venue_id'))
    if venue1.owner_id != request.user_id and request.role != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    data=json.loads(request.body)
    availability=VenueAvailability.objects.create(
        venue=venue1,
        date=data.get('date'),
    )
    return JsonResponse({'message': 'Availability added successfully',
                         'availability_id':availability.id}, status=201)


def list_venues(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
    state=request.GET.get('state')
    city=request.GET.get('city')
    venues= venue.objects.all()
    if state:
        venues=venues.filter(state=state)
    if city:
        venues=venues.filter(city=city)
    data=list(venues.values())
    return JsonResponse({'venues':data},status=200)

# Create your views here.
