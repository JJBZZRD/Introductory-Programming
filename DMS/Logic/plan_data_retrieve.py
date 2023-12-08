from ..DB.plan import Plan
from ..DB.refugee import Refugee
from .. import util
from datetime import datetime
from . import logic_util


class PlanDataRetrieve:

    @staticmethod
    def get_plans():
        plan_tuples = Plan.get_all_plans()
        return util.parse_result('Plan', plan_tuples)

    @staticmethod
    def get_plan(planID=None, start_date=None, end_date=None, name=None, 
                 country=None, event_name=None, description=None, active=None):
        
        #Validate user input
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
        
        plan_tuples = Plan.get_plan(planID=planID, start_date=start_date, end_date=end_date, name=name, 
                 country=country, event_name=event_name, description=description)

        plans = util.parse_result('Plan', plan_tuples)
        if isinstance(plans, list):
            for plan in plans:
                plan.food, plan.water, plan.shelter, plan.medical_supplies = Plan.get_total_resources(plan.planID)
        return plans


    @staticmethod
    def get_plan_resources_estimate(planID):
        refugees_tuples = Refugee.get_by_planID(planID)
        refugees = util.parse_result(refugees_tuples)
        total_refugees = len(refugees_tuples)

        plan_resources = Plan.get_total_resources(planID)
        #[food, water, shelter, medical supplies]

        nutrition_cost = 1
        medical_cost = 1

        for refugee in refugees:
            current_date = datetime.now()
            birth_date = datetime.strptime(refugee.date_of_birth, '%Y-%m-%d')
            refugee.age = current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            if refugee.age < 18:
                nutrition_cost += 1
            elif refugee.age > 40:
                nutrition_cost += 0.8
            else: 
                nutrition_cost += 2

            if refugee.medical_conditions is not None:
                medical_cost += 1
    
        est_food = plan_resources[0]//nutrition_cost
        est_water = plan_resources[1]//nutrition_cost
        est_medical = plan_resources[3]//medical_cost

        est_resources = [est_food, est_water, est_medical]

        return est_resources
