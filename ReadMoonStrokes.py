#!/usr/bin/env python3

import os # for the reading of the file
import json # for the decoding of the file
import matplotlib.pyplot as plt # draw the strokes somewhere
from matplotlib.patches import Circle

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
class CGPoint:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		#self.z = z
	def __iter__(self):
		yield self.x
		yield self.y

class pencil_sample:
	def __init__(self, **sample):
		'''
		sample (dict): A dictionary with the following keys:
		location, timestamp, force, azimuth, altitude, rollAngle
		'''
		required_keys = ['location', 'timestamp', 'force', 'azimuth', 'altitude', 'rollAngle']
		for key in required_keys:
			if key not in sample:
				raise Exception(f'The sample must have "{key}" key')
		self.location = sample['location']
		self.timestamp = sample['timestamp']
		self.force = sample['force']
		self.azimuth = sample['azimuth']
		self.altitude = sample['altitude']
		self.rollAngle = sample['rollAngle']


class pencil_stroke:
	def __init__(self, samples):
		self.samples = samples
	def __len__(self):
		return len(self.samples)
	def __getitem__(self, index):
		return self.samples[index]
	def min(self):
		''' returns the minimum corner for the containin box '''
		if len(self.samples) == 0:
			return None
		mnx, mny = self.samples[0].location.x, self.samples[0].location.y
		for sample in self.samples:
			if sample.location.x < mnx:
				mnx = sample.location.x
			if sample.location.y < mny:
				mny = sample.location.y
		return (mnx, mny)
	def max(self):
		if len(self.samples) == 0:
			return None
		mxx, mxy = self.samples[0].location.x, self.samples[0].location.y
		for sample in self.samples:
			if sample.location.x > mxx:
				mxx = sample.location.x
			if sample.location.y > mxy:
				mxy = sample.location.y
		return (mxx, mxy)

class pencil_strokes_array:
	def __init__(self, value):
		self.value = value # the array of pencil strokes
	def __len__(self): # wrapper function gets at the array
		return len(self.value)
	def __getitem__(self, item): # wrapper function
		return self.value[item]
	def min(self):
		if len(self.value) == 0:
			return None
		(mnx, mny) = self.value[0].min()
		for stroke in self.value:
			(MINx, MINy) = stroke.min()
			#print("testing for new min", MINx, MINy)
			if MINx < mnx:
				#print("A new min on x...")
				mnx = MINx
			if MINy < mny:
				mny = MINy
		return (mnx, mny)
	def max(self):
		if len(self.value) == 0:
			return None
		(mxx, mxy) = self.value[0].max()
		for stroke in self.value:
			(MAXx, MAXy) = stroke.max()
			#print("testing for new max", MAXx, MAXy)
			if MAXx > mxx:
				#print("A new max on x...")
				mxx = MAXx
			if MAXy > mxy:
				mxy = MAXy
		return (mxx, mxy)

