import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import (
    analyze_review_sentiments,
    get_request,
    post_review,
)


logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 405,
                "message": "POST required",
            },
            status=405,
        )

    data = json.loads(request.body)

    username = data.get("userName", "")
    password = data.get("password", "")

    user = authenticate(
        username=username,
        password=password,
    )

    if user is not None:
        login(request, user)

        return JsonResponse(
            {
                "userName": username,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "status": "Authenticated",
            }
        )

    return JsonResponse(
        {
            "userName": username,
            "status": "Failed",
        },
        status=401,
    )


@csrf_exempt
def logout_request(request):
    logout(request)

    return JsonResponse(
        {
            "userName": "",
            "status": "Logged out",
        }
    )


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 405,
                "message": "POST required",
            },
            status=405,
        )

    data = json.loads(request.body)

    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if User.objects.filter(
        username=username
    ).exists():

        return JsonResponse(
            {
                "userName": username,
                "error": "Already Registered",
            },
            status=409,
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    login(request, user)

    return JsonResponse(
        {
            "userName": username,
            "firstName": first_name,
            "lastName": last_name,
            "status": "Authenticated",
        }
    )


def get_dealerships(request, state="All"):
    if state == "All":
        dealerships = get_request(
            "/fetchDealers"
        )
    else:
        dealerships = get_request(
            f"/fetchDealers/{state}"
        )

    return JsonResponse(
        {
            "status": 200,
            "dealers": dealerships,
        }
    )


def get_dealer_details(request, dealer_id):
    dealerships = get_request(
        f"/fetchDealer/{dealer_id}"
    )

    return JsonResponse(
        {
            "status": 200,
            "dealer": dealerships,
        }
    )


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(
        f"/fetchReviews/dealer/{dealer_id}"
    )

    for review in reviews:
        sentiment = analyze_review_sentiments(
            review.get("review", "")
        )

        review["sentiment"] = sentiment.get(
            "sentiment",
            "neutral",
        )

    return JsonResponse(
        {
            "status": 200,
            "reviews": reviews,
        }
    )


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 405,
                "message": "POST required",
            },
            status=405,
        )

    if request.user.is_anonymous:
        return JsonResponse(
            {
                "status": 403,
                "message": "Unauthorized",
            },
            status=403,
        )

    data = json.loads(request.body)

    try:
        saved_review = post_review(data)

        return JsonResponse(
            {
                "status": 200,
                "review": saved_review,
            }
        )

    except Exception as error:
        logger.exception(error)

        return JsonResponse(
            {
                "status": 500,
                "message": "Error posting review",
            },
            status=500,
        )


def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    models = CarModel.objects.select_related(
        "car_make"
    ).all()

    cars = []

    for model in models:
        cars.append(
            {
                "CarMake": model.car_make.name,
                "CarModel": model.name,
                "CarType": model.type,
                "CarYear": model.year,
            }
        )

    return JsonResponse(
        {
            "CarModels": cars,
        }
    )