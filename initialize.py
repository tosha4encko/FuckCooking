import json
import pandas as pd
import numpy as np

train = pd.read_json('./train.json')
test = pd.read_json('./test.json')

#Создает предикаты для тех ингридиентов, частота вхождения которых удовлетворяет lower_bounds и upper_bounds
def create_subParams(df, count_all_class:int, lower_bounds: int, upper_bounds: int):
    count_in = dict()
    for ingredients in df.loc[:, 'ingredients']:
        for ingridient in ingredients:
            if ingridient in count_in.keys():
                count_in[ingridient] += 1
            else:
                count_in[ingridient] = 0

    ind = create_subData(count_all_class)
    data = df.loc[ind, :]
    ingredients = []
    for key in count_in.keys():
        if count_in[key] > lower_bounds and count_in[key] < upper_bounds:
            ingredients.append(key)

    for ingredient in ingredients:
        data[ingredient] = [0 for i in range(data.shape[0])]

    for i in ind:
        for ingredient in ingredients:
            if ingredient in data.loc[i, 'ingredients']:
                data.loc[i, ingredient] = 1
    return data

#Формирует сбалансированную выборку, count_one_cuisine -- колличество объектов каждого класса
def create_subData(count_one_cuisine:int):
    count_res_obj = 0
    res_dict = dict()
    for i in range(39774):
        cuisine = train.loc[i, 'cuisine']
        if cuisine in res_dict.keys():
            if len(res_dict[cuisine]) < count_one_cuisine:
                res_dict[cuisine].append(i)
                if len(res_dict[cuisine]) == count_one_cuisine:
                    count_res_obj += 1
        else:
            res_dict[cuisine] = [i]
            
        if count_res_obj == 20:
            break
    return np.hstack([res_dict[key] for key in res_dict.keys()])

