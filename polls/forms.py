#_*_ encoding: utf-8 *_*
from django import forms
from polls import models

 
class ElecForm(forms.ModelForm):
    class Meta:
        model = models.DTSF04
        fields = ['DASHBOARD', 'INPUT_DATE', 'LAST_DEGREES', 'THIS_DEGREES','ELECTRIC_AMT','AVG_AMT']

    def __init__(self, *args, **kwargs):
        super(ElecForm, self).__init__(*args, **kwargs)
        self.fields['DASHBOARD'].label = '電表'
        self.fields['INPUT_DATE'].label = '輸入日期'
        self.fields['LAST_DEGREES'].label = '上次電表度數'
        self.fields['THIS_DEGREES'].label = '本次電表度數'
        self.fields['ELECTRIC_AMT'].label = '總電費'
        self.fields['AVG_AMT'].label = '平均分攤電費'