from .. import util
from ..DB.camp import Camp
from ..DB.plan import Plan
# from ..DB.refugee import Refugee
from ..Logic.person_data_retrieve import PersonDataRetrieve
from datetime import datetime

class CampDataRetrieve:

    @staticmethod
    def get_all_camps():
        camp_tuples = Camp.get_all_camps()
        return util.parse_result('Camp', camp_tuples)

    @staticmethod
    def get_camp(campID=None, location=None, shelter=None, water=None,food=None, medical_supplies=None, planID=None):
        # if location:
        #     if not util.is_country(location):
        #         return "You should enter a country name for real."

        if shelter:
            if util.is_num(shelter):
                if not util.is_positive(shelter):
                    return "Cannot enter a negative value to shelter."
            else:
                return "You should enter a number to shelter."

        if water:
            if util.is_num(water):
                if not util.is_positive(water):
                    return "Cannot enter a negative value to water level."
            else:
                return "You should enter a number to water level."
        if food:
            if util.is_num(food):
                if not util.is_positive(food):
                    return "Cannot enter a negative value to food level."
            else:
                return "You should enter a number to food level."
        if medical_supplies:
            if util.is_num(medical_supplies):
                if not util.is_positive(medical_supplies):
                    return "Cannot enter a negative value to medical_supplies."
            else:
                return "You should enter a number to medical_supplies."
        if planID:
            if util.is_num(planID):
                if not Plan.get_plan_by_id(planID):
                    return "Cannot find this planID. Please try again."
            else:
                return "You should enter a number to planID."
        camp_tuples = Camp.get_camp(campID, location, shelter, water, food, medical_supplies, planID)
        # add more validation procedure in the future
        return util.parse_result('Camp', camp_tuples)

    @staticmethod
    def get_camp_resources(campID):
        estimation = {}
        resources_name = ['water', 'food']
        refugees = PersonDataRetrieve.get_refugees(camp_id=campID)
        # if len(refugees) >0:
        #     # print("found some refs")
        #     # for refugee in refugees:
        #     #     print(refugee.display_info())
        # else:
        #     print("NO ref")
        #     return []
        camp = CampDataRetrieve.get_camp(campID=campID)
        if len(camp) >0:
            camp = camp[0]
            # print(camp.display_info())
        else:
            print("NO CAMP")
            # return []

        cost = 1
        cost_med = 1
        for refugee in refugees:
            # print(refugee.display_info())
            current_date = datetime.now()
            try:
                birth_date = datetime.strptime(refugee.date_of_birth, '%Y-%m-%d')
            except:
                return f"Invalid date format for refugee: {refugee.refugeeID}, wrong format: {refugee.date_of_birth}"
            age = current_date.year - birth_date.year - (
                    (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            if age < 18:
                cost += 1
            elif 18 <= age < 40:
                cost += 2
            else:
                cost += 0.8

            if refugee.medical_conditions is not None:
                cost_med += 1

        for resource in resources_name:
            value = getattr(camp, resource)  # value = camp.water
            estimation[resource.capitalize()] = (value // cost)

        medicine = getattr(camp, 'medical_supplies')
        estimation['Medical Supplies'] = (medicine // cost_med)

        return estimation

    @staticmethod
    def get_stats_triage_category(campID):
        triage_categories = ['None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate']
        lists = {
            category: PersonDataRetrieve.get_refugees(camp_id=campID, triage_category=category)
            for category in triage_categories
        }
        if all(isinstance(l, list) for l in lists.values()):
            total_list = lists['None'] + lists['Non-Urgent'] + \
                         lists['Standard'] + lists['Urgent'] + \
                         lists['Very-Urgent'] + lists['Immediate']
            num_total = len(total_list)
            if num_total > 0:
                num_none = len(lists['None'])
                num_non_urgent = len(lists['Non-Urgent'])
                num_standard = len(lists['Standard'])
                num_urgent = len(lists['Urgent'])
                num_very_urgent = len(lists['Very-Urgent'])
                num_immediate = len(lists['Immediate'])
                pct_none = (num_none/num_total)*100
                pct_non_urgent = (num_non_urgent/num_total)*100
                pct_standard = (num_standard/num_total)*100
                pct_very_urgent = (num_very_urgent/num_total)*100
                pct_urgent = (num_urgent/num_total)*100
                pct_immediate = (num_immediate/num_total)*100
                stats = {
                    'num_none': num_none,
                    'pct_none': pct_none,
                    'num_non_urgent': num_non_urgent,
                    'pct_non_urgent': pct_non_urgent,
                    'num_standard': num_standard,
                    'pct_standard': pct_standard,
                    'num_urgent': num_urgent,
                    'pct_urgent': pct_urgent,
                    'num_very_urgent': num_very_urgent,
                    'pct_very_urgent': pct_very_urgent,
                    'num_immediate':  num_immediate,
                    'pct_immediate':  pct_immediate
                }
            else:
                stats = "There is no refugee."
        else:
            stats = "There is an error"
        return stats

    @staticmethod
    def get_stats_gender(campID):
        list_male = PersonDataRetrieve.get_refugees(camp_id=campID, gender='Male')
        list_female = PersonDataRetrieve.get_refugees(camp_id=campID, gender='Female')
        list_other = PersonDataRetrieve.get_refugees(camp_id=campID, gender='Other')
        if isinstance(list_male, list) and isinstance(list_female, list) and isinstance(list_other, list):
            num_male = len(list_male)
            num_female = len(list_female)
            num_other = len(list_other)
            num_total = num_female + num_male + num_other
            if num_total < 1:
                return "There is no refugee"
            pct_male = (num_male/num_total)*100
            pct_female = (num_female/num_total)*100
            pct_other = (num_other/num_total)*100
            stats = {
                'num_male':num_male,
                'pct_male':pct_male,
                'num_female':num_female,
                'pct_female':pct_female,
                'num_other':num_other,
                'pct_other':pct_other
            }
        else:
            stats = "There is an error"
        return stats 
    
    @staticmethod
    def get_stats_age(campID):
        refugees = PersonDataRetrieve.get_refugees(camp_id=campID)
        if isinstance(refugees, list):
            num_total = len(refugees)
            if num_total > 0: 
                num_child = num_adult = num_elders = 0
                for refugee in refugees:
                    current_date = datetime.now()
                    try:
                        birth_date = datetime.strptime(refugee.date_of_birth, '%Y-%m-%d')
                    except:
                        return f"Invalid date format for refugee: {refugee.refugeeID}, wrong format: {refugee.date_of_birth}"
                    age = current_date.year - birth_date.year - (
                            (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
                    if age <= 18:
                        num_child += 1
                    elif 18 < age <= 65:
                        num_adult += 1
                    else:
                        num_elders += 1

                pct_child = (num_child/num_total)*100
                pct_adult = (num_adult/num_total)*100
                pct_elders = (num_elders/num_total)*100

                stats = {
                    'num_child':num_child,
                    'pct_child':pct_child,
                    'num_adult':num_adult,
                    'pct_adult':pct_adult,
                    'num_elders':num_elders,
                    'pct_elders':pct_elders
                }
            else:
                stats = {
                    'num_child':0,
                    'pct_child':0,
                    'num_adult':0,
                    'pct_adult':0,
                    'num_elders':0,
                    'pct_elders':0
                }
            return stats
        else:
            return refugees

    @staticmethod
    def get_stats_family(campID):
        try:
            all_separate_families = [i[0] for i in Camp.get_separate_family()]
            families = [i[0] for i in Camp.get_camp_families(campID)]
            num_families = len(families)
            camp_separate_families = []
            for i in families:
                if i in all_separate_families:
                    camp_separate_families.append(i)
            
            stats = {
                'num_families':num_families,
                'separate_families': camp_separate_families
            }
        except Exception as e:
            stats = str(e)
        return stats

    @staticmethod
    def get_stats_vital_status(campID):
        deads = PersonDataRetrieve.get_refugees(camp_id=campID, vital_status='Deceased')
        alives = PersonDataRetrieve.get_refugees(camp_id=campID, vital_status='Alive')
        if isinstance(deads, list) and isinstance(alives, list):
            num_dead = len(deads)
            num_alive = len(alives)
            num_total = num_alive + num_dead
            if num_total < 1:
                return "There is no refugee."
            pct_dead = (num_dead/num_total)*100
            pct_alive = (num_alive/num_total)*100
            stats = {
                'num_dead':num_dead,
                'pct_dead':pct_dead,
                'num_alive':num_alive,
                'pct_alive':pct_alive
            }
        else:
            stats = "An error occured"
        return stats