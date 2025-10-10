from django.shortcuts import render, get_object_or_404, redirect
from .models import Makhbaz, Takiya, Taslima_makhbaz, Taslima_takiya
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import logging
import urllib.parse



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
    total_sugar = sum(t.sugar or 0 for t in all_tasleemat)
    total_cooking_oil = sum(t.cooking_oil or 0 for t in all_tasleemat)
    total_wood = sum(t.wood or 0 for t in all_tasleemat)
    total_gas = sum(t.gas or 0 for t in all_tasleemat)

    context = {
        "makhbaz": makhbaz,
        "all_tasleemat": all_tasleemat,
        "latest_taslim": latest_taslim,
        "total_deliveries": all_tasleemat.count(),
        "total_flour": total_flour,
        "total_salt": total_salt,
        "total_yeast": total_yeast,
        "total_sugar": total_sugar,
        "total_cooking_oil": total_cooking_oil,
        "total_wood": total_wood,
        "total_gas": total_gas,
    }

    return render(request, "makhabez_detail.html", context)



@login_required(login_url='login')
# @require_http_methods(["POST"])
def update_makhbaz(request, pk):
    if request.method == "POST":
        try:
            makhbaz = get_object_or_404(Makhbaz, pk=pk)
            data = json.loads(request.body)
            
            # تحديث الحقول
            fields = [
                'name', 'owner_name', 'owner_id', 'mobile_number', 
                'address', 'governorate', 'coordinates', 'oven_type',
                'production_capacity', 'contract_type', 'status'
            ]
            
            for field in fields:
                if field in data:
                    setattr(makhbaz, field, data[field])
            
            makhbaz.save()
            
            return JsonResponse({"success": True})
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})



@login_required(login_url='login')
@require_http_methods(["POST"])
def update_takiya(request, pk):
    """
    تحديث بيانات التكية المحددة بواسطة مفتاحها الأساسي (pk).
    تستقبل البيانات المعدلة كـ JSON في جسم الطلب.
    """
    try:
        takiya = get_object_or_404(Takiya, pk=pk)
        data = json.loads(request.body)
        
        # قائمة بالحقول القابلة للتعديل
        fields = [
            'name', 'owner_name', 'owner_id', 'mobile_number', 
            'address', 'governorate', 'coordinates', 'status',
            'total_pots', 'pots_80', 'pots_100', 'pots_120', 
            'pots_150', 'pots_200', 'daily_capacity'
        ]
        
        for field in fields:
            # التحقق مما إذا كان الحقل موجودًا في بيانات JSON
            # واستخدام قيمة None إذا كان الحقل فارغًا أو غير موجود لتجنب أخطاء التحويل
            if field in data:
                value = data[field] if data[field] != "" else None
                setattr(takiya, field, value)
        
        # ملاحظة: حقول الاختيار (choices) مثل 'governorate' و 'status' يجب أن تكون 
        # قيمتها في JSON هي القيمة المخزنة (مثل "رفح" أو "فعال").

        takiya.save()
        
        return JsonResponse({"success": True})
            
    except Takiya.DoesNotExist:
        return JsonResponse({"success": False, "error": "التكية غير موجودة"}, status=404)
    except Exception as e:
        # يمكن تسجيل الخطأ التفصيلي في السجل (logging)
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required(login_url='login')
# عرض كل التكيات
def takiyat_list(request):
    takiyat = Takiya.objects.all()
    return render(request, "takiyat_list.html", {"takiyat": takiyat})



