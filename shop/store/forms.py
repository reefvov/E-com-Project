from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(max_length=250,help_text='example@gmail.com')

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2')


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget = forms.TextInput(attrs={             
      'class':'readonly'
    }))   
    





BANK_CHOICES = [
    ('kbank', 'ธ.กสิกรไทย : 747-2-07355-3'),
    ('ktb', 'ธ.กรุงไทย : 036-0-17652-6'),
    ('scb', 'ธ.ไทยพาณิชย์ : 101-2-44265-0'),
]



class CheckOutForm(forms.Form):
    first_name = forms.CharField(widget = forms.TextInput(attrs={                   #ชื่อ
        'class' : 'form-control',
        'id' : 'firstname'
    }))   

    last_name = forms.CharField(widget = forms.TextInput(attrs={                   #นามสกุล
        'class' : 'form-control',
        'id' : 'lastname'
    }))  
    
    phone = forms.CharField(widget = forms.TextInput(attrs={                  #เบอร์โทร
        'class' : 'form-control',
        'id' : 'phone'
    }))     
    address = forms.CharField(widget = forms.TextInput(attrs={                #ที่อยู่
        'class' : 'form-control',
        'id' : 'address'
    }))          
    city = forms.CharField(widget = forms.TextInput(attrs={                   #ชื่อ
        'class' : 'form-control',
        'id' : 'city'
    }))               
    district = forms.CharField(widget = forms.TextInput(attrs={                   #ชื่อ
        'class' : 'form-control',
        'id' : 'district'
    }))               
    subdistrict = forms.CharField(widget = forms.TextInput(attrs={                   #ชื่อ
        'class' : 'form-control',
        'id' : 'subdistrict'
    }))               
    postcode = forms.CharField(widget = forms.TextInput(attrs={               
        'class' : 'form-control',
        'id' : 'postcode'
    })) 




class PaymentForm(forms.Form):
    slip = forms.ImageField(widget = forms.FileInput(attrs={
        'id' : 'slip'
    }))            

 


        