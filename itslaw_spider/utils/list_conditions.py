import itertools;

regions= ['北京市','天津市']
judgment_years = ['2020','2019']
court_level = ['高级人民法院','中级人民法院','初级人民法院']

def generate_all_conditions():
    conditions = []
    for item in itertools.product(regions,judgment_years,court_level):
       conditions.append({'region':'reason+1931+1+%s'%item[0],'judgmentYear':'region+1+6+%s'%item[1],'courtLevel':'courtLevel+2+12+%s'%item[2]})
    return conditions

def get_a_condition(index):
    conditions = generate_all_conditions()
    condition = {'totalCount': len(conditions)}
    if index is None or index == 0 or index >= len(conditions):
        condition['value'] = conditions[0]
    condition['value'] = conditions[index]
    return condition
        



        