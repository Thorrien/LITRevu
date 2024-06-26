from application.models import Ticket, Review
from django import forms
from authentication.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if self.user:
            ticket.user = self.user
        if commit:
            ticket.save()
        return ticket


class NewReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class FollowUserForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username


class SearchUserForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur à suivre',
                               max_length=150)


class TicketAndReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(label='Rating',
                               choices=[(i, str(i)) for i in range(6)],
                               widget=forms.RadioSelect)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    headline = forms.CharField(label='Headline', max_length=128)
    body = forms.CharField(label='Body', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self):
        ticket = super().save(commit=False)
        ticket.user = self.user
        ticket.save()
        review = Review.objects.create(
            ticket=ticket,
            rating=self.cleaned_data['rating'],
            user=self.user,
            headline=self.cleaned_data['headline'],
            body=self.cleaned_data['body']
        )
        return ticket, review


class ReviewFormfromticket(forms.ModelForm):
    rating = forms.ChoiceField(label='Rating',
                               choices=[(i, str(i)) for i in range(6)],
                               widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Headline'}),
            'body': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Body'}),
        }
