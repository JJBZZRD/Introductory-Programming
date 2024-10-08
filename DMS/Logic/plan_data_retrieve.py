from ..DB.plan import Plan
from ..DB.refugee import Refugee
from .. import util
from datetime import datetime
from . import logic_util
from ..Logic.person_data_retrieve import PersonDataRetrieve
from ..DB.camp import Camp

class PlanDataRetrieve:

    @staticmethod
    def get_all_plans():
        plan_tuples = Plan.get_all_plans()
        return util.parse_result('Plan', plan_tuples)

    @staticmethod
    def get_plan(planID=None, start_date=None, end_date=None, name=None, 
                 country=None, event_name=None, description=None, active=None):
        
        if name:
            name = logic_util.validate_name(name)
        if country:
            country = logic_util.validate_country(country)
        if event_name:
            event_name = logic_util.validate_event(event_name)
        if description:
            description = logic_util.validate_description(description)
        if start_date:
            start_date = logic_util.validate_date(start_date)
        if end_date:
            end_date = logic_util.validate_date(end_date)

        print(f' ======== [DEBUG] PlanDataRetrieve.get_plan: planID: {planID}, start_date: {start_date}, end_date: {end_date}, name: {name}, country: {country}, event_name: {event_name}, desc: {description} ============ ')

        if active:
            status = 'Active'
        elif active == None:
            status = None
        else:
            status = 'Ended'

        plan_tuples = Plan.get_plan(planID=planID, start_date=start_date, end_date=end_date, name=name, country=country, event_name=event_name, description=description, status=status)

        plans = util.parse_result('Plan', plan_tuples)
        print(f' ======== [DEBUG] PlanDataRetrieve.get_plan: plans: {plans} ============ ')
        if isinstance(plans, list):

            return plans
        else:
            return f"Cannot find plan with id {planID}"

    @staticmethod
    def get_resources(planID):
        try:
            plan = PlanDataRetrieve.get_plan(planID=planID)[0]
        except:
            return f"Cannot find plan with id {planID}"
        return [plan.shelter, plan.food, plan.water, plan.medical_supplies]

    @staticmethod
    def get_plan_resources_estimate(planID):
        refugees_tuples = Refugee.get_refugees_by_plan(planID)

        refugees = util.parse_result('Refugee', refugees_tuples)
        total_refugees = len(refugees_tuples)

        plan_resources = PlanDataRetrieve.get_resources(planID)

        nutrition_cost = 1
        medical_cost = 1

        for refugee in refugees:
            current_date = datetime.now()
            try:
                birth_date = datetime.strptime(refugee.date_of_birth, '%Y-%m-%d')
            except:
                birth_date = datetime.strptime(refugee.date_of_birth, '%Y/%m/%d')
            refugee.age = current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            if refugee.age < 18:
                nutrition_cost += 1
            elif refugee.age > 40:
                nutrition_cost += 0.8
            else: 
                nutrition_cost += 2

            if refugee.triage_category == 'Immediate':
                medical_cost += 3
            elif refugee.triage_category == 'Very-Urgent':
                medical_cost += 2.5 
            elif refugee.triage_category == 'Urgent':
                medical_cost += 2
            elif refugee.triage_category == 'Standard':
                medical_cost += 1
            elif refugee.triage_category == 'Non-Urgent':
                medical_cost += 0.5
    
        est_food = plan_resources[0]//nutrition_cost
        est_water = plan_resources[1]//nutrition_cost
        est_medical = plan_resources[3]//medical_cost

        est_resources = [est_food, est_water, est_medical]

        return est_resources

    @staticmethod
    def get_stats_triage_category(planID):
        triage_categories = ['None', 'Non-Urgent', 'Standard', 'Urgent', 'Very-Urgent', 'Immediate']
        lists = {
            category: PersonDataRetrieve.get_refugees_by_plan(planID, category)
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
    def get_stats_gender(planID):
        list_male = PersonDataRetrieve.get_refugees_by_plan(planID, gender='Male')
        list_female = PersonDataRetrieve.get_refugees_by_plan(planID, gender='Female')
        list_other = PersonDataRetrieve.get_refugees_by_plan(planID, gender='Other')
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
    def get_stats_age(planID):
        refugees = PersonDataRetrieve.get_refugees_by_plan(planID)
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
    def get_stats_family(planID):
        try:
            all_separate_families = [i[0] for i in Camp.get_separate_family()]
            families = [i[0] for i in Plan.get_plan_families(planID)]
            num_families = len(families)
            plan_separate_families = []
            for i in families:
                if i in all_separate_families:
                    plan_separate_families.append(i)
            
            stats = {
                'num_families':num_families,
                'separate_families': plan_separate_families
            }
        except Exception as e:
            stats = str(e)
        return stats

    @staticmethod
    def get_stats_vital_status(planID):
        deads = PersonDataRetrieve.get_refugees_by_plan(planID, vital_status='Deceased')
        alives = PersonDataRetrieve.get_refugees_by_plan(planID, vital_status='Alive')
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