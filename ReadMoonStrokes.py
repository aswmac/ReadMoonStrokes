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
#
#        if 'location' not in sample:
#            raise Exception('The sample must have "location" key')
#        if 'timestamp' not in sample:
#            raise Exception('The sample must have "timestamp" key')
#        if 'force' not in sample:
#            raise Exception('The sample must have "force" key')
#        if 'azimuth' not in sample:
#            raise Exception('The sample must have "azimuth" key')
#        if 'altitude' not in sample:
#            raise Exception('The sample must have "altitude" key')
#        if 'rollAngle' not in sample:
#            raise Exception('The sample must have "rollAngle" key')
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
        self.value = value
    def __len__(self):
        return len(self.value)
    def __getitem__(self, item):
        return self.value[item]

if __name__ == '__main__':
    print('Running some standard operations to get a feel for the code to do file stuff...')
    cwd = os.getcwd()
    print("os.getcwd() gives", cwd)

    directories = [d for d in os.listdir(cwd) if os.path.isdir(d)]
    DirFound = False
    for d in directories:
        if d == "MoonStrokeFiles":
            print("found the directory MoonStrokeFiles")
            DirFound = True
        else:
            print(f"directory {d} is not the directory I am looking for")
    if not DirFound:
        print("Directory not found, exiting the program")
        exit(1)
    file_path = os.path.join(cwd, "MoonStrokeFiles", "Untitled 122.moonstroke")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            count = 0
            for i in range(5):
                line = f.readline()
                if not line: break
                #print(line.strip())
                count += 1
                data = json.loads(line)
            print(f"Read and printed {count} lines...")
            #print(f"Read in {count} lines (max lines of 5)")

    else:
        print(f"File with path \"{file_path}\" not found, exiting the program")
    print(f"len(data) = {len(data)}")
    #print(f"data =\n{data}")
    value_array = data["value"] # array of strokes, here strokes are still dictionaries w/ "samples"
    NStrokes = len(value_array)
    print(f"Number of strokes (len(data[\"value\"])): {NStrokes}")
    strokes = []
    for i in range(NStrokes):
        stroke_array = value_array[i]['samples']
        print(f"len of stroke_array[{i}] = {len(stroke_array)}")
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
    fig, ax = plt.subplots(figsize=(8, 6))

    index = (3)%len(all_strokes)
    minx, miny = all_strokes[index].min()
    for i in range(len(all_strokes[index]) - 1):
        x, y = all_strokes[index][i].location.x - minx, all_strokes[index][i].location.y - miny
        circle = Circle((x, y), radius=1, color='red')
        ax.add_patch(circle)


    # Set plot limits and labels
    ax.set_xlim(0, max([stroke.max()[0] - stroke.min()[0] for stroke in all_strokes]) * 2)
    ax.set_ylim(0, max([stroke.max()[1] - stroke.min()[1] for stroke in all_strokes]) * 2)
    ax.invert_yaxis()  # Invert y-axis to match the typical orientation of drawings
    ax.set_title('MoonStrokes Plot')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    plt.show()

print("yes?")
