from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Espacio,Ingreso,Egreso

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

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['tipo_ingreso', 'fuente_ingreso', 'monto_ingreso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))

class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ('tipo_egreso', 'fuente_egreso', 'monto_egreso')
        
    def __init__(self, *args, **kwargs):
        super(EgresoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Guardar'))