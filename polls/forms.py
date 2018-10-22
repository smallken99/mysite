#_*_ encoding: utf-8 *_*
from django import forms
from polls import models
from django.forms.widgets import HiddenInput,Textarea,DateInput
 
class DTSF04Form(forms.ModelForm):
    class Meta:
        model = models.DTSF04
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DTSF04Form, self).__init__(*args, **kwargs)
        self.fields['DASHBOARD'].label = '電表'
        self.fields['INPUT_DATE'].label = '輸入日期'
        self.fields['LAST_DEGREES'].label = '上次電表度數'
        self.fields['THIS_DEGREES'].label = '本次電表度數'
        self.fields['ELECTRIC_AMT'].label = '總電費'
        self.fields['AVG_AMT'].label = '平均分攤電費'

class DTSF02Form(forms.ModelForm):
    class Meta:
        model = models.DTSF02
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(DTSF02Form, self).__init__(*args, **kwargs)
        self.fields['DTSF01'].label = '房客'
        self.fields['INPUT_DATE'].label = '輸入日期'
        self.fields['LAST_DEGREES'].label = '上次電表度數'
        self.fields['THIS_DEGREES'].label = '本次電表度數'
        self.fields['RENT_AMT'].label = '租金'
        self.fields['PUB_ELECTRIC_AMT'].label = '公共電費'
        self.fields['ELECTRIC_AMT'].label = '個人電費'
        self.fields['DIPOSIT_AMT'].label = '押金'
        self.fields['TOTAL_AMT'].label = '應繳房租'
        self.fields['MESSAGE'].label = '訊息' 
        self.fields['MESSAGE'].widget = Textarea(attrs={'rows':3, 'cols':30})
        self.fields['IS_CONF'].widget = HiddenInput()