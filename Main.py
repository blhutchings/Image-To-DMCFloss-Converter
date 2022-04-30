import csv
import statistics
import time
import numpy as np
import cv2
import os
import DMC_Data
from ColourTransformation import closest_color

INPUT_FOLDER = "./input/"
OUTPUT_FOLDER = "./output/"

CVS = "dmc_table.csv"
DMC_Data.update(name=CVS)

# Parse floss database
reader = csv.reader(open(CVS, 'r'))
next(reader)  # Skip header

d = {}
for row in reader:
    DMC, Floss_Name, RGB, gimpHSV, opencvHSV = row  # Parse row
    d[opencvHSV] = [DMC, Floss_Name, RGB, gimpHSV]

# Set up palette
palette = [eval(i) for i in d.keys()]
print("Palette Size: ", len(palette))


def main():
    # For all files in input
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        print("Processing: " + file)
        filepath = INPUT_FOLDER + file
        filename, file_extension = os.path.splitext(file)
        file_out = filename #+ "_" + str(time.time_ns())

        picture_folder = os.path.join(OUTPUT_FOLDER, file_out) + "/"
        os.mkdir(picture_folder)

        # Load image
        im_org = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
        im_hsv = cv2.cvtColor(im_org, cv2.COLOR_BGR2HSV)

        # Dimensions
        height, width, channels = im_org.shape
        print("Width:", width)
        print("Height:", height)
        print("Channels:", channels)

        # Stats and Trackers
        pixel_count = width * height
        pixel_counter = 0
        progress_previous = 0

        # Shift color to DMC floss color
        non_alpha_color = (0, 0, 255)
        memory = {}
        for py in range(0, height):
            for px in range(0, width):
                pixel_hsv = tuple(im_hsv[py, px])  # HSV

                if pixel_hsv not in memory:
                    closest_colour = closest_color(pixel_hsv, palette)
                    memory[pixel_hsv] = closest_colour

                im_hsv[py, px] = memory[pixel_hsv]

                # If alpha, set the background color
                if channels == 4:
                    if im_org[py, px][3] != 255:
                        im_hsv[py, px] = non_alpha_color

                # Progress updates
                pixel_counter = pixel_counter + 1
                progress = int(pixel_counter / pixel_count * 100)
                if progress != progress_previous:
                    print(int(pixel_counter / pixel_count * 100), "%")
                progress_previous = progress

        im_bgr = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)

        # Re-add alpha channel
        alpha_channel = im_org[:, :, 3]
        output = np.dstack((im_bgr, alpha_channel))

        # Construct list with used colors
        colours_out = []
        for colour in memory.values():
            value = d[str(colour)]
            colours_out.append(value[0:3])
        print(str(len(colours_out)) + " colours used...")

        # Create csv with used colors
        with open(picture_folder + file_out + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["DMC", "Floss Name", "RGB"])
            writer.writerows(colours_out)
        print("Creating colour csv...")

        print("Writing images...")
        # Write Image
        cv2.imwrite((picture_folder + file_out + file_extension), output)



if __name__ == "__main__":
    main()
