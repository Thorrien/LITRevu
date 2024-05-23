from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from application.models import Ticket, Review, UserBlock, UserFollows
from application.forms import TicketForm, NewReview
from application.forms import ReviewFormfromticket, FollowUserForm
from application.forms import TicketAndReviewForm
from authentication.models import User
from django.db.models import Q


@login_required
def flux(request):
    """
    Affiche le flux des tickets et des critiques pour l'utilisateur connecté.

    Cette vue récupère tous les tickets créés par l'utilisateur connecté ainsi
    que ceux créés par les utilisateurs suivis par l'utilisateur connecté.
    Ensuite, elle récupère toutes les critiques associées à ces tickets ainsi
    que celles créées par l'utilisateur connecté et les utilisateurs suivis.
    Les tickets et les critiques sont triés par date de création dans l'ordre
    décroissant et passés au template 'flux.html' pour l'affichage.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'flux.html' avec le contexte des tickets et des critiques triés par
        date de création.

    Template:
        - flux.html: Affiche les tickets et les critiques de l'utilisateur et
        des utilisateurs suivis.

    Contexte:
        reviewAndTicket (list): Une liste triée par date de création
        décroissante contenant des instances de Ticket et de Review.
    """
    user_follows = UserFollows.objects.filter(user=request.user)
    blocked_users = UserBlock.objects.filter(
        user=request.user).values_list('blocked_user', flat=True)

    tickets = Ticket.objects.filter(
        Q(user__in=user_follows.values('followed_user')) | Q(user=request.user)
    ).exclude(user__in=blocked_users)

    reviews = Review.objects.filter(
        Q(ticket__in=tickets) | Q(user__in=user_follows.values(
            'followed_user')) | Q(user=request.user)
    ).exclude(user__in=blocked_users)

    reviewAndTicket = sorted(chain(reviews, tickets),
                             key=lambda instance: instance.time_created,
                             reverse=True)
    return render(request, 'flux.html', {'reviewAndTicket': reviewAndTicket})


@login_required
def ticket_creation(request):
    """
    Gère la création d'un nouveau ticket par l'utilisateur connecté.

    Cette vue affiche un formulaire permettant à l'utilisateur de créer un
    nouveau ticket. Si la méthode de requête est POST, elle tente de valider
    et de sauvegarder le formulaire. Si le formulaire est valide, le ticket
    est sauvegardé et l'utilisateur est redirigé vers la vue 'flux'. Si la
    méthode de requête est GET, un formulaire vide est affiché.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'ticketcreation.html' avec le contexte du formulaire de création
        de ticket.

    Template:
        - ticketcreation.html: Affiche le formulaire de création de ticket.

    Contexte:
        form (TicketForm): Le formulaire de création de ticket, soit vide,
        soit pré-rempli avec les données soumises en cas de validation échouée.
    """
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
    """
    Gère la modification d'un ticket existant par l'utilisateur connecté.

    Cette vue affiche un formulaire permettant à l'utilisateur de modifier un
    ticket existant. Si la méthode de requête est POST, elle tente de valider
    et de sauvegarder le formulaire. Si le formulaire est valide, le ticket
    est mis à jour et l'utilisateur est redirigé vers la vue 'fluxperso'.
    Si la méthode de requête est GET, le formulaire est pré-rempli avec les
    données du ticket existant.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.
        id (int): L'identifiant unique du ticket à modifier.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'ticketmodify.html' avec le contexte du formulaire de modification
        de ticket.

    Template:
        - ticketmodify.html: Affiche le formulaire de modification de ticket.

    Contexte:
        form (TicketForm): Le formulaire de modification de ticket, soit
        pré-rempli avec les données du ticket existant, soit avec les données
        soumises en cas de validation échouée.
        ticket (Ticket): L'instance du ticket à modifier.
    """
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('fluxperso')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'ticketmodify.html', {'form': form,
                                                 'ticket': ticket})


@login_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('flux')
    return render(request, 'ticketdelete.html', {'ticket': ticket})


