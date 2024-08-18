from django import forms

from backendApp.module.qrcodeCreate import generate_qr_code
from ..models import TurnPoint, QRCodePoint, ActionType, Patient, RouteCondition

class TurnPointForm(forms.ModelForm):
    turn_point_name = forms.CharField(
        max_length=100,
        label="事件名稱",
        widget=forms.TextInput(attrs={'placeholder': '請輸入事件名稱'})
    )

    action_type = forms.ModelChoiceField(
        queryset=ActionType.objects.all(),
        widget=forms.Select,
        label="動作類型"
    )

    patient = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_patients'}),
        label="被照護者",
        required=False
    )

    class Meta:
        model = TurnPoint
        fields = ['turn_point_name', 'action_type', 'patient']

    def __init__(self, *args, **kwargs):
        super(TurnPointForm, self).__init__(*args, **kwargs)
            
        self.fields['turn_point_name'].label = "事件名稱"
        self.fields['patient'].label = "觸發條件(對象)"
        self.fields['action_type'].label = "執行動作"

    def save(self, commit=True):
        turn_point = super(TurnPointForm, self).save(commit=False)

        if commit:
            turn_point.save() 

            qr_code_data = f"TurnPoint-{turn_point.turn_point_id}"
            qr_code_image_path = generate_qr_code(qr_code_data)

            action_type = self.cleaned_data['action_type']

            qr_code_point = QRCodePoint.objects.create(
                qr_code_image=qr_code_image_path,
                action_type=action_type
            )

            turn_point.qr_point = qr_code_point
            turn_point.save()

            patients = self.cleaned_data['patient']
            for patient in patients:
                RouteCondition.objects.create(patient=patient, turn_point=turn_point)

        return turn_point
