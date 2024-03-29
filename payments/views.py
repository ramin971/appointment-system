from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse,Http404
from appointment.models import Patient
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse

# from appointment.views import me
def go_to_gateway_view(request):
    print('@@@@@@gateway ')
    # print('@@@@@@kws',kwargs)
    # kwargs.get('serializer').save()
    # print('####serializer',a)
    # خواندن مبلغ از هر جایی که مد نظر است
    #old
    # amount = int(kwargs.get('fee',50000))
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    #old
    # user_mobile_number = kwargs.get('patient_phone',+989123456789) # اختیاری

    amount = request.session.get('fee')
    user_mobile_number = request.session.get('phone')
    print('$$$',amount,user_mobile_number)

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback-gateway'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        print('######bankrecord',bank_record)
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        # TODO: redirect to failed page.
        raise e
    

def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    patient_id = request.session.get('pat_id')
    # patient = Patient.objects.get(pk=patient_id)
    patient = get_object_or_404(Patient,pk=patient_id)
    # print('$$$$$$$$$$tc',tracking_code)
    # print('type tc:$',type(tracking_code))

    if not tracking_code:
        #patient.delete()
        # logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        #patient.delete()
        # logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # print('session_pat:######',request.session.get('pat_id'))
        # serializer = PatientSerializer(patient,tc=tracking_code)
        # serializer.is_valid(raise_exception=True)
        # tc must be unique
        # serializer.save()
        # print('*****',bank_record)
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        # result = serializer.data
        # result['tracking_code'] = tracking_code
        # result['result'] = "پرداخت با موفقیت انجام شد." 
        # return Response(serializer.data,status=status.HTTP_200_OK)
        # return me(request,tc=tracking_code)
        patient.tracking_code = tracking_code
        patient.save()
        
        del request.session['phone']
        del request.session['fee']
        del request.session['pat_id']
        return redirect(reverse('receipt',kwargs={'tc':tracking_code}))
    
    #patient.delete()
    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