@login_required(login_url='login')
# عرض تفاصيل تكية محددة مع جميع التسليمات
def takiya_detail(request, pk):
    takiya = get_object_or_404(Takiya, pk=pk)

    # جلب التسليمات المرتبطة بهذه التكية (من Taslima_takiya)
    all_tasleemat = takiya.taslimat.all().order_by('-taslima_date')

    latest_taslim = all_tasleemat.first() if all_tasleemat.exists() else None

    # حساب الإجماليات لجميع الحقول
    total_salt = sum(t.salt or 0 for t in all_tasleemat)
    total_macaroni = sum(t.macaroni or 0 for t in all_tasleemat)
    total_rice = sum(t.rice or 0 for t in all_tasleemat)
    total_oil = sum(t.oil or 0 for t in all_tasleemat)
    total_peas = sum(t.peas or 0 for t in all_tasleemat)
    total_lentils = sum(t.lentils or 0 for t in all_tasleemat)
    total_beans = sum(t.beans or 0 for t in all_tasleemat)
    total_sauce = sum(t.sauce or 0 for t in all_tasleemat)
    total_luncheon = sum(t.luncheon or 0 for t in all_tasleemat)
    total_maggi_spice = sum(t.maggi_spice or 0 for t in all_tasleemat)
    total_vegetable_soup = sum(t.vegetable_soup or 0 for t in all_tasleemat)
    total_seven_spices = sum(t.seven_spices or 0 for t in all_tasleemat)
    total_ghee = sum(t.ghee or 0 for t in all_tasleemat)
    total_bulgur = sum(t.bulgur or 0 for t in all_tasleemat)

    context = {
        "takiya": takiya,
        "all_tasleemat": all_tasleemat,
        "latest_taslim": latest_taslim,
        "total_deliveries": all_tasleemat.count(),
        
        # إجماليات التسليمات
        "total_salt": total_salt,
        "total_macaroni": total_macaroni,
        "total_rice": total_rice,
        "total_oil": total_oil,
        "total_peas": total_peas,
        "total_lentils": total_lentils,
        "total_beans": total_beans,
        "total_sauce": total_sauce,
        "total_luncheon": total_luncheon,
        "total_maggi_spice": total_maggi_spice,
        "total_vegetable_soup": total_vegetable_soup,
        "total_seven_spices": total_seven_spices,
        "total_ghee": total_ghee,
        "total_bulgur": total_bulgur,
        
        # بيانات التكية الأساسية
        "governorate_choices": Takiya.GOVERNORATE_CHOICES,
        "status_choices": Takiya.STATUS_CHOICES,
        
        # إجماليات القدور
        "total_pots_all": (takiya.pots_80 or 0) + (takiya.pots_100 or 0) + 
                         (takiya.pots_120 or 0) + (takiya.pots_150 or 0) + 
                         (takiya.pots_200 or 0),
    }

    return render(request, "takiya_detail.html", context)


