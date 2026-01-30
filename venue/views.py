import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import venue, VenueAvailability
from accounts.models import OwnerPermission
from venue.decorator import owner_permission_required


@csrf_exempt
@owner_permission_required("create")
def create_venue(request):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST allowed'},
            status=405
        )

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

    return JsonResponse(
        {
            'message': 'Venue created successfully',
            'venue_id': venue1.id
        },
        status=201
    )


@csrf_exempt
@owner_permission_required("update")
def update_venue(request):

    if request.method != 'PUT':
        return JsonResponse(
            {'error': 'Only PUT allowed'},
            status=405
        )

    venue_id = request.GET.get('venue_id')

    if not venue_id:
        return JsonResponse(
            {'error': 'venue_id required'},
            status=400
        )

    try:
        venue1 = venue.objects.get(id=venue_id)
    except venue.DoesNotExist:
        return JsonResponse(
            {'error': 'Venue not found'},
            status=404
        )

    # owner must own the venue
    if request.role == 'owner' and venue1.owner_id != request.user_id:
        return JsonResponse(
            {'error': 'Not your venue'},
            status=403
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )

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

    return JsonResponse(
        {'message': 'Venue updated successfully'}
    )


@csrf_exempt
@owner_permission_required("delete")
def delete_venue(request):

    if request.method != 'DELETE':
        return JsonResponse(
            {'error': 'Only DELETE allowed'},
            status=405
        )

    venue_id = request.GET.get('venue_id')

    if not venue_id:
        return JsonResponse(
            {'error': 'venue_id required'},
            status=400
        )

    try:
        venue1 = venue.objects.get(id=venue_id)
    except venue.DoesNotExist:
        return JsonResponse(
            {'error': 'Venue not found'},
            status=404
        )

    if request.role == 'owner' and venue1.owner_id != request.user_id:
        return JsonResponse(
            {'error': 'Not your venue'},
            status=403
        )

    venue1.is_delete = True
    venue1.save()

    return JsonResponse(
        {'message': 'Venue deleted successfully'}
    )


@csrf_exempt
def add_availability(request):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST allowed'},
            status=405
        )

    venue_id = request.GET.get('venue_id')

    if not venue_id:
        return JsonResponse(
            {'error': 'venue_id required'},
            status=400
        )

    try:
        venue1 = venue.objects.get(id=venue_id)
    except venue.DoesNotExist:
        return JsonResponse(
            {'error': 'Venue not found'},
            status=404
        )

    if venue1.owner_id != request.user_id and request.role != 'admin':
        return JsonResponse(
            {'error': 'Permission denied'},
            status=403
        )

    data = json.loads(request.body)
    date = data.get('date')

    if not date:
        return JsonResponse(
            {'error': 'date is required'},
            status=400
        )

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

    return JsonResponse(
        {
            'message': 'Availability added successfully',
            'availability_id': availability.id
        },
        status=201
    )


@csrf_exempt
def list_venues(request):

    if request.method != 'GET':
        return JsonResponse(
            {'error': 'Only GET allowed'},
            status=405
        )

    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('size', 10)

    state = request.GET.get('state')
    city = request.GET.get('city')

    venues = venue.objects.all().order_by('id')

    if request.role == 'owner':
        venues = venues.filter(owner_id=request.user_id)

    if state:
        venues = venues.filter(state=state)

    if city:
        venues = venues.filter(city=city)

    paginator = Paginator(venues, page_size)
    page_object = paginator.get_page(page_number)

    return JsonResponse(
        {
            "total_records": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_object.number,
            "venues": list(page_object.object_list.values())
        },
        status=200
    )
