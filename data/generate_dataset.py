import json
import os
import random
random.seed(42)

dataset_path = 'shallalist/'
desired_positive_categories = ['porn', 'models']

folders = sorted([tup for tup in os.walk(dataset_path)])

nonallowed_characters = ['_', '&', '#', ';', '/', 'ü', ',', 'ö', '"', 'ı']

desired_negative_categories = []

for tup in folders:
	if 'domains' in tup[2] and 'urls' in tup[2]:
		desired_negative_categories.append(tup[0][len(dataset_path):])

desired_negative_categories = list(set(desired_negative_categories) - set(desired_positive_categories))

# Generates a JSON dataset for positives and negatives from the Shallist set of blacklists
def generate_dataset(dataset_path, desired_positive_categories, desired_negative_categories, save_path="dataset.json"):

	# Validate category names and file structure
	for cat in desired_positive_categories + desired_negative_categories:
		assert(os.path.isfile(dataset_path + cat + "/domains"))

	assert(len(set(desired_positive_categories + desired_negative_categories)) == len(desired_positive_categories) + len(desired_negative_categories))

	positives = []
	negatives = []
	for cat in desired_positive_categories + desired_negative_categories:
		with open(dataset_path + cat + "/domains", 'r') as f:
			raw_urls = f.read()
		urls = raw_urls.split()
		if cat in desired_positive_categories:
			positives += urls
		else:
			negatives += urls

    # Remove unallowed characters

	initial_positive_length = len(positives)
	initial_negative_length = len(negatives)

	new_positives = []
	for url in positives:
		allowed = True
		for char in nonallowed_characters:
			if char in url:
				allowed = False
		if allowed:
			new_positives.append(url)
	positives = new_positives

	new_negatives = []
	for url in negatives:
		allowed = True
		for char in nonallowed_characters:
			if char in url:
				allowed = False
		if allowed:
			new_negatives.append(url)
	negatives = new_negatives

	print(initial_positive_length - len(positives), "invald character positives removed.")
	print(initial_negative_length - len(negatives), "invalid character negatives removed.")



	# Remove duplicates

	initial_positive_length = len(positives)
	initial_negative_length = len(negatives)

	positives = [pos.lower() for pos in positives]
	negatives = [neg.lower() for neg in negatives]

	# Ensures no duplicates within lists
	positives = set(positives)
	negatives = set(negatives)

	print(initial_positive_length - len(positives), "duplicate positives removed.")
	print(initial_negative_length - len(negatives), "duplicate negatives removed.")

	count = 0
	for x in positives:
		if x in negatives:
			negatives.remove(x)
			count += 1
	print(count, "duplicates removed across lists by removing from negatives.")

	positives = list(positives)
	negatives = list(negatives)

	random.shuffle(positives)
	random.shuffle(negatives)

	print("Number of positives:", len(positives))
	print("Number of negatives:", len(negatives))

	# Ensures no duplicates across lists
	assert(len(set(positives + negatives)) == len(positives) + len(negatives))

	with open(save_path, 'w') as f:
		json.dump({"positives": positives, "negatives": negatives}, f)

	print("Finished!")


if __name__=='__main__':
	generate_dataset(dataset_path, desired_positive_categories, desired_negative_categories)