if __name__ == '__main__':
#	print('Running some standard operations to get a feel for the code to do file stuff...')
#	cwd = os.getcwd()
#	print("os.getcwd() gives", cwd)
#
#	directories = [d for d in os.listdir(cwd) if os.path.isdir(d)]
#	DirFound = False
#	for d in directories:
#		if d == "MoonStrokeFiles":
#			print("found the directory MoonStrokeFiles")
#			DirFound = True
#		else:
#			print(f"directory {d} is not the directory I am looking for")
#	if not DirFound:
#		print("Directory not found, exiting the program")
#		exit(1)
##	file_path = os.path.join(cwd, "MoonStrokeFiles", "Binary_Cross_Entropy.moonstroke")
##	if os.path.exists(file_path):
##		with open(file_path, "r") as f:
##			count = 0
##			for i in range(5):
##				line = f.readline()
##				if not line: break
##				#print(line.strip())
##				count += 1
##				data = json.loads(line)
##			#print(f"Read and printed {count} lines...")
#
#	else:
#			print(f"File with path \"{file_path}\" not found, exiting the program")
	with open('MoonStrokeFiles/Binary_Cross_Entropy.moonstroke', 'r') as file:
		data = json.load(file)

	print(f"len(data) = {len(data)}")
	#print(f"data =\n{data}")
	value_array = data["value"] # array of strokes, here strokes are still dictionaries w/ "samples"
	NStrokes = len(value_array)
	print(f"Number of strokes (len(data[\"value\"])): {NStrokes}")
	strokes = []
	for i in range(NStrokes):
		stroke_array = value_array[i]['samples']
		#print(f"len of stroke_array[{i}] = {len(stroke_array)}")
		pencil_samples = [] # for each stroke, make an array of pencil samples
		for j in range(len(stroke_array)): # convert the inputs of dictionaries to type pencil samples
			d ={}
			x = stroke_array[j]['location'][0]
			y = stroke_array[j]['location'][1]
			d['location'] = CGPoint(x, y) # could also do ... = CGPoint(*stroke_array[j]['location'])
			d['force'] = stroke_array[j]['force']
			d['azimuth'] = stroke_array[j]['azimuth']
			d['altitude'] = stroke_array[j]['altitude']
			d['rollAngle'] = stroke_array[j]['rollAngle']
			d['timestamp'] = stroke_array[j]['timestamp']
			ps = pencil_sample(**d)
			pencil_samples.append(ps)
		psa = pencil_stroke(pencil_samples)
		strokes.append(psa)
	all_strokes = pencil_strokes_array(strokes)

	# Plotting using matplotlib
	fig, ax = plt.subplots(figsize=(18, 16))


	#minx, miny = all_strokes[index].min()
	minx, miny = all_strokes.min()
	maxx, maxy = all_strokes.max()
	x_range = maxx - minx
	y_range = maxy - miny
	svg_points = []
	svg_width = x_range #800
	svg_height = y_range #600
	filename = "scratch_page.svg"
	path_data = ""
	for index in range(len(all_strokes)):
		for i in range(len(all_strokes[index]) - 1):
			#print(".", end="")
			#x, y = all_strokes[index][i].location.x - minx, all_strokes[index][i].location.y - miny
			x, y = all_strokes[index][i].location.x, all_strokes[index][i].location.y
			svg_x = ((x - minx)/x_range)*(svg_width)#
			svg_y = ((y - miny)/y_range)*(svg_height)
			svg_points.append(f"{svg_x},{svg_y}")
			circle = Circle((x, y), radius=1, color='red')
			ax.add_patch(circle)
		# Create SVG path data using quadratic Bezier
		if len(svg_points) >= 3:
			path_data += f"M {svg_points[0]}"
			for i in range(1, len(svg_points) - 1):
				# Create smooth curve using using quadratic Bexier for better results
				if i == 1:
					path_data += f" Q {svg_points[0]} {svg_points[1]}"
				else:
					path_data += f" Q {svg_points[i-1]} {svg_points[i]}"
			# Add final point
			if len(svg_points) > 2:
				path_data += f" T {svg_points[-1]} "
			else:
				path_data += " "
			
			# Write SVG file
	svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="100%" height="100%" fill="white"/>
  
  <!-- Stroke curve -->
  <path d="{path_data}" 
        stroke="white" 
        stroke-width="0.5" 
        fill="none"/>
        
  <!-- Points markers -->
  {''.join([f'<circle cx="{point.split(",")[0]}" cy="{point.split(",")[1]}" r="3" fill="red"/>' for point in svg_points])}
</svg>"""

	with open(filename, 'w') as f:
		f.write(svg_content)

	print(f"SVG file '{filename}' created successfully!")


	# Set plot limits and labels
	ax.set_xlim(minx - 1, maxx + 1)
	ax.set_ylim(miny - 1, maxy + 1)
	ax.invert_yaxis()  # Invert y-axis to match the typical orientation of drawings
	ax.set_title('MoonStrokes Plot')
	ax.set_xlabel('X Coordinate')
	ax.set_ylabel('Y Coordinate')

	plt.show()

print("yes?")

import code
code.interact(local=locals())
