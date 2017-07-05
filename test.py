"""
A test for ragdoll.
"""

from ragdoll import *

mongo = MongoDB(host='47.93.246.201', port=27017, database='eatech', user='harry', password='password')

meal_dict = {"五谷饭" : "595597b5d4ae8333cc8e257e",
			 "混合沙拉" : "593bc7e2445ba7052fa73d6b",
			 "五谷套餐龙利鱼" : "59583ff5d4ae831089f4e5e1",
			 "五谷套餐番茄牛腩" : "595864acd4ae831417e50208",
			 "五谷套餐鸡胸肉" : "59586615d4ae831417e50209",
			 "手撕猪肉卷" : "59585ea6d4ae831417e50205",
			 "至尊豪华卷" : "59585f8fd4ae831417e50206",
			 "西班牙炖牛肉卷" : "5958615cd4ae831417e50207",
			 "鸡肉沙拉" : "595867f7d4ae831417e5020a",
			 "鸡蛋沙拉" : "59586898d4ae831417e5020b",
			 "金枪鱼沙拉" : "59588cabd4ae8320b8e1915d",
			 "大虾沙拉" : "595874a9d4ae831417e5020e",
			 "莎莎酱玉米片" : "59587030d4ae831417e5020d",
			 "番茄炖牛腩" : "5958433ed4ae831089f4e5e2",
			 "墨西哥BBQ手撕猪肉" : "59584ae8d4ae831089f4e5e4",
			 "墨西哥皮克伽罗酱" : "59584ee6d4ae831089f4e5e7",
			 "墨西哥莎莎酱" : "59584dd4d4ae831089f4e5e6"
			 }

meal = mongo.retrieve_item("DIY", "595597b5d4ae8333cc8e257e")

# prob_dict = {}
# nuts = ['ENERC_KCAL', 'PROCNT', 'CHOCDF', 'FAT', 'FIBTG', 'VITA_IU', 'VITA_IU', 
#         'VITC', 'NIA', 'RIBF', 'CHOLE', 'THIA',  'TOCPHA', 'CARTB', 'CA', 
#         'MG', 'FE', 'MN', 'ZN', 'CU', 'K', 'P', 'NA', 'SE']

# test_man = Human(name='man', 
#     			 gender='male', 
#     			 age=25, 
#     			 height=175, 
#     			 weight=68, 
#     			 PAL=1.2, 
#     			 AMRD={"PROCNT" : 0.25,
# 						 "FAT"    : 0.25,
# 						 "CHOCDF" : 0.5})
# test_woman = Human(name='woman', 
#     			   gender='female', 
#     			   age=25, 
#     			   height=165, 
#     			   weight=50, 
#     			   PAL=1.2, 
#     			   AMRD={"PROCNT" : 0.25,
# 						 "FAT"    : 0.25,
# 						 "CHOCDF" : 0.5})

# test_man.get_req(mongo, 'old_req')
# test_woman.get_req(mongo, 'old_req')

# print(test_man.nutrients)
# print(test_woman.nutrients)


# def operation(meal):

# 	meal.nutrients = meal.nutrients[nuts]

# 	with open("{name}.txt".format(name=meal.name), 'w') as fout:

# 		fout.write("餐名 : {name}\n".format(name=meal.name))
# 		fout.write("成分\n")
# 		fout.write(meal.__repr__())


# 	# donut_plot(meal, test_man, test_woman)

# 	plot_paracoor(meal.flatten(), test_man)

# err_list = []

# for name, item_id in prob_dict.items():

# 	print("Working on {name}...\n".format(name=name))

# 	if "{name}折线.png".format(name=name) in os.listdir():
# 		continue


# 	meal = mongo.retrieve_item("DIY", item_id)
# 	operation(meal)


