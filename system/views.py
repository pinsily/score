import json

from django.contrib import auth
from django.http import JsonResponse, HttpResponse

# Create your views here.
from system.models import Profile, Module, Professor, Score
from system.userforms import LoginForm, RegistrationForm

score_str = {
    1: "*",
    2: "**",
    3: "***",
    4: "****",
    5: "*****",
}


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                rep = build_response('login successfully, have fun!', 200)
                rep.set_cookie('login', True)
                rep.set_cookie('uname', username)
                return rep
            else:
                # login fail
                print("login fail")
                return build_response('UserName or Password not Right!', 405)
        else:
            return build_response('UserName or Password not Right!', 405)

    return build_response('not post method!', 401)


def user_register(request):
    """
    user_register
    """
    print(request.POST)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = Profile.objects.create_user(username=username, password=password, email=email)
            print(f"create user: {user}")
            return build_response('register successfully, go to login!', 200)

        else:
            # errors
            return build_response(form.errors.as_text(), 403)

    return build_response('register fail, try again!', 200)


def user_logout(request):
    """
    logout logic
    """
    check_login(request)

    rep = build_response("--- Successfully logged off", 200)
    rep.delete_cookie('login')
    rep.delete_cookie('uname')
    return rep


def module_list(request):
    check_res = check_login(request)
    if check_res is not None:
        return check_res

    # get module list
    modules = Module.objects.all()
    if len(modules) < 1:
        return build_response("--- no modules!", 404)

    module_data = []
    for module in modules:
        module_data.append({
            "index": module.index,
            "code": module.code,
            "name": module.name,
            "year": module.year,
            "semester": module.semester,
            "professor": " ; ".join(
                [f"{professor.code}, Professor {professor.name}" for professor in module.professor.all()]),
        })

    rep = json.dumps({'modules': module_data})
    return HttpResponse(content=rep, content_type="application/json", status=200)


def professor_list(request):
    check_res = check_login(request)
    if check_res is not None:
        return check_res

    # professor
    professors = Professor.objects.all()
    if len(professors) < 1:
        return build_response("--- no modules!", 404)

    professor_data = []
    for professor in professors:
        professor_data.append({
            "index": professor.index,
            "code": professor.code,
            "name": professor.name,
        })
    rep = json.dumps({'professors': professor_data})
    return HttpResponse(content=rep, content_type="application/json", status=200)


def rating_view(request):
    check_res = check_login(request)
    if check_res is not None:
        return check_res

    scores = Score.objects.all()
    if len(scores) < 1:
        return build_response("--- It hasn't been rating yet!", 404)

    # {“module”: [score]}
    data = {}
    for score in scores:
        if not data.get(score.professor.index, None):
            data[score.professor.index] = []
        data[score.professor.index].append(score.score)

    res_list = []
    for key, value in data.items():
        professor = Professor.objects.get(pk=key)
        res = {
            "professor_name": professor.name,
            "professor_code": professor.code,
            "score": score_str.get(round(sum(value)/len(value)), "")
        }

        res_list.append(res)

    rep = json.dumps({'views': res_list})
    return HttpResponse(content=rep, content_type="application/json", status=200)


def average(request):
    """
    average [professor_code] [module_code]
    """
    check_res = check_login(request)
    if check_res is not None:
        return check_res

    data = json.loads(request.body)
    print(data)
    # professor
    try:
        professor = Professor.objects.get(code=data['professor_code'])
    except Professor.DoesNotExist:
        return build_response(f"--- Professor info Not Exist, code={data['professor_code']}", 404)

    # module
    module_list = Module.objects.filter(code=data['module_code'])
    if len(module_list) < 1:
        return build_response(f"--- Module info Not Exist, code={data['module_code']}", 400)

    module = module_list[0]

    scores = Score.objects.filter(module__in=module_list, professor=professor)
    print(scores)
    if len(scores) < 1:
        return build_response(f"--- The professor has not rating in this module yet", 404)

    total_score = sum([score.score for score in scores])
    print(total_score)
    res = {
        "professor_name": professor.name,
        "professor_code": professor.code,
        "module_name": module.name,
        "module_code": module.code,
        "average": score_str.get(round(total_score / len(scores)), "")
    }

    return HttpResponse(content=json.dumps(res), content_type="application/json", status=200)


def rating(request):
    check_res = check_login(request)
    if check_res is not None:
        return check_res

    try:
        user = Profile.objects.get(username=request.COOKIES.get('uname'))
    except Profile.DoesNotExist:
        return build_response("--- You haven't logged in yet", 400)

    data = json.loads(request.body)
    print(data)
    # professor
    try:
        professor = Professor.objects.get(code=data['professor_code'])
    except Professor.DoesNotExist:
        return build_response(f"--- Professor info Not Exist, code={data['professor_code']}", 404)

    # module
    try:
        module = Module.objects.get(code=data['module_code'], year=data['year'], semester=int(data['semester']))
    except Module.DoesNotExist:
        return build_response(f"--- Module info Not Exist, code={data['module_code']}, year={data['year']}"
                              f", semester={data['semester']}", 400)

    if professor not in module.professor.all():
        return build_response(f"--- The professor didn't teach this module", 400)

    if len(Score.objects.filter(student=user, professor=professor, module=module)) > 0:
        return build_response(f"--- You have been rating repeatedly", 400)

    record = Score(student=user, professor=professor, module=module, score=int(data["rating"]))
    record.save()

    return build_response(f"--- rating successfully! Thank for your rating!", 200)


def build_response(msg: str, status: int):
    """
    build common response
    """
    data = {
        "msg": msg
    }
    return JsonResponse(data, status=status)


def check_login(request):
    """
    login status check
    """
    if not request.COOKIES.get('login'):
        print("not login!")
        return build_response("--- You haven't logged in yet", 400)