@login_required
def review_creation(request):
    """
    Gère la suppression d'un ticket existant par l'utilisateur connecté.

    Cette vue affiche une confirmation avant de supprimer un ticket existant.
    Si la méthode de requête est POST, elle supprime le ticket et redirige
    l'utilisateur vers la vue 'flux'. Si la méthode de requête est GET, elle
    affiche une page de confirmation pour la suppression du ticket.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.
        id (int): L'identifiant unique du ticket à supprimer.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'ticketdelete.html' avec le contexte du ticket à supprimer.

    Template:
        - ticketdelete.html: Affiche une page de confirmation pour
        la suppression du ticket.

    Contexte:
        ticket (Ticket): L'instance du ticket à supprimer.
    """
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
    """
    Gère la modification d'une critique existante par l'utilisateur connecté.

    Cette vue affiche un formulaire permettant à l'utilisateur de modifier une
    critique existante. Si la méthode de requête est POST, elle tente de
    valider et de sauvegarder le formulaire. Si le formulaire est valide,
    la critique est mise à jour et l'utilisateur est redirigé vers la
    vue 'fluxperso'. Si la méthode de requête est GET, le formulaire est
    pré-rempli avec les données de la critique existante.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant
        les informations sur la demande de l'utilisateur.
        id (int): L'identifiant unique de la critique à modifier.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du
        template 'reviewmodify.html' avec le contexte du formulaire de
        modification de critique et du ticket associé.

    Template:
        - reviewmodify.html: Affiche le formulaire de modification de critique.

    Contexte:
        form (ReviewFormfromticket): Le formulaire de modification de critique,
        soit pré-rempli avec les données de la critique existante, soit avec
        les données soumises en cas de validation échouée.
        ticket (Ticket): L'instance du ticket associé à la critique à modifier.
    """
    review = get_object_or_404(Review, id=id)
    ticket = review.ticket
    if request.method == 'POST':
        form = ReviewFormfromticket(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('fluxperso')
    else:
        form = ReviewFormfromticket(instance=review)
    return render(request, 'reviewmodify.html', {'form': form,
                                                 'ticket': ticket})


@login_required
def review_delete(request, id):
    """
    Gère la suppression d'une critique existante par l'utilisateur connecté.

    Cette vue affiche une confirmation avant de supprimer une critique
    existante. Si la méthode de requête est POST, elle supprime la critique
    et redirige l'utilisateur vers la vue 'flux'. Si la méthode de requête
    est GET, elle affiche une page de confirmation pour la suppression de
    la critique.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.
        id (int): L'identifiant unique de la critique à supprimer.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'reviewdelete.html' avec le contexte de la critique à supprimer.

    Template:
        - reviewdelete.html: Affiche une page de confirmation pour la
        suppression de la critique.

    Contexte:
        review (Review): L'instance de la critique à supprimer.
    """
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('flux')
    return render(request, 'reviewdelete.html', {'review': review})


@login_required
def add_user_follow(request):
    """
    Gère l'ajout d'un utilisateur suivi par l'utilisateur connecté.

    Cette vue affiche un formulaire permettant à l'utilisateur de suivre un
    autre utilisateur. Si la méthode de requête est POST, elle tente de
    valider et de sauvegarder le formulaire. Si le formulaire est valide,
    elle vérifie que l'utilisateur à suivre existe et qu'il n'est pas déjà
    suivi par l'utilisateur connecté, puis l'ajoute à la liste des
    utilisateurs suivis. Si la méthode de requête est GET, un formulaire
    vide est affiché.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'follow.html' avec le contexte du formulaire d'ajout d'utilisateur
        suivi et des listes des utilisateurs suivis et des abonnés.

    Template:
        - follow.html: Affiche le formulaire d'ajout d'utilisateur suivi
        ainsi que les listes des utilisateurs suivis et des abonnés.

    Contexte:
        form (FollowUserForm): Le formulaire d'ajout d'utilisateur suivi,
        soit vide, soit pré-rempli avec les données soumises en cas de
        validation échouée.
        user_follows (QuerySet): La liste des utilisateurs suivis par
        l'utilisateur connecté.
        followed_by (QuerySet): La liste des utilisateurs abonnés à
        l'utilisateur connecté.
        message (str, optionnel): Un message indiquant que l'utilisateur
        est déjà suivi.
    """
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            followed_username = form.cleaned_data['username']
            followed_user = User.objects.get(username=followed_username)
            current_user = request.user
            if (current_user != followed_user and
                not UserFollows.objects.filter(
                    user=request.user,
                    followed_user=followed_user).exists()):
                UserFollows.objects.get_or_create(user=current_user,
                                                  followed_user=followed_user)
                return redirect('followUsers')
            else:
                form = FollowUserForm()
                user_follows = UserFollows.objects.filter(user=request.user)
                folloded_by = UserFollows.objects.filter(
                    followed_user=request.user
                    )
                return render(request, 'follow.html', {
                    'user_follows': user_follows,
                    'folloded_by': folloded_by,
                    'message': "Vous êtes déjà abonné à cet utilisateur.",
                    'form': form
                    })
    else:
        form = FollowUserForm()

    user_follows = UserFollows.objects.filter(user=request.user)
    folloded_by = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'follow.html', {
        'form': form,
        'folloded_by': folloded_by,
        'user_follows': user_follows
        })


