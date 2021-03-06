from django import forms
from poker.detect import PokerHandAnalyzer

LANG_CODE_CHOICES = (
    ("en", "en"),
    ("jp", "jp")
)


class PokerHandDataForm(forms.Form):
    lang_code = forms.ChoiceField(label="Lang", initial="en", choices=LANG_CODE_CHOICES)
    hand_line = forms.CharField(label="Input", required=True)

    def __init__(self, *args, **kwargs):
        super(PokerHandDataForm, self).__init__(*args, **kwargs)
        self.fields["hand_line"].widget.attrs["class"] = "form-control"
        self.fields["hand_line"].widget.attrs["place-holder"] = "Input"
        self.fields["hand_line"].widget.attrs["AUTOCOMPLETE"] = "OFF"
        self.fields["lang_code"].widget.attrs["class"] = "form-control"

    def clean_hand_line(self):
        hand_line = self.cleaned_data.get("hand_line")
        lang_code = self.cleaned_data.get("lang_code")
        self.pa = PokerHandAnalyzer(lang_code=lang_code)
        if self.pa.parse(hand_line) is False:
            raise forms.ValidationError(self.pa.parse_error_msg)
        return hand_line

    def parse_result(self):
        return self.pa
