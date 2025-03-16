class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']