@login_required
def delete_user_follow(request, id):
    """
    Gère la suppression d'un abonnement utilisateur existant par l'utilisateur
    connecté.

    Cette vue affiche une confirmation avant de supprimer un abonnement
    utilisateur existant. Si la méthode de requête est POST, elle supprime
    l'abonnement et redirige l'utilisateur vers la vue 'followUsers'.
    Si la méthode de requête est GET, elle affiche une page de confirmation
    pour la suppression de l'abonnement.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.
        id (int): L'identifiant unique de l'abonnement à supprimer.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'followdelete.html' avec le contexte de l'abonnement à supprimer.

    Template:
        - followdelete.html: Affiche une page de confirmation pour la
        suppression de l'abonnement.

    Contexte:
        follow (UserFollows): L'instance de l'abonnement utilisateur
        à supprimer.
    """
    follow = get_object_or_404(UserFollows, id=id)
    if request.method == 'POST':
        follow.delete()
        return redirect('followUsers')
    return render(request, 'followdelete.html', {'follow': follow})


@login_required
def ticket_Review_creation(request):
    """
    Gère la création simultanée d'un ticket et d'une critique par
    l'utilisateur connecté.

    Cette vue affiche un formulaire permettant à l'utilisateur de créer à
    la fois un ticket et une critique. Si la méthode de requête est POST,
    elle tente de valider et de sauvegarder le formulaire. Si le formulaire
    est valide, le ticket et la critique sont sauvegardés et l'utilisateur
    est redirigé vers la vue 'flux'. Si la méthode de requête est GET,
    un formulaire vide est affiché.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'ticketreviewcreation.html' avec le contexte du formulaire
        de création de ticket et critique.

    Template:
        - ticketreviewcreation.html: Affiche le formulaire de création de
        ticket et critique.

    Contexte:
        form (TicketAndReviewForm): Le formulaire de création de ticket et
        critique, soit vide, soit pré-rempli avec les données soumises en
        cas de validation échouée.
    """
    if request.method == 'POST':
        form = TicketAndReviewForm(request.POST, request.FILES,
                                   user=request.user)
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
    """
    Gère la création d'une critique pour un ticket existant par
    l'utilisateur connecté.

    Cette vue affiche un formulaire permettant à l'utilisateur de créer une
    critique pour un ticket existant. Si la méthode de requête est POST,
    elle tente de valider et de sauvegarder le formulaire. Si le formulaire
    est valide, la critique est associée au ticket et à l'utilisateur,
    puis sauvegardée. L'utilisateur est ensuite redirigé vers la vue 'flux'.
    Si la méthode de requête est GET, un formulaire vide est affiché.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.
        ticket_id (int): L'identifiant unique du ticket pour lequel
        la critique est créée.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'createreview.html' avec le contexte du formulaire de création
        de critique et du ticket associé.

    Template:
        - createreview.html: Affiche le formulaire de création de critique.

    Contexte:
        form (ReviewFormfromticket): Le formulaire de création de critique,
        soit vide, soit pré-rempli avec les données soumises en cas de
        validation échouée.
        ticket (Ticket): L'instance du ticket pour lequel la critique
        est créée.
    """
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
    return render(request, 'createreview.html', {'form': form,
                                                 'ticket': ticket})


@login_required
def fluxperso(request):
    """
    Affiche le flux personnel des tickets et des critiques de
    l'utilisateur connecté.

    Cette vue récupère tous les tickets et critiques créés par l'utilisateur
    connecté. Les tickets et les critiques sont ensuite triés par date de
    création dans l'ordre décroissant et passés au template 'fluxperso.html'
    pour l'affichage.

    Args:
        request (HttpRequest): L'objet de requête HTTP contenant les
        informations sur la demande de l'utilisateur.

    Returns:
        HttpResponse: Une réponse HTTP contenant le rendu du template
        'fluxperso.html' avec le contexte des tickets et des critiques
        triés par date de création.

    Template:
        - fluxperso.html: Affiche les tickets et les critiques de
        l'utilisateur connecté.

    Contexte:
        reviewAndTicket2 (list): Une liste triée par date de création
        décroissante contenant des instances de Ticket et de Review
        créées par l'utilisateur connecté.
    """
    tickets2 = Ticket.objects.filter(user=request.user)
    reviews2 = Review.objects.filter(user=request.user)
    reviewAndTicket2 = sorted(chain(reviews2, tickets2),
                              key=lambda instance: instance.time_created,
                              reverse=True)

    return render(request, 'fluxperso.html',
                  {'reviewAndTicket2': reviewAndTicket2})


def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    if request.user != user_to_block:
        UserBlock.objects.get_or_create(user=request.user,
                                        blocked_user=user_to_block)
    return redirect('flux')


def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(User, id=user_id)
    UserBlock.objects.filter(user=request.user,
                             blocked_user=user_to_unblock).delete()
    return redirect('flux')
