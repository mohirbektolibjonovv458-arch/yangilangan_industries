from django import forms

from .models import ContactMessage, WholesaleOrder

INPUT_CLASSES = (
    "w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-800 "
    "placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 "
    "outline-none transition"
)


class WholesaleOrderForm(forms.ModelForm):
    class Meta:
        model = WholesaleOrder
        fields = ['name', 'phone', 'company_name', 'product', 'quantity', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': 'Ismingiz familyangiz'
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': '+998 90 123 45 67'
            }),
            'company_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': 'Korxona nomi (ixtiyoriy)'
            }),
            'product': forms.Select(attrs={'class': INPUT_CLASSES}),
            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': 'Miqdor (dona)', 'min': 1
            }),
            'comment': forms.Textarea(attrs={
                'class': INPUT_CLASSES, 'placeholder': "Qo'shimcha izoh", 'rows': 4
            }),
        }
        labels = {
            'name': 'Ism familya',
            'phone': 'Telefon raqam',
            'company_name': 'Korxona nomi (ixtiyoriy)',
            'product': 'Mahsulot',
            'quantity': 'Miqdor',
            'comment': 'Izoh',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = self.fields['product'].queryset.model.objects.filter(is_active=True)
        self.fields['company_name'].required = False
        self.fields['comment'].required = False


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': 'Ismingiz'
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': '+998 90 123 45 67'
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES, 'placeholder': 'email@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': INPUT_CLASSES, 'placeholder': 'Xabaringiz', 'rows': 5
            }),
        }
        labels = {
            'name': 'Ism',
            'phone': 'Telefon',
            'email': 'Email',
            'message': 'Xabar',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['email'].required = False
