from django import forms
from poker.detect import PokenHandAnalyzer


class PokerHandDataForm(forms.Form):
    hand_line = forms.CharField(label="Input", required=True)

    def __init__(self, *args, **kwargs):
        super(PokerHandDataForm, self).__init__(*args, **kwargs)
        self.fields["hand_line"].widget.attrs["class"] = "form-control"
        self.fields["hand_line"].widget.attrs["place-holder"] = "form-control"
        self.fields["hand_line"].widget.attrs["aria-describedby"] = "id_hand_line_Status"
        
        self.pa = PokenHandAnalyzer()

    def clean_hand_line(self):
        hand_line = self.cleaned_data.get("hand_line")
        if self.pa.parse(hand_line) is False:
            raise forms.ValidationError(self.pa.parse_error_msg)
        return hand_line

    def parse_result(self):
        return self.pa
