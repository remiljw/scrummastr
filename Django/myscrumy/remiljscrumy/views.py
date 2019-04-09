from django.shortcuts import render,redirect,get_object_or_404
from remiljscrumy.models import *
from django.http import JsonResponse,HttpResponse,Http404,HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.models  import User,Group
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import viewsets,status, views,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from remiljscrumy.serializers import *
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
#from django.core.exceptions import ObjectDoesNotExist 

# Create your views here.

def index(request):
	# scrumygoals = ScrumyGoals.objects.all()
	# return HttpResponse(scrumygoals)
    if request.method == 'POST':
    #this is a method used to send data to the server   
        form = SignupForm(request.POST)
        #creates the form instance and bounds form data to it
        if form .is_valid():#used to validate the form
            #add_goal = form.save(commit=False)#save an object bounds in the form
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # password2 = form.cleaned_data.get('password1')
            # if password2 != raw_password:
            #     raise form.Http404('password must match')
            user = authenticate(username=username, password=raw_password)
            user.is_staff=True
            login(request,user)
            g = Group.objects.get(name='Developer')
            g.user_set.add(request.user)
            user.save()
            return redirect('home')
    else:
        form = SignupForm()#creates an unbound form with an empty data
    return render(request, 'remiljscrumy/index.html', {'form': form})


def filterArg(request):
    output = ScrumyGoals.objects.filter(goal_name='Learn Django')
    return HttpResponse(output)


def move_goal(request, goal_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
    dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
    current = request.user
    group = current.groups.all()[0]
    # form1 = QAMoveForm()
    try:
        goal = ScrumyGoals.objects.get(goal_id=goal_id)
    except ObjectDoesNotExist:
        notexist = 'A record with that goal id does not exist'
        context = {'not_exist': notexist}
        return render(request, 'remiljscrumy/exception.html', context)
    if group == Group.objects.get(name='Developer') and current == goal.user:
        form = DevMoveGoalForm()
        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
            form = DevMoveGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goal.goal_status = choice
                goal.save()
                return HttpResponseRedirect(reverse('home'))

        else:
            form = DevMoveGoalForm()
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'current_user': current, 'group': group})
    # if group == Group.objects.get(name='Developer') and current != goal.user:
    #     form = DevMoveGoalForm()

    #     if request.method == 'GET':
    #         notexist = 'YOU DO NO NOT HAVE THE PERMISSION TO CHANGE OTHER USERS GOAL'
    #         context = {'not_exist': notexist}
    #         return render(request, 'remiljscrumy/exception.html', context)

    if group == Group.objects.get(name='Admin') and current == goal.user:
        form = AdminChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = AdminChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        else:
            form = AdminChangeGoalForm()
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'current_user': current, 'group': group})


    if group == Group.objects.get(name='Admin') and current != goal.user:
        form = AdminChangeForm()
        if request.method == 'GET':
                return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = AdminChangeForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        else:
                form = AdminChangeForm()
                return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'currentuser': current, 'group': group})
   




    if group == Group.objects.get(name='Owner'):
        form = OwnerChangeForm()

        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = OwnerChangeForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        else:
            form = OwnerChangeForm()
            return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'current_user': current,  'group': group})
    # else:
    #     notexist = 'You cannot move other users goals'
    #     context = {'not_exist': notexist}
    #     return render(request, 'maleemmyscrumy/exception.html', context)

    if group == Group.objects.get(name='Quality Assurance') and  goal.goal_status == verifygoal:
        form = QAChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
            form = QAChangeGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goal.goal_status = choice
                goal.save()
                return HttpResponseRedirect(reverse('home'))
        else:
            form = QAChangeGoalForm()
            return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'currentuser': current, 'group': group})

    # if group == Group.objects.get(name='Quality Assurance') and current != goal.user and goal.goal_status == verifygoal:
    #     form = QAChangeGoalForm()
    #     if request.method == 'GET':
    #             return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
    #     if request.method == 'POST':
    #             form = QAChangeGoalForm(request.POST)
    #             if form.is_valid():
    #                 selected_status = form.save(commit=False)
    #                 selected = form.cleaned_data['goal_status']
    #                 get_status = selected_status.status_name
    #                 choice = GoalStatus.objects.get(id=int(selected))
    #                 goal.goal_status = choice
    #                 goal.save()
    #                 return HttpResponseRedirect(reverse('home'))
    #     else:
    #             form = QAChangeGoalForm()
    #             return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'currentuser': current, 'group': group})
    else : 
        form = QAMoveForm()
        if request.method == 'GET':
                return render(request, 'remiljscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        if request.method == 'POST':
                form = QAMoveForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('home'))
        # return render(request, 'remiljscrumy/movegoal.html',{'form': form, 'goal': goal, 'currentuser': current, 'group': group})
        # notexist = 'You can only move goal from verify goals to done goals'
        # context = {'not_exist': notexist}
        # return render(request, 'remiljscrumy/exception.html', context)

