'''
Generate a YAML file with the pixel layout and chip connections for the
packaged 1x1-rev2 pixel tile

'''
import yaml
import patterngenerator as pg

pixels = []
subgrid_width = 16
chip_ids = (2,)
pixel_pitch = 4.434
width = pixel_pitch*7
height = pixel_pitch*7
for chip in chip_ids:
    x = pixel_pitch/2 - width/2
    y = pixel_pitch/2 - height/2
    pixels.extend(pg.pixels_plain_grid(pixel_pitch, 1, 1, x, y, len(pixels), batch_size=7, pixels_per_grid=49))

pixelids = dict()
for chip_idx, chip in enumerate(chip_ids):
    # Bool value is argument to right_side_up
    chip_pixels = list(range(chip_idx*49, chip_idx*49 + 49))
    pixelids[chip] = (True, 'plain', chip_pixels)

chips = []
for chipid, (right_side_up, shape, ids) in pixelids.items():
    assignment = pg.grid_7x7_assignments_0_64_v2_1_0
    channels = pg.assign_pixels(ids, assignment, right_side_up, range(64))
    chips.append([chipid, channels])

with open('layout-2.1.0.yaml', 'w') as f:
    yaml.dump({'pixels': pixels, 'chips': chips, 'x': -width/2, 'y': -height/2,
        'width': width, 'height': height}, f)
