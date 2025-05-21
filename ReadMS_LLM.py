#!/usr/bin/env python3

import os  # for the reading of the file
import json  # for the decoding of the file
import matplotlib.pyplot as plt  # for drawing the strokes somewhere

# Define the CGPoint class to store location coordinates
class CGPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Define the pencil_sample class to store sample data
class pencil_sample:
    def __init__(self, **sample):
        required_keys = ['location', 'timestamp', 'force', 'azimuth', 'altitude', 'rollAngle']
        for key in required_keys:
            if key not in sample:
                raise Exception(f'The sample must have "{key}" key')
        
        self.location = CGPoint(*sample['location'])
        self.timestamp = sample['timestamp']
        self.force = sample['force']
        self.azimuth = sample['azimuth']
        self.altitude = sample['altitude']
        self.rollAngle = sample['rollAngle']

# Define the pencil_stroke class to store an array of samples
class pencil_stroke:
    def __init__(self, samples):
        self.samples = samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]

    def min(self):
        if not self.samples:
            return None
        mnx, mny = self.samples[0].location.x, self.samples[0].location.y
        for sample in self.samples:
            if sample.location.x < mnx:
                mnx = sample.location.x
            if sample.location.y < mny:
                mny = sample.location.y
        return (mnx, mny)

    def max(self):
        if not self.samples:
            return None
        mxx, mxy = self.samples[0].location.x, self.samples[0].location.y
        for sample in self.samples:
            if sample.location.x > mxx:
                mxx = sample.location.x
            if sample.location.y > mxy:
                mxy = sample.location.y
        return (mxx, mxy)

# Define the pencil_strokes_array class to store an array of strokes
class pencil_strokes_array:
    def __init__(self, strokes):
        self.strokes = strokes

    def __len__(self):
        return len(self.strokes)

    def __getitem__(self, index):
        return self.strokes[index]

# Main code to read the data and plot it using matplotlib
if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the JSON file (assuming the file is in the same directory)
    json_file_path = os.path.join(current_dir, 'data.json')
    
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    value_array = data['value']
    strokes = []

    for stroke_data in value_array:
        pencil_samples = []
        sample_array = stroke_data['samples']
        
        for sample_dict in sample_array:
            location = CGPoint(*sample_dict['location'])
            ps = pencil_sample(
                location=location,
                force=sample_dict['force'],
                azimuth=sample_dict['azimuth'],
                altitude=sample_dict['altitude'],
                rollAngle=sample_dict['rollAngle'],
                timestamp=sample_dict['timestamp']
            )
            pencil_samples.append(ps)
        
        stroke = pencil_stroke(pencil_samples)
        strokes.append(stroke)

    all_strokes = pencil_strokes_array(strokes)

    # Plotting using matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))

    for stroke in all_strokes:
        x_coords = [sample.location.x for sample in stroke]
        y_coords = [sample.location.y for sample in stroke]

        min_x, min_y = stroke.min()
        max_x, max_y = stroke.max()

        # Normalize coordinates to fit within the plot area
        x_coords = [(x - min_x) * 2 for x in x_coords]
        y_coords = [(y - min_y) * 2 for y in y_coords]

        ax.plot(x_coords, y_coords, color='green', linewidth=2)

    # Set plot limits and labels
    ax.set_xlim(0, max([stroke.max()[0] - stroke.min()[0] for stroke in all_strokes]) * 2)
    ax.set_ylim(0, max([stroke.max()[1] - stroke.min()[1] for stroke in all_strokes]) * 2)
    ax.invert_yaxis()  # Invert y-axis to match the typical orientation of drawings
    ax.set_title('MoonStrokes Plot')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    plt.show()