# def move_goal(request, goal_id):
#     #response = ScrumyGoals.objects.get(goal_id=goal_id)
#     # try:
#     #goal = ScrumyGoals.objects.get(goal_id=goal_id)
#     # except ScrumyGoals.DoesNotExist:
#     #     raise Http404 ('A record with that goal id does not exist')
#     instance = get_object_or_404(ScrumyGoals,goal_id=goal_id)
#     form = MoveGoalForm(request.POST or None, instance=instance)
#     if form. is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         return redirect('home')
#     context={
#         'goal_id': instance.goal_id,
#         'user': instance.user,
#         'goal_status': instance.goal_status,
#         'form':form,
#         }
#     return render(request, 'remiljscrumy/exception.html', context)
            #move_goal = form.save(commit=False)
            # move_goal = 
            # form.save()
            # # goal_name = form.cleaned_data.get('goal_name')
            # # ScrumyGoals.objects.get(goal_name)
            # return redirect('home')
    # def form_valid(self, form):
    #          form.instance.goal_status = self.request.user
    #          return super(addgoalForm, self).form_valid(form)
    

    # }
    # return render(request, 'remiljscrumy/exception.html', context=gdict)
    #return HttpResponse(response)
    # return HttpResponse('%s is the response at the record of goal_id %s' % (response, goal_id))'''

from random import randint 
def add_goal(request):
    # existing_id = ScrumyGoals.objects.order_by('goal_id')
    # while True:
    #     goal_id = randint(1000, 10000)  #returns a random number between 1000 and 9999           
    #     if goal_id not in existing_id:        
    #         pr = ScrumyGoals.objects.create(goal_name='Keep Learning Django', goal_id=goal_id, created_by='Louis', moved_by="Louis", goal_status=GoalStatus.objects.get(pk=1), user=User.objects.get(pk=6))
    #         break
    #  form = CreateGoalForm
    # if request.method == 'POST':
    #     form = CreateGoalForm(request.POST)
    #     if form .is_valid():
    #         add_goals = form.save(commit=False)
    #         add_goals = form.save()
    #         #form.save()
    #         return redirect('home')
    # else:
    #     form = CreateGoalForm()
    return render(request, 'remiljscrumy/addgoal.html', {'form': form})

