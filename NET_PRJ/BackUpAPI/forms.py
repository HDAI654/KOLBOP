from django import forms

class flogin(forms.Form):
    def __init__(self, *args, **kwargs):
        super(flogin, self).__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.field.widget.attrs['class'] = 'form-control'
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput)