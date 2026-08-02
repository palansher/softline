from company.office import *


office_first_salaries = get_salaries("Московская 8",10)
office_second_salaries = get_salaries("Чапаева 89",5)
office_third_salaries = get_salaries("Омская 18",8)

company = [office_first_salaries,office_second_salaries,office_third_salaries]
for office in company:
    show_salaries(office)
    print("="*50)