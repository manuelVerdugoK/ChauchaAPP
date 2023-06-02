from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Espacio

class EspacioForm(forms.ModelForm):
    class Meta:
        model = Espacio
        fields = ['nombre', 'descripcion']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'crear-espacio-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''  # Dejar en blanco para la misma URL
        self.helper.layout = Layout(
            'nombre',
            'descripcion',
            Submit('submit', 'Aceptar', css_class='btn btn-success'),
            # Si quieres incluir el botón "Cancelar", puedes agregarlo aquí
        )
