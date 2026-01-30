import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import Booking
from venue.models import venue as Venue, VenueAvailability


@csrf_exempt
def create_booking(request):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Only POST method allowed'},
            status=405
        )

    if request.role != 'user':
        return JsonResponse(
            {'error': 'Only users can book venues'},
            status=403
        )

    data = json.loads(request.body)

    venue_id = data.get('venue_id')
    date = data.get('date')

    if not venue_id or not date:
        return JsonResponse(
            {'error': 'venue_id and date are required'},
            status=400
        )

    try:
        availability = VenueAvailability.objects.get(
            venue_id=venue_id,
            date=date,
            is_booked=False
        )
    except VenueAvailability.DoesNotExist:
        return JsonResponse(
            {'error': 'Venue not available on selected date'},
            status=400
        )

    booking = Booking.objects.create(
        user_id=request.user_id,
        venue_id=venue_id,
        date=date,
        status='booked'
    )

    availability.is_booked = True
    availability.save()

    return JsonResponse(
        {
            'message': 'Booking created successfully',
            'booking_id': booking.id
        },
        status=201
    )


@csrf_exempt
def cancel_booking(request):

    if request.method != 'DELETE':
        return JsonResponse(
            {'error': 'Only DELETE allowed'},
            status=405
        )

    booking_id = request.GET.get('booking_id')

    if not booking_id:
        return JsonResponse(
            {'error': 'booking_id required'},
            status=400
        )

    try:
        booking_id = int(booking_id)
    except ValueError:
        return JsonResponse(
            {'error': 'Invalid booking_id'},
            status=400
        )

    try:
        booking = Booking.objects.select_related('venue').get(id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse(
            {'error': 'Booking not found'},
            status=404
        )

    # permission check
    if request.role == 'admin':
        pass

    elif request.role == 'owner' and booking.venue.owner_id == request.user_id:
        pass

    elif request.role == 'user' and booking.user_id == request.user_id:
        pass

    else:
        return JsonResponse(
            {'error': 'Permission denied'},
            status=403
        )

    if booking.status == 'cancelled':
        return JsonResponse(
            {'error': 'Booking already cancelled'},
            status=400
        )

    booking.status = 'cancelled'
    booking.save()

    VenueAvailability.objects.filter(
        venue_id=booking.venue_id,
        date=booking.date
    ).update(is_booked=False)

    return JsonResponse(
        {'message': 'Booking cancelled successfully'}
    )


@csrf_exempt
def list_bookings(request):

    if request.role == 'admin':
        bookings = Booking.objects.all()

    elif request.role == 'owner':
        bookings = Booking.objects.filter(
            venue__owner_id=request.user_id
        )

    elif request.role == 'user':
        bookings = Booking.objects.filter(
            user_id=request.user_id
        )

    else:
        return JsonResponse(
            {'error': 'Permission denied'},
            status=403
        )

    data = list(
        bookings.values(
            'id',
            'venue__name',
            'date',
            'status'
        )
    )

    return JsonResponse(
        {'bookings': data},
        status=200
    )
