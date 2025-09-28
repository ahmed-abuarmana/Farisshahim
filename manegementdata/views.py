from django.shortcuts import render, get_object_or_404, redirect
from .models import Makhbaz, Takiya, Taslima
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # يرجع للصفحة الرئيسية بعد الدخول
        else:
            return render(request, 'login.html', {'error': '❌ اسم المستخدم أو كلمة المرور غير صحيحة'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # يرجع لصفحة تسجيل الدخول



@login_required(login_url='login')
def index(request):
    makhabiz = Makhbaz.objects.all()
    takiyat = Takiya.objects.all()
    context = {
        "makhabiz": makhabiz,
        "takiyat": takiyat,
    }
    return render(request, "index.html", context)



@login_required(login_url='login')
# عرض كل المخابز
def makhabez_list(request):
    makhabiz = Makhbaz.objects.all()
    return render(request, "makhabez_list.html", {"makhabiz": makhabiz})



@login_required(login_url='login')
# عرض تفاصيل مخبز محدد مع جميع التسليمات
def makhabez_detail(request, pk):
    makhbaz = get_object_or_404(Makhbaz, pk=pk)

    # جلب التسليمات المرتبطة بهذا المخبز
    all_tasleemat = makhbaz.taslimat.all().order_by('-taslima_date')

    latest_taslim = all_tasleemat.first() if all_tasleemat.exists() else None

    # حساب الإجماليات
    total_flour = sum(t.flour or 0 for t in all_tasleemat)
    total_salt = sum(t.salt or 0 for t in all_tasleemat)
    total_yeast = sum(t.yeast or 0 for t in all_tasleemat)
    total_oil = sum(t.oil or 0 for t in all_tasleemat)
    total_wood = sum(t.wood or 0 for t in all_tasleemat)
    total_rice = sum(t.rice or 0 for t in all_tasleemat)
    total_beans = sum(t.beans or 0 for t in all_tasleemat)
    total_lentils_red = sum(t.lentils_red or 0 for t in all_tasleemat)
    total_lentils_black = sum(t.lentils_black or 0 for t in all_tasleemat)
    total_pasta = sum(t.pasta or 0 for t in all_tasleemat)

    context = {
        "makhbaz": makhbaz,
        "all_tasleemat": all_tasleemat,
        "latest_taslim": latest_taslim,
        "total_deliveries": all_tasleemat.count(),
        "total_flour": total_flour,
        "total_salt": total_salt,
        "total_yeast": total_yeast,
        "total_oil": total_oil,
        "total_wood": total_wood,
        "total_rice": total_rice,
        "total_beans": total_beans,
        "total_lentils_red": total_lentils_red,
        "total_lentils_black": total_lentils_black,
        "total_pasta": total_pasta,
    }

    return render(request, "makhabez_detail.html", context)



@login_required(login_url='login')
# عرض كل التكيات
def takiyat_list(request):
    takiyat = Takiya.objects.all()
    return render(request, "takiyat_list.html", {"takiyat": takiyat})



@login_required(login_url='login')
# عرض تفاصيل تكية محددة مع جميع التسليمات
def takiya_detail(request, pk):
    takiya = get_object_or_404(Takiya, pk=pk)

    # جلب التسليمات المرتبطة بهذه التكية
    all_tasleemat = takiya.taslimat.all().order_by('-taslima_date')

    latest_taslim = all_tasleemat.first() if all_tasleemat.exists() else None

    # حساب الإجماليات
    total_flour = sum(t.flour or 0 for t in all_tasleemat)
    total_salt = sum(t.salt or 0 for t in all_tasleemat)
    total_yeast = sum(t.yeast or 0 for t in all_tasleemat)
    total_oil = sum(t.oil or 0 for t in all_tasleemat)
    total_wood = sum(t.wood or 0 for t in all_tasleemat)
    total_rice = sum(t.rice or 0 for t in all_tasleemat)
    total_beans = sum(t.beans or 0 for t in all_tasleemat)
    total_lentils_red = sum(t.lentils_red or 0 for t in all_tasleemat)
    total_lentils_black = sum(t.lentils_black or 0 for t in all_tasleemat)
    total_pasta = sum(t.pasta or 0 for t in all_tasleemat)

    context = {
        "takiya": takiya,
        "all_tasleemat": all_tasleemat,
        "latest_taslim": latest_taslim,
        "total_deliveries": all_tasleemat.count(),
        "total_flour": total_flour,
        "total_salt": total_salt,
        "total_yeast": total_yeast,
        "total_oil": total_oil,
        "total_wood": total_wood,
        "total_rice": total_rice,
        "total_beans": total_beans,
        "total_lentils_red": total_lentils_red,
        "total_lentils_black": total_lentils_black,
        "total_pasta": total_pasta,
    }

    return render(request, "takiya_detail.html", context)



@login_required(login_url='login')
def add_taslima(request):
    if request.method == 'POST':
        taslima_date = request.POST.get('taslima_date')
        flour = request.POST.get('flour') or None
        salt = request.POST.get('salt') or None
        yeast = request.POST.get('yeast') or None
        oil = request.POST.get('oil') or None
        wood = request.POST.get('wood') or None
        rice = request.POST.get('rice') or None
        beans = request.POST.get('beans') or None
        lentils_red = request.POST.get('lentils_red') or None
        lentils_black = request.POST.get('lentils_black') or None
        pasta = request.POST.get('pasta') or None

        makhbaz_id = request.POST.get('makhbaz')
        takiya_id = request.POST.get('takiya')

        # تأكد أنه تم اختيار إما مخبز أو تكية فقط
        if makhbaz_id and takiya_id:
            return render(request, 'add_taslima.html', {
                'makhabiz': Makhbaz.objects.all(),
                'takiyat': Takiya.objects.all(),
                'error': 'لا يمكن اختيار مخبز وتكية في نفس الوقت!'
            })

        taslima = Taslima.objects.create(
            taslima_date=taslima_date,
            flour=flour,
            salt=salt,
            yeast=yeast,
            oil=oil,
            wood=wood,
            rice=rice,
            beans=beans,
            lentils_red=lentils_red,
            lentils_black=lentils_black,
            pasta=pasta,
            makhbaz_id=makhbaz_id if makhbaz_id else None,
            takiya_id=takiya_id if takiya_id else None
        )

        return redirect('index')

    makhabiz = Makhbaz.objects.all()
    takiyat = Takiya.objects.all()
    return render(request, 'add_taslima.html', {
        'makhabiz': makhabiz,
        'takiyat': takiyat
    })



@login_required(login_url='login')
def add_tasleema_for_makhbaz(request, makhbaz_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            makhbaz = Makhbaz.objects.get(id=makhbaz_id)
            taslima = Taslima.objects.create(
                taslima_date = data.get('taslima_date'),
                flour = data.get('flour') or None,
                salt = data.get('salt') or None,
                yeast = data.get('yeast') or None,
                oil = data.get('oil') or None,
                wood = data.get('wood') or None,
                rice = data.get('rice') or None,
                beans = data.get('beans') or None,
                lentils_red = data.get('lentils_red') or None,
                lentils_black = data.get('lentils_black') or None,
                pasta = data.get('pasta') or None,
            )
            makhbaz.taslimat.add(taslima)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})



@login_required(login_url='login')
def add_tasleema_for_takiya(request, takiya_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            takiya = Takiya.objects.get(id=takiya_id)
            taslima = Taslima.objects.create(
                taslima_date = data.get('taslima_date'),
                flour = data.get('flour') or None,
                salt = data.get('salt') or None,
                yeast = data.get('yeast') or None,
                oil = data.get('oil') or None,
                wood = data.get('wood') or None,
                rice = data.get('rice') or None,
                beans = data.get('beans') or None,
                lentils_red = data.get('lentils_red') or None,
                lentils_black = data.get('lentils_black') or None,
                pasta = data.get('pasta') or None,
            )
            takiya.taslimat.add(taslima)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})



