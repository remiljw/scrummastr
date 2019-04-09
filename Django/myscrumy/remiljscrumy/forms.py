from django.forms import ModelForm
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#importing our ModelForms from django
from .models import User, GoalStatus, ScrumyGoals
#importing your models from models.py
class SignupForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True,)
	last_name = forms.CharField(max_length=30, required=True, )
	email = forms.EmailField(max_length=254,)
	# password = forms.CharField(widget=forms.PasswordInput)
	# password1= forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
	class Meta:
    #to specify the model and field that is being imported into the class SignupForm 
		model = User
		fields = ['username','first_name','last_name','email','password1','password2']#port fields in the model User

# class CreateGoalForm(ModelForm):

# 	#to specify the model and field that is being imported into the class CreateGoalForm
# 		class Meta:
# 		   model = ScrumyGoals
# 		   fields = ['goal_name','user','goal_id','goal_status']

class MoveGoalForm(ModelForm):

      class Meta:
      	model = ScrumyGoals
      	fields = ['goal_name','goal_status','user']

      	# def __str__(self):
       #  	form.goal_name= ScrumyGoals.objects.get(goal_id=goal_id)
       #  	return self.goal_name

class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']

# class AddGoalForm(ModelForm):
#     class Meta:
#         model = ScrumyGoals
#         fields = ['goal_name', 'goal_status']

# class MoveGoalForm(ModelForm):
#     class Meta:
#         model = ScrumyGoals
#         fields = ['goal_status']

class DevMoveGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminChangeGoalForm(forms.ModelForm):
	queryset = GoalStatus.objects.all()
	goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

	class Meta:
		model = GoalStatus
		fields = ['goal_status']

class AdminChangeForm(forms.ModelForm):
	queryset = GoalStatus.objects.all()
	goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])

	class Meta:
		model = GoalStatus
		fields = ['goal_status']


class OwnerChangeForm(forms.ModelForm):

	class Meta:
		model = ScrumyGoals
		fields = ['goal_status']

class QAChangegoal(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[::1][:3]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QAChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:4][::4]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class QAMoveForm(forms.ModelForm):
  queryset = GoalStatus.objects.all()
  goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])

  class Meta:
    model = GoalStatus
    fields = ['goal_status']

# class QAChangeGoalForm(ModelForm):
#     class Meta:
#         model = ScrumyGoals
#         fields = ['goal_status', 'user']
