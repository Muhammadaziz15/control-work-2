from .models import CompanyInfo


def company_info(request):
    return {'site_company': CompanyInfo.objects.first()}
