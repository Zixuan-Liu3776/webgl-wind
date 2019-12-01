import rasterio
import sys
import json

out_data = {"width":0, "height":0, "u": {"specs":{"maximum":-1*float("inf"), "minimum":float("inf")}, "values":[]}, "v":{"specs":{"maximum":-1*float("inf"), "minimum":float("inf")}, "values":[]}}

with rasterio.open(sys.argv[1]) as fileref:
	band = fileref.read(1, masked=True)
	band_mask = fileref.read_masks(1)
	out_data["width"] = fileref.width
	out_data["height"] = fileref.height
	for j in range(fileref.height):
		for i in range(fileref.width):
			if (band_mask[j, i]):
				out_data["u"]["values"] += [band[j, i]]
				if (band[j, i] > out_data["u"]["specs"]["maximum"]):
					out_data["u"]["specs"]["maximum"] = band[j,i]
				if (band[j,i] < out_data["u"]["specs"]["minimum"]):
					out_data["u"]["specs"]["minimum"] = band[j,i]
			else:
				out_data["u"]["values"] += [0.0]
				if (0.0 > out_data["u"]["specs"]["maximum"]):
					out_data["u"]["specs"]["maximum"] = 0.0
				if (0.0 < out_data["u"]["specs"]["minimum"]):
					out_data["u"]["specs"]["minimum"] = 0.0

with rasterio.open(sys.argv[2]) as fileref:
	band = fileref.read(1, masked=True)
	band_mask = fileref.read_masks(1)
	for j in range(fileref.height):
		for i in range(fileref.width):
			if (band_mask[j, i]):
				out_data["v"]["values"] += [band[j, i]]
				if (band[j, i] > out_data["v"]["specs"]["maximum"]):
					out_data["v"]["specs"]["maximum"] = band[j,i]
				if (band[j,i] < out_data["v"]["specs"]["minimum"]):
					out_data["v"]["specs"]["minimum"] = band[j,i]
			else:
				out_data["v"]["values"] += [0.0]
				if (0.0 > out_data["v"]["specs"]["maximum"]):
					out_data["v"]["specs"]["maximum"] = 0.0
				if (0.0 < out_data["v"]["specs"]["minimum"]):
					out_data["v"]["specs"]["minimum"] = 0.0

with open("tmp.json", 'w') as outfile:
	json.dump(out_data, outfile)