def home(request):
    '''# all=','.join([eachgoal.goal_name for eachgoal in ScrumyGoals.objects.all()])  
    # home = ScrumyGoals.objects.filter(goal_name='keep learning django')
    # return HttpResponse(all)
    #homedict = {'goal_name':ScrumyGoals.objects.get(pk=3).goal_name,'goal_id':ScrumyGoals.objects.get(pk=3).goal_id, 'user': ScrumyGoals.objects.get(pk=3).user,}
    user = User.objects.get(email="louisoma@linuxjobber.com")
    name = user.scrumygoal.all()
    homedict={'goal_name':ScrumyGoals.objects.get(pk=1).goal_name,'goal_id':ScrumyGoals.objects.get(pk=1).goal_id,'user':ScrumyGoals.objects.get(pk=1).user,
             'goal_name1':ScrumyGoals.objects.get(pk=2).goal_name,'goal_id1':ScrumyGoals.objects.get(pk=2).goal_id,'user':ScrumyGoals.objects.get(pk=2).user,
             'goal_name2':ScrumyGoals.objects.get(pk=3).goal_name,'goal_id2':ScrumyGoals.objects.get(pk=3).goal_id,'user2':ScrumyGoals.objects.get(pk=3).user}'''
   
    # form = CreateGoalForm
    # if request.method == 'POST':
    #     form = CreateGoalForm(request.POST)
    #     if form .is_valid():
    #         add_goal = form.save(commit=True)
    #         add_goal = form.save()
    # #         #form.save()
    #         return redirect('home')

    current = request.user #gets the logged in user
    week = GoalStatus.objects.get(pk=1) #gets status name weekly goal
    day = GoalStatus.objects.get(pk=2) #gets status name daily goal
    verify = GoalStatus.objects.get(pk=3)#gets status name verify goals
    done = GoalStatus.objects.get(pk=4)#gets status name done goals
    user = User.objects.all() #gets all users in the db
    weeklygoal = ScrumyGoals.objects.filter(goal_status=week) #get all goals stored as weeklygoal
    dailygoal = ScrumyGoals.objects.filter(goal_status=day) #get all goals stored as dailygoal
    verifygoal = ScrumyGoals.objects.filter(goal_status=verify) #get all goals stored as verifygoal
    donegoal = ScrumyGoals.objects.filter(goal_status=done) #get all goals stored as donegoal
    groups = current.groups.all()# gets the group(s) that the logged in user belongs to
    #cug= current.ScrumyGoals.all()#gets all the goals of the current user
    dev = Group.objects.get(name='Developer') #Gets group name Developer
    owner = Group.objects.get(name='Owner') #Gets group name Owner
    admin = Group.objects.get(name='Admin') #Gets group name Admin
    qa = Group.objects.get(name='Quality Assurance') #Gets group name Quality assurance
    form = CreateGoalForm()

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if current.is_authenticated:
        if dev in groups or qa in groups or owner in groups:
            # if request.method == 'GET':
            #     return render(request, 'remiljscrumy/home.html', context)
            form = CreateGoalForm()
            context = {'user': user, 'weeklygoal': weeklygoal, 'dailygoal': dailygoal, 'verifygoal': verifygoal,
                       'donegoal': donegoal, 'form': form, 'current': current, 'groups': groups,'dev': dev,'owner':owner,'admin':admin,'qa':qa}
        if request.method == 'POST':
            form = CreateGoalForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                status_name = GoalStatus(id=1)
                post.goal_status = status_name
                post.user = current
                post = form.save()
        elif admin in groups:
             context = {'user': user, 'weeklygoal': weeklygoal, 'dailygoal': dailygoal, 'verifygoal': verifygoal,
                       'donegoal': donegoal,'form':form,'current': current, 'groups': groups,'dev': dev,'owner':owner,'admin':admin,'qa':qa}
        return render(request, 'remiljscrumy/home.html', context)


def filtered_users():
    users = ScrumUserSerializer(ScrumUser.objects.all(), many=True).data

    for user in users:
        user['scrumygoals_set'] = [x for x in user['scrumygoals_set'] if x ['visible'] == True]

    return users



# class UserViewSet(viewsets.ModelViewSet):
#     '''
#     API endpoint that allows users to be viewed or edited
#     '''
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
#     # permission_classes = (IsAuthenticated,)

#     def create (self,request):
#         # for ScrumUser.objects.all() dfg

#         # current = ScrumUser.objects.all()
#         # blob = ScrumUser.objects.filter(user=current[1])

#         # content = {
#         #     'user': User(request.user),  # `django.contrib.auth.User` instance.
#         #     'auth': User(request.auth), 
#         #     'role': ScrumProjectRole.objects.get(user=user.scrumuser).role, # None
#         # }
#         # return Response(content)
#         # username = request.data['username']
#         # password = request.data['password']


#         # content = {'message': 'Hello, World!',
#         # }

#         # login_user = authenticate(request, username=username,password=password)
#         # if login_user is not None:
#         #     return JsonResponse(content)
#         # else:
#         #     return JsonResponse({'exit': 1, 'message': 'Error: Invalid Credentials'})


#         username = request.data['username']
#         password = request.data['password']
        