@login_required(login_url='login')
def add_new_makhbaz(request):
    if request.method == "POST":
        name = request.POST.get("name")
        owner_name = request.POST.get("owner_name")
        address = request.POST.get("address")
        mobile_number = request.POST.get("mobile_number")

        if name and owner_name and address and mobile_number:
            Makhbaz.objects.create(
                name=name,
                owner_name=owner_name,
                address=address,
                mobile_number=mobile_number
            )
            messages.success(request, "✅ تم إضافة المخبز بنجاح")
            return redirect("makhabez_list")  # بعد الحفظ يرجع لقائمة المخابز
        else:
            messages.error(request, "⚠️ الرجاء تعبئة جميع الحقول المطلوبة")

    return render(request, "add_new_makhbaz.html")



@login_required(login_url='login')
def add_new_takiya(request):
    if request.method == "POST":
        name = request.POST.get("name")
        owner_name = request.POST.get("owner_name")
        address = request.POST.get("address")
        mobile_number = request.POST.get("mobile_number")

        # 📝 إنشاء تكية جديدة
        Takiya.objects.create(
            name=name,
            owner_name=owner_name,
            address=address,
            mobile_number=mobile_number
        )

        # ✅ رسالة نجاح
        messages.success(request, "✅ تم إضافة التكية بنجاح.")
        return redirect("takiyat_list")  # اسم صفحة عرض التكيات

    return render(request, "add_new_takiya.html")



@login_required(login_url='login')
def delete_makhbaz(request, makhbaz_id):
    makhbaz = get_object_or_404(Makhbaz, id=makhbaz_id)

    # ⚠️ حذف المخبز
    makhbaz.delete()
    messages.success(request, "🗑️ تم حذف المخبز بنجاح.")
    return redirect("makhabez_list")



@login_required(login_url='login')
def delete_takiya(request, takiya_id):
    takiya = get_object_or_404(Takiya, id=takiya_id)

    # ⚠️ حذف التكية
    takiya.delete()
    messages.success(request, "🗑️ تم حذف التكية بنجاح.")
    return redirect("takiyat_list")  # اسم صفحة قائمة التكيات