@login_required(login_url='login')
def add_tasleema_for_makhbaz(request, makhbaz_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            makhbaz = Makhbaz.objects.get(id=makhbaz_id)
            
            # إنشاء التسليمة
            taslima = Taslima_makhbaz.objects.create(
                taslima_date = data.get('taslima_date'),
                flour = data.get('flour') or None,
                yeast = data.get('yeast') or None,
                salt = data.get('salt') or None,
                sugar = data.get('sugar') or None,
                cooking_oil = data.get('cooking_oil') or None,
                wood = data.get('wood') or None,
                gas = data.get('gas') or None,
                additions = data.get('additions') or None,
                makhbaz = makhbaz
            )
            
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
            
            taslima = Taslima_takiya.objects.create(
                taslima_date=data.get('taslima_date'),
                salt=data.get('salt') or None,
                macaroni=data.get('macaroni') or None,
                rice=data.get('rice') or None,
                oil=data.get('oil') or None,
                peas=data.get('peas') or None,
                lentils=data.get('lentils') or None,
                beans=data.get('beans') or None,
                sauce=data.get('sauce') or None,
                luncheon=data.get('luncheon') or None,
                maggi_spice=data.get('maggi_spice') or None,
                vegetable_soup=data.get('vegetable_soup') or None,
                seven_spices=data.get('seven_spices') or None,
                ghee=data.get('ghee') or None,
                bulgur=data.get('bulgur') or None,
                additions=data.get('additions') or None,  # إضافة حقل الإضافات
                takiya=takiya
            )
            return JsonResponse({"success": True, "taslima_id": taslima.id})
        except Takiya.DoesNotExist:
            return JsonResponse({"success": False, "error": "التكية غير موجودة"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "طريقة الطلب غير صالحة"})


@login_required(login_url='login')
def add_new_makhbaz(request):
    if request.method == "POST":
        data = {
            'name': request.POST.get("name") or None,
            'governorate': request.POST.get("governorate") or None,
            'address': request.POST.get("address") or None,
            'owner_name': request.POST.get("owner_name") or None,
            'owner_id': request.POST.get("owner_id") or None,
            'mobile_number': request.POST.get("mobile_number") or None,
            'coordinates': request.POST.get("coordinates") or None,
            'oven_type': request.POST.get("oven_type") or None,
            'production_capacity': request.POST.get("production_capacity") or None,
            'contract_type': request.POST.get("contract_type") or None,
            'status': request.POST.get("status") or None,
        }

        # تحويل الإنتاجية اليومية من نص لرقم لو موجود
        if data['production_capacity']:
            try:
                data['production_capacity'] = int(data['production_capacity'])
            except ValueError:
                data['production_capacity'] = None

        Makhbaz.objects.create(**data)
        messages.success(request, "✅ تم إضافة المخبز بنجاح")
        return redirect("makhabez_list")

    return render(request, "add_new_makhbaz.html")


@login_required(login_url='login')
def add_new_takiya(request):
    if request.method == "POST":
        name = request.POST.get("name")
        governorate = request.POST.get("governorate")
        address = request.POST.get("address")
        owner_name = request.POST.get("owner_name")
        owner_id = request.POST.get("owner_id")
        mobile_number = request.POST.get("mobile_number")
        coordinates = request.POST.get("coordinates")

        # تحويل القيم الرقمية إلى Integers مع معالجة الحقول الفارغة
        total_pots = int(request.POST.get("total_pots") or 0)
        pots_80 = int(request.POST.get("pots_80") or 0)
        pots_100 = int(request.POST.get("pots_100") or 0)
        pots_120 = int(request.POST.get("pots_120") or 0)
        pots_150 = int(request.POST.get("pots_150") or 0)
        pots_200 = int(request.POST.get("pots_200") or 0)
        daily_capacity = int(request.POST.get("daily_capacity") or 0)

        status = request.POST.get("status")

        # إنشاء التكية الجديدة
        Takiya.objects.create(
            name=name,
            governorate=governorate,
            address=address,
            owner_name=owner_name,
            owner_id=owner_id,
            mobile_number=mobile_number,
            coordinates=coordinates,
            total_pots=total_pots,
            pots_80=pots_80,
            pots_100=pots_100,
            pots_120=pots_120,
            pots_150=pots_150,
            pots_200=pots_200,
            daily_capacity=daily_capacity,
            status=status,
        )

        messages.success(request, "✅ تم إضافة التكية بنجاح.")
        return redirect("takiyat_list")

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



logger = logging.getLogger(__name__)
@login_required(login_url='login')
def export_makhbaz_excel(request, makhbaz_id):
    try:
        makhbaz = get_object_or_404(Makhbaz, id=makhbaz_id)
        tasleemat = Taslima_makhbaz.objects.filter(makhbaz=makhbaz)

        wb = Workbook()
        ws = wb.active
        ws.title = "تقرير المخبز"
        
        # تفعيل الاتجاه من اليمين لليسار (RTL)
        ws.rightToLeft = True
        ws.sheet_view.rightToLeft = True

        # تنسيقات الألوان
        HEADER_FILL = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid') 
        SECTION_FILL = PatternFill(start_color='C6D9F1', end_color='C6D9F1', fill_type='solid') 
        DATA_FILL = PatternFill(start_color='DCE6F1', end_color='DCE6F1', fill_type='solid') 
        PLAIN_DATA_FILL = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')

        BORDER = Border(
            left=Side(style='thin', color='000000'), 
            right=Side(style='thin', color='000000'), 
            top=Side(style='thin', color='000000'), 
            bottom=Side(style='thin', color='000000')
        )
        
        # خط عربي
        title_font = Font(name='Arial', size=16, bold=True, color='FFFFFF')
        header_font = Font(name='Arial', size=12, bold=True, color='FFFFFF')
        section_font = Font(name='Arial', size=12, bold=True, color='1F4E78')
        normal_font = Font(name='Arial', size=11, bold=False, color='000000')
        bold_font = Font(name='Arial', size=11, bold=True, color='000000')
        
        # عنوان التقرير
        ws.merge_cells('A1:J1')
        title_cell = ws['A1']
        title_cell.value = f"📊 تقرير مفصل - مخبز {makhbaz.name or 'غير محدد'} 🥖"
        title_cell.fill = HEADER_FILL
        title_cell.font = title_font
        title_cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[1].height = 25

        # ----------------------------------------------------
        ## بيانات المخبز الأساسية
        # ----------------------------------------------------
        
        start_row_info = 3
        ws.merge_cells(f'A{start_row_info}:J{start_row_info}')
        section_title1 = ws[f'A{start_row_info}']
        section_title1.value = "البيانات الأساسية للمخبز"
        section_title1.fill = SECTION_FILL
        section_title1.font = section_font
        section_title1.alignment = Alignment(horizontal='center', vertical='center')
        
        headers_info = [
            'اسم المخبز', 'اسم صاحب المخبز', 'رقم الهوية', 'رقم الجوال', 
            'العنوان', 'المحافظة', 'الإحداثيات', 'نوع الفرن', 
            'القدرة الإنتاجية', 'نوع التعاقد', 'حالة المخبز', 'تاريخ الإضافة'
        ]
        
        values_info = [
            makhbaz.name or "غير محدد",
            makhbaz.owner_name or "غير محدد", 
            makhbaz.owner_id or "غير محدد",
            makhbaz.mobile_number or "غير محدد",
            makhbaz.address or "غير محدد",
            makhbaz.governorate or "غير محدد",
            makhbaz.coordinates or "غير محدد",
            makhbaz.oven_type or "غير محدد",
            makhbaz.production_capacity or "غير محدد",
            makhbaz.contract_type or "غير محدد",
            makhbaz.status or "غير محدد",
            makhbaz.created_at.strftime("%Y-%m-%d") if makhbaz.created_at else "غير محدد"
        ]
        
        current_row = start_row_info + 1
        for i, (header, value) in enumerate(zip(headers_info, values_info)):
            if i % 2 == 0:
                # الحقل الأول في الصف
                cell_key = ws.cell(row=current_row, column=1)
                cell_key.value = header
                cell_key.fill = DATA_FILL
                cell_key.font = bold_font
                cell_key.border = BORDER
                cell_key.alignment = Alignment(horizontal='right', vertical='center', wrap_text=True)

                # دمج الخلايا للقيمة (B إلى D)
                ws.merge_cells(f'B{current_row}:D{current_row}')
                cell_value = ws.cell(row=current_row, column=2)
                cell_value.value = value
                cell_value.fill = PLAIN_DATA_FILL
                cell_value.font = normal_font
                cell_value.border = BORDER
                cell_value.alignment = Alignment(horizontal='right', vertical='center', wrap_text=True)

                # تطبيق التنسيق على الخلايا المدمجة
                for col in [3, 4]:  # الأعمدة C و D
                    cell = ws.cell(row=current_row, column=col)
                    cell.border = BORDER
                    cell.fill = PLAIN_DATA_FILL
            
            else:
                # الحقل الثاني في نفس الصف
                cell_key = ws.cell(row=current_row, column=6)  # العمود F
                cell_key.value = header
                cell_key.fill = DATA_FILL
                cell_key.font = bold_font
                cell_key.border = BORDER
                cell_key.alignment = Alignment(horizontal='right', vertical='center', wrap_text=True)

                # دمج الخلايا للقيمة (G إلى J)
                ws.merge_cells(f'G{current_row}:J{current_row}')
                cell_value = ws.cell(row=current_row, column=7)  # العمود G
                cell_value.value = value
                cell_value.fill = PLAIN_DATA_FILL
                cell_value.font = normal_font
                cell_value.border = BORDER
                cell_value.alignment = Alignment(horizontal='right', vertical='center', wrap_text=True)

                # تطبيق التنسيق على الخلايا المدمجة
                for col in [8, 9, 10]:  # الأعمدة H, I, J
                    cell = ws.cell(row=current_row, column=col)
                    cell.border = BORDER
                    cell.fill = PLAIN_DATA_FILL
                
                current_row += 1

        # إذا كان عدد الحقول فردياً، ننهي الصف الأخير
        if len(headers_info) % 2 != 0:
            # نملأ الخلايا الفارغة في النصف الثاني من الصف
            for col in [6, 7, 8, 9, 10]:  # الأعمدة F إلى J
                cell = ws.cell(row=current_row, column=col)
                cell.border = BORDER
                cell.fill = DATA_FILL
            current_row += 1

        # ----------------------------------------------------
        ## قسم التسليمات
        # ----------------------------------------------------
        empty_row = current_row + 1
        
        ws.merge_cells(f'A{empty_row}:J{empty_row}')
        section_title2 = ws.cell(row=empty_row, column=1)
        section_title2.value = "سجل التسليمات والمواد المستلمة"
        section_title2.fill = SECTION_FILL
        section_title2.font = section_font
        section_title2.alignment = Alignment(horizontal='center', vertical='center')
        
        tasleem_headers = ["تاريخ التسليم", "طحين (كغ)", "خميرة (كغ)", "ملح (كغ)", 
                          "سكر (كغ)", "زيت (لتر)", "حطب (كغ)", "غاز (كغ)", "إضافات"]
        
        header_row = empty_row + 1
        for col_index, header in enumerate(tasleem_headers, start=1):
            cell = ws.cell(row=header_row, column=col_index)
            cell.value = header
            cell.fill = HEADER_FILL
            cell.font = header_font
            cell.border = BORDER
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        
        data_row = header_row + 1
        total_flour = total_yeast = total_salt = total_sugar = 0
        total_oil = total_wood = total_gas = 0
        
        for t in tasleemat:
            flour = t.flour or 0
            yeast = t.yeast or 0
            salt = t.salt or 0
            sugar = t.sugar or 0
            oil = t.cooking_oil or 0
            wood = t.wood or 0
            gas = t.gas or 0
            
            row_data = [
                t.taslima_date.strftime("%Y-%m-%d") if t.taslima_date else "غير محدد",
                flour,
                yeast, 
                salt,
                sugar,
                oil,
                wood,
                gas,
                t.additions or ""
            ]
            
            for col_index, value in enumerate(row_data, start=1):
                cell = ws.cell(row=data_row, column=col_index)
                cell.value = value
                cell.border = BORDER
                cell.font = normal_font
                cell.fill = PLAIN_DATA_FILL if data_row % 2 != 0 else DATA_FILL
                
                if col_index in [2, 3, 4, 5, 6, 7, 8]:  # الأعمدة الرقمية
                    cell.number_format = '0.00'
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                elif col_index == 1:  # التاريخ
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                else:  # الإضافات
                    cell.alignment = Alignment(horizontal='right', vertical='center', wrap_text=True)
            
            total_flour += flour
            total_yeast += yeast
            total_salt += salt
            total_sugar += sugar
            total_oil += oil
            total_wood += wood
            total_gas += gas
            
            data_row += 1
        
        # إضافة صف الإجمالي
        if tasleemat:
            total_row = data_row
            
            # خلية "الإجمالي الكلي"
            ws.merge_cells(f'A{total_row}:A{total_row}')
            total_cell = ws.cell(row=total_row, column=1)
            total_cell.value = "الإجمالي الكلي"
            total_cell.fill = HEADER_FILL
            total_cell.font = header_font
            total_cell.border = BORDER
            total_cell.alignment = Alignment(horizontal='center', vertical='center')
            
            totals = [total_flour, total_yeast, total_salt, total_sugar, 
                     total_oil, total_wood, total_gas, ""]
            
            for col_index, total in enumerate(totals, start=2):
                cell = ws.cell(row=total_row, column=col_index)
                cell.value = total
                cell.fill = SECTION_FILL
                cell.font = bold_font
                cell.border = BORDER
                cell.alignment = Alignment(horizontal='center', vertical='center')
                if col_index < 9:  # الأعمدة الرقمية فقط
                    cell.number_format = '0.00'

        # ضبط أبعاد الأعمدة
        column_widths = {
            'A': 18, 'B': 25, 'C': 12, 'D': 12, 'E': 12,
            'F': 18, 'G': 25, 'H': 12, 'I': 12, 'J': 20
        }
        
        for col_letter, width in column_widths.items():
            ws.column_dimensions[col_letter].width = width

        # إعداد الاستجابة
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        
        filename = f"تقرير_مخبز_{makhbaz.name or 'غير_محدد'}.xlsx"
        import urllib.parse
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
        
        response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'
        response['Content-Encoding'] = 'utf-8'

        wb.save(response)
        return response
        
    except Exception as e:
        logger.error(f"Error exporting Excel for makhbaz {makhbaz_id}: {str(e)}")
        # للتصحيح، يمكنك طباعة الخطأ في الكونسول
        print(f"DEBUG - Error: {str(e)}")
        from django.contrib import messages
        messages.error(request, f"حدث خطأ أثناء تصدير الملف: {str(e)}")
        from django.shortcuts import redirect
        return redirect('makhabez_list')  # استبدل باسم view مناسب
        
