import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import venue, VenueAvailability
from accounts.models import OwnerPermission


def check_owner_permission(user_id, perm_type):

    perm = (
        OwnerPermission.objects
        .select_related("permission")
        .filter(owner_id=user_id)
        .first()
    )

    if not perm:
        return False


    if perm_type == "create":
        return perm.permission.create

    if perm_type == "update":
        return perm.permission.update

    if perm_type == "delete":
        return perm.permission.delete

    return False


@csrf_exempt
def create_venue(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    if request.role not in ['owner', 'admin']:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    if request.role == 'owner':
        if not check_owner_permission(request.user_id, "create"):
            return JsonResponse({'error': 'Create permission denied'}, status=403)

    data = json.loads(request.body)

    name = data.get('name')
    state = data.get('state')
    city = data.get('city')

    if not name or not state or not city:
        return JsonResponse(
            {'error': 'name, state and city are required'},
            status=400
        )

    if venue.objects.filter(
        name=name,
        state=state,
        city=city
    ).exists():
        return JsonResponse(
            {'error': 'Venue with same name already exists in this city'},
            status=400
        )

    venue1 = venue.objects.create(
        owner_id=request.user_id,
        name=name,
        state=state,
        city=city
    )

    return JsonResponse({
        'message': 'Venue created successfully',
        'venue_id': venue1.id
    }, status=201)


 
@csrf_exempt
def update_venue(request):

    if request.method != 'PUT':
        return JsonResponse({'error': 'Only PUT allowed'}, status=405)

    venue_id = request.GET.get('venue_id')

    if not venue_id:
        return JsonResponse({'error': 'venue_id required'}, status=400)

    try:
        venue1 = venue.objects.get(id=venue_id)
    except venue.DoesNotExist:
        return JsonResponse({'error': 'Venue not found'}, status=404)

    if request.role == 'admin':
        pass

    elif request.role == 'owner' and venue1.owner_id == request.user_id:
        if not check_owner_permission(request.user_id, "update"):
            return JsonResponse({'error': 'Update permission denied'}, status=403)

    else:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if venue.objects.filter(
        name=data.get('name'),
        state=data.get('state'),
        city=data.get('city')
    ).exclude(id=venue1.id).exists():
        return JsonResponse(
            {'error': 'Venue with same name already exists in this city'},
            status=400
        )
    venue1.name = data.get('name', venue1.name)
    venue1.state = data.get('state', venue1.state)
    venue1.city = data.get('city', venue1.city)

    venue1.save()

    return JsonResponse({'message': 'Venue updated successfully'})


@csrf_exempt
def delete_venue(request):

    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE allowed'}, status=405)

    venue_id = request.GET.get('venue_id')

    if not venue_id:
        return JsonResponse({'error': 'venue_id required'}, status=400)

    try:
        venue1 = venue.objects.get(id=venue_id)
    except venue.DoesNotExist:
        return JsonResponse({'error': 'Venue not found'}, status=404)

    # permission check
    if request.role == 'admin':
        pass

    elif request.role == 'owner' and venue1.owner_id == request.user_id:
        if not check_owner_permission(request.user_id, "delete"):
            return JsonResponse({'error': 'Delete permission denied'}, status=403)

    else:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    venue1.delete()

    return JsonResponse({'message': 'Venue deleted successfully'})


@csrf_exempt
def add_availability(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    venue_id = request.GET.get('venue_id')

    if not venue_id:
        return JsonResponse({'error': 'venue_id required'}, status=400)

    try:
        venue1 = venue.objects.get(id=venue_id)
    except venue.DoesNotExist:
        return JsonResponse({'error': 'Venue not found'}, status=404)

    if venue1.owner_id != request.user_id and request.role != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)

    data = json.loads(request.body)
    date = data.get('date')

    if not date:
        return JsonResponse({'error': 'date is required'}, status=400)

    if VenueAvailability.objects.filter(
        venue=venue1,
        date=date
    ).exists():
        return JsonResponse(
            {'error': 'This date already exists for this venue'},
            status=400
        )

    availability = VenueAvailability.objects.create(
        venue=venue1,
        date=date
    )

    return JsonResponse({
        'message': 'Availability added successfully',
        'availability_id': availability.id
    }, status=201)


def list_venues(request):

    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    state = request.GET.get('state')
    city = request.GET.get('city')

    venues = venue.objects.all()
    if request.role == 'owner':
        venues = venue.objects.filter(owner_id=request.user_id)

    if state:
        venues = venues.filter(state=state)

    if city:
        venues = venues.filter(city=city)

    return JsonResponse({
        'venues': list(venues.values())
    }, status=200)
