from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from application.models import Ticket, Review, UserFollows
from application.forms import TicketForm, NewReview, ReviewFormfromticket, FollowUserForm, TicketAndReviewForm
from authentication.models import User
from django.db.models import Q


@login_required
def flux(request):
    user_follows = UserFollows.objects.filter(user=request.user)
    tickets = Ticket.objects.filter(
        Q(user__in=user_follows.values('followed_user')) | Q(user=request.user)
    )
    
    reviews = Review.objects.filter(
        Q(ticket__in=tickets) | Q(user__in=user_follows.values('followed_user')) | Q(user=request.user)
    )

    #tickets = tickets.exclude(pk__in=reviews.values('ticket'))
    
    reviewAndTicket = sorted(chain(reviews, tickets), key=lambda instance: instance.time_created, reverse=True)
    
    return render(request, 'flux.html', {'reviewAndTicket': reviewAndTicket})

@login_required
def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(request, 'ticketdetails.html', {'ticket': ticket})


@login_required
def ticket_creation(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = TicketForm(user=request.user)
    return render(request, 'ticketcreation.html', {'form': form})

@login_required
def ticket_modify(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'ticketmodify.html', {'form': form})


@login_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('flux')
    return render(request, 'ticketdelete.html', {'ticket': ticket})




@login_required
def review_detail(request, id):
    review = Review.objects.get(id=id)
    return render(request, 'reviewdetails.html', {'review': review})


@login_required
def review_creation(request):
    if request.method == 'POST':
        form = NewReview(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = NewReview()
    return render(request, 'reviewcreation.html', {'form': form})


@login_required
def review_modify(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        form = NewReview(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = NewReview(instance=review)
    return render(request, 'reviewmodify.html', {'form': form})


@login_required
def review_delete(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('flux')
    return render(request, 'reviewdelete.html', {'review': review})


@login_required
def add_user_follow(request):
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            followed_username = form.cleaned_data['username']
            followed_user = User.objects.get(username=followed_username)
            current_user = request.user
            if current_user != followed_user and not UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists() :
                UserFollows.objects.get_or_create(user=current_user, followed_user=followed_user)
                return redirect('followUsers')                  
            else:
                form = FollowUserForm()
                user_follows = UserFollows.objects.filter(user=request.user)
                folloded_by = UserFollows.objects.filter(followed_user=request.user)
                return render(request, 'follow.html', {'user_follows': user_follows, 'folloded_by':folloded_by, 'message': "Vous êtes déjà abonné à cet utilisateur.", 'form': form})
    else:
        form = FollowUserForm()

    user_follows = UserFollows.objects.filter(user=request.user)
    folloded_by = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'follow.html', {'form': form, 'folloded_by':folloded_by, 'user_follows': user_follows})


@login_required
def delete_user_follow(request, id):
    follow = get_object_or_404(UserFollows, id=id)
    if request.method == 'POST':
        follow.delete()
        return redirect('followUsers')
    return render(request, 'followdelete.html', {'follow': follow})

@login_required
def ticket_Review_creation(request):
    if request.method == 'POST':
        form = TicketAndReviewForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('flux')
        else:
            print(form.errors)
    else:
        form = TicketAndReviewForm(user=request.user)
    return render(request, 'ticketreviewcreation.html', {'form': form})

@login_required
def create_review_from_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ReviewFormfromticket(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux') 
    else:
        form = ReviewFormfromticket()
    return render(request, 'createreview.html', {'form': form, 'ticket': ticket})