#         login_user = authenticate(request, username=username, password=password)
#         if login_user is not None:
#             return JsonResponse({'exit': 0, 'message': 'WELCOME!','role': login_user.groups.all()[0].name, 'data': filtered_users()})
#         else:
#             return JsonResponse({'exit': 1, 'message': 'Error: Invalid Credentials'})





   # class ExampleView(APIView):
   #  authentication_classes = (SessionAuthentication, BasicAuthentication)
   #  permission_classes = (IsAuthenticated,)

   #  def get(self, request, format=None):
   #      content = {
   #          'user': unicode(request.user),  # `django.contrib.auth.User` instance.
   #          'auth': unicode(request.auth),  # None
   #      }
   #      return Response(content)
    # @api_view(['GET', 'POST'])
    # def user_list(srequest):
    #     if request.method == 'GET':
    #         users = User.objects.all()
    #         serializer = UserSerializer(users, many=True)
    #         return Response(serializer.data)

    #     elif request.method == 'POST':
    #         serializer = UserSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all code snippets, or create a new snippet.
    """
    
    

    


# class GroupViewSet(viewsets.ModelViewSet):
#     '''
#     API endpoint that allows groups to be viewed or edited
#     '''
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer

    # def create(self,request):
    #     password = request.data['password']
    #     rtpassword = request.data['rtpassword']
    #     if password != rtpassword:
    #         return JsonResponse({'message': 'Password Do Not Match.'})
    #     user, created = User.objects.get_or_create(username=request.POST.get('username', None))
    #     if created:
    #         user.set_password(password)
    #         group = Group.objects.get(name=request.POST.get('usertype', None))
    #         group.user_set.add(user)
    #         user.save()
    #         scrum_user = ScrumUser(user=user, nickname=request.data['full_name'])
    #         scrum_user.save()
    #         return JsonResponse({'message': 'User Created Successfully.'})
    #     else:
    #         return JsonResponse({'message': 'Error:Username already Exists'})



    def create(self,request):
        password = request.data['password']
        rtpassword = request.data['pass_auth']
        if password != rtpassword:
            return JsonResponse({'message':'Error: Passwords Mismatch'})
        user, created = User.objects.get_or_create(username=request.data['username'], email=request.data['email'],)
        if created:
            user.set_password(password)
            group = Group.objects.get(name=request.data['usertype'])
            group.user_set.add(user)
            user.save()
            scrum_user = ScrumUser(user=user, nickname=request.data['full_name'])
            scrum_user.save()
            scrum_project_role = ScrumProjectRole(role=request.data['usertype'], user=scrum_user)
            scrum_project_role.save()
            return JsonResponse({'message': 'User Created Successfully.'})
        else:
            return JsonResponse({'message': 'Error: User with that e-mail already exists.'})

    '''
    API endpoint that allows groups to be viewed or edited
    '''
    
    # def create(self, request):
    #     password = request.data['password']
        
    #     user = User.objects.get_or_create(username=request.data['username'],email=request.data['email'],
    #         first_name=request.data['firstname'], last_name=request.data['lastname'])
    #     # group = Group.objects.get_or_create(name=request.data['usertype'])
           
    #     if user:
    #         user[0].set_password(password)
    #         group = Group.objects.get(name=request.data['usertype'])
    #         group.user_set.add(user[0])
    #         user[0].save()
    #         # group = user[0].groups(name=request.data['usertype'])
    #         # user[0].save()
            # # print(group)
    #         # group_user = Group(name=user[0].usertype)
    #         # group_user.save


    #         scrum_user = User(username=user[0].username,  email=user[0].email,
    #             first_name=user[0].firstname,last_name=user[0].lastname)
    #         scrum_user.save()
    #         # if request.data['usertype'] == 'Owner':
    #         #     scrum_role= Group(name="Owner")
    #         #     scrum_role.save()
    #         # user.set_password(request.data['password'])
    #         # user.save()

    #         return JsonResponse({'message': 'User created successfully'})
    #     else:
    #         return JsonResponse({'message': 'Error: Username already exist'})
    #     #  user, created = User.objects.get_or_create(username=request.data['email'], email=request.data['email'])
    #     # if created:
    #     #     scrum_user = ScrumUser(user=user, nickname=request.data['full_name'])
        #     scrum_user.save()
        #     if request.data['usertype'] == 'Owner':
        #         scrum_project = ScrumProject(name=request.data['projname'])
        #         scrum_project.save()
        #         scrum_project_role = ScrumProjectRole(role="Owner", user=scrum_user, project=scrum_project)
        #         scrum_project_role.save()

        #     user.set_password(request.data['password'])
        #     user.save()
        #     return JsonResponse({'message': 'User Created Successfully.'})
        # else:
        #     return JsonResponse({'message': 'Error: User with that e-mail already exists.'})



        
            
            # rtpassword = request.data['rtpassword']
        
            # rtpassword = False
        
        # if password != rtpassword:
        #     return JsonResponse({'message': 'Error: The Password Do Not Match'})
      
       



class ScrumGoalViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited
    '''
    queryset = ScrumyGoals.objects.all()
    serializer_class = ScrumGoalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self,request):
            name_goal = request.data['name']
            group_name = request.user.groups.all()[0].name
            goal_status_start = GoalStatus(id=1)
            if group_name == 'Admin':
                goal_status_start = GoalStatus(id=3)
            elif group_name == 'Quality Assurance':
               goal_status_start = GoalStatus(id=2)
            goal = ScrumyGoals(user=request.user.scrumuser, goal_name=name_goal,goal_status=goal_status_start)
            goal.save()
            return JsonResponse({'message':'Goal added', 'data': filtered_users()})
        
    def patch(self, request):
            goals_id = request.data['goal_id']
            to_id = request.data['to_id']
        
            if to_id == 5:
                if request.user.groups.all()[0].name == 'Developer':
                    if request.user != ScrumyGoals.objects.get(id = goals_id).user:
                        return JsonResponse({'message':'Permission Denied: Unauthorized Deletion of Goal', 'data':filtered_users()})          
                del_goal = ScrumyGoals.objects.get(id = goals_id)
                del_goal.visible = False
                print (goals_id)
                del_goal.save()
                return JsonResponse({'message':'Goal Removed Successfully', 'data':filtered_users()})
            else:
                goal_item = ScrumyGoals.objects.get(id = goals_id)

                group = request.user.groups.all()[0].name
                from_allowed = []
                to_allowed = []
                    
                if group == 'Developer':
                    if request.user != goal_item.user:
                        return JsonResponse({'message':'Permission Denied: Unauthorized Movement of Goal', 'data':filtered_users()})
                           
                if group == 'Owner':
                    from_allowed = [1, 2, 3, 4]
                    to_allowed = [1, 2, 3, 4]
                elif group == 'Admin':
                    from_allowed = [2, 3]
                    to_allowed = [1, 2]
                elif group == 'Developer':
                    from_allowed = [1, 2]
                    to_allowed = [1, 2]
                # elif group == 'Quality Analyst':
                #     from_allowed = [3, 4]
                #     to_allowed = [3, 4]
                        
                if (goal_item.goal_status_id in from_allowed) and (to_id in to_allowed):
                    # if to_id >= 0:
                        goal_item.goal_status_id = to_id 
                elif group == 'Quality Assurance' and goal_item.goal_status_id == 3 and to_id == 1:
                    goal_item.goal_status_id = to_id 
                else:
                    return JsonResponse({'message':'Permission Denied: Unauthorized Movement of Goal', 'data':filtered_users()})
                    
                goal_item.save()
                return JsonResponse({'message':'Goal Moved Successfully', 'data':filtered_users()})
        

    def put(self, request):
        if request.data['mode'] == 0:
            from_id = request.data['from_id']
            to_id = request.data['to_id']

            if request.user.groups.all()[0].name == 'Developer':
                return JsonResponse({'exit':0, 'message':'Permission Denied: Reassignment of Goal', 'data':filtered_users()})

            goal = ScrumyGoals.objects.get(id=from_id)

            author = None
            if to_id [0] == 'u':
                author = ScrumUser.objects.get(id=to_id[1:])
            else:
                author = ScrumyGoals.objects.get(id=to_id).user
            goal.user = author
            goal.save()
            return JsonResponse({'message':'Goal Reassigned Successfully', 'data':filtered_users()})
        else:
            goal = ScrumyGoals.objects.get(id = request.data['goal_id'])
            if request.user.groups.all()[0].name != 'Owner' and request.user != goal.scrumuser.user:
                return JsonResponse({'exit':0, 'message':'Permission Denied: Unauthorized Name Change of Goal', 'data':filtered_users()})
            goal.goal_name = request.data['new_name']
            goal.save()
            return JsonResponse({'message':'Goal Name Changed', 'data':filtered_users()})
        


                    

    # def list(self, request):
    #     queryset = ScrumyGoals.objects.all()
    #     serializer = ScrumGoalSerializer(queryset, many=True)
    #     return Response(serializer.data)




def jwt_response_payload_handler(token, user=None, request=None):
        
    return {
        'token': token,
        'message': 'WELCOME!.',
        'role': user.groups.all()[0].name,
        'data': filtered_users()
        }
    

# class ScrumProjectRoleViewSet(viewsets.ModelViewSet):
#     queryset = ScrumProjectRole.objects.all()
#     serializer_class = ScrumProjectRoleSerializer