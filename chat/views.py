from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from pyarrow._flight import Ticket

from tutorial.models import Course


@login_required
def course_chat_room(request, course_id):
    # chat rooms of tutorials
    try:
        # retrieve course with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()
    # retrieve chat history
    latest_messages = course.chat_messages.select_related("user").order_by(
        "-id",
    )[:5]
    latest_messages = reversed(latest_messages)
    return render(
        request,
        "chat/room.html",
        {"course": course, "latest_messages": latest_messages},
    )


"""
@login_required
def support_chat_room(request, ticket_id):
    # chat rooms of support ticket
    try:
        # retrieve ticket with given id opened by the current user
    except Ticket.DoesNotExist:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()
    # retrieve chat history
    latest_messages = ticket.chat_messages.select_related("user").order_by(
        "-id",
    )[:5]
    latest_messages = reversed(latest_messages)
    return render(
        request,
        "chat/room.html",
        {"ticket_id": ticket_id, "latests_message": latest_message},
    )
"""
