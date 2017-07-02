"""
A general holder for all kinds of plots for now. Note all children are ingredients
in foodmate.


"""
import os
import numpy as np
import pandas as pd

import plotly as py
import plotly.graph_objs as go
py.tools.set_credentials_file(username='wangsen992', api_key='g3bks9Ikbcz0Thb4qtrc')

from bokeh.plotting import figure
from bokeh.models import Range1d, Legend
from bokeh.palettes import Category10, Viridis256, Magma256
from bokeh.io import export_png

nut_dict_file = "{root}/ragdoll/NUTR_DEF_more.csv".format(root=os.getcwd())
nut_dict_df = pd.read_csv(nut_dict_file, keep_default_na=False)

def donut_plot(meal, req_male, req_female):
	"""A custom function for create donut plots

	Parameters
	----------
	meal : MealComponent

	req : Human

	"""

	# obtain energy requirement
	energy_male = req_male.nutrients.nutrients['ENERC_KCAL'].value
	energy_female = req_female.nutrients.nutrients['ENERC_KCAL'].value
	energy = meal.nutrients.nutrients['ENERC_KCAL'].value
	energy_ratio_male = energy / energy_male
	energy_ratio_female = energy / energy_female

	# obtain AMDR for the meal
	prot = meal.nutrients.nutrients['PROCNT'].value * 4
	carbs = meal.nutrients.nutrients['CHOCDF'].value * 4
	fat = meal.nutrients.nutrients['FAT'].value * 9
	

	# Make the plots
	# make plot test
	fig = {
	  "data": [
	    {
	      "values": [energy_ratio_male, energy_ratio_female, 
	                 1 - energy_ratio_male - energy_ratio_female],
	      "labels": ['男性\n{perc:.0%}'.format(perc=energy_ratio_male),
	                 '女性\n{perc:.0%}'.format(perc=energy_ratio_female),
	                 '总需求<sup>a</sup>'],
	      "marker" : {'colors' : ['#FFF0EB', '#EEBBCC', '#D7C3E0']},
	      "domain": {"x": [0, .48]},
	      "textinfo":"label",
	      "hole": .4,
	      "type": "pie"
	    },     
	    {
	      "values": [prot, carbs, fat],
	      "labels": ['蛋白质', '碳水化合物', '脂肪'],
	      "text":"AMDR",
	      "textposition":"inside",
	      "marker" : {'colors' : ['#F4D3DE', '#C98592', '#B1DBCF']},
	      "domain": {"x": [.52, 1]},
	      "textinfo":"label+percent",
	      "hole": .4,
	      "type": "pie"
	    }],
	  "layout": {
	        "title":"Energy and Macro-nutrients",
	        "annotations": [
	            {
	                "font": {
	                    "size": 20
	                },
	                "showarrow": False,
	                "text": "热量",
	                "x": 0.198,
	                "y": 0.5
	            },
	            {
	                "font": {
	                    "size": 20
	                },
	                "showarrow": False,
	                "text": "AMDR<sup>b</sup>",
	                "x": 0.831,
	                "y": 0.5
	            }
	        ]
	    }
	}

	py.plotly.image.save_as(fig, '{}.png'.format(meal.name), scale=4)

def plot_paracoor(meal, human):
	"""A custom function for create parallel coordinate plots

		Parameters
		----------
		meal : MealComponent

		req : Human

		"""

	nuts = ['VITA_IU', 'VITC', 'TOCPHA', 'CA', 'MG', 'FE', 'MN', 'ZN', 'CU', 
			'K', 'P', 'NA', 'SE']

	nut_names = [nut_dict_df[nut_dict_df['abbr'] == abbr]['name_Foodmate'].values[0] for abbr in nuts]

	index = []
	data = []
	# organize data into workable formats
	for name, ingre in meal.items():
		index.append(name)

		# get nut data
		data.append([nut.value for nut in ingre.nutrients[nuts].values()])

	nut_df = pd.DataFrame(data=data, index=index, columns=nut_names)
	
	# now work on the requirements
	req_data = [nut.value for nut in human.nutrients[nuts].values()]
	req_df = pd.DataFrame(data=[req_data,], index=[human.name,], columns=nut_names)

	# get cumulative data
	cul_data = nut_df.divide(req_df.values[0],axis=1).cumsum(axis=0)

	def parallel_axis(data,
					  fname = "test.png",
					  title = "nutrition",
					  plot_size = [2100, 1500],
					  font_size = {'title' : '30pt',
					  			   'legend' : '5pt',
					  			   'xticks' : '30pt',
					  			   'yticks' : '30pt'}):

		nu_categories = data.columns.tolist()

		# bokeh setup

		COLORS = [Viridis256[int(i)] for i in np.arange(30, 256, (256-30)/data.index.size)]

		p = figure(title=title,
				   x_range = nu_categories,
				   plot_width = plot_size[0],
				   plot_height = plot_size[1])

		p.xaxis.major_label_orientation = np.pi/3

		p.y_range = Range1d(0, 1)
		p.title.text_font_size = font_size['title']
		p.xaxis.major_label_text_font_size = font_size['xticks']
		p.yaxis.major_label_text_font_size = font_size['yticks']

		# plot points
		for i in np.arange(data.index.size):
			p.circle(nu_categories,
					 data.loc[data.index[i]].values,
					 color = COLORS[i],
					 size = 5)
			p.line(nu_categories,
				   data.loc[data.index[i]].values,
				   color = COLORS[i],
				   line_width = 5)

			if i == 0:
				p.patch(nu_categories + list(reversed(nu_categories)),
						list(np.zeros(data.shape[1])) \
						+ list(reversed(list(data.loc[data.index[i]].values))),
						color = COLORS[i],
						alpha = 1)
			else:
				p.patch(nu_categories + list(reversed(nu_categories)),
						list(data.loc[data.index[i-1]].values) \
						+ list(reversed(list(data.loc[data.index[i]].values))),
						color = COLORS[i],
						alpha=1)

		return p

	p = parallel_axis(cul_data)
	fname = "{name}折线.png".format(name=meal.name)
	export_png(p, filename = fname)
