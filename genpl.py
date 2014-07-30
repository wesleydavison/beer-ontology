import xmltodict
import json

from keyword_mapping import global_map

global_styles = []
global_groups = []
global_beers = []
global_attributes = {}

goals_attributes = {}

def simplify(string):
	return string.lstrip(" ").rstrip(" ").lstrip("-").rstrip("-").replace(" ", "_").replace("(", "").replace(")", "").replace("\"", "").replace("+", "").lower()

def handle_root(node):
	for k, v in node.iteritems():
		handle_style(simplify(k), v)

def handle_style(style, node):
	print_style(style)

	for k, v in node.iteritems():
		handle_group(style, simplify(k), v)

def print_style(style):
	global_styles.append("""
style(%s) :-
	true.""" % (style))

def handle_group(parent, name, node):
	if name != 'nogroup':
		print_group(parent, name)

		for k, v in node.iteritems():
			if v != None:
				if k != 'Samples':
					handle_group_attribute(name, simplify(k), v)
				else:
					for k1, v1 in v.iteritems():
						handle_sample(name, simplify(k1), v1)

	else:
		for k, v in node.iteritems():
			handle_sample(parent, simplify(k), v)

def print_group(style, group):
	global_groups.append("""
group(%(group)s) :-
	style(%(style)s),
	color(%(group)s),
	head(%(group)s),
	malt(%(group)s),
	hops(%(group)s),
	yeast(%(group)s),
	consistency(%(group)s),
	carbonation(%(group)s),
	body(%(group)s),
	finish(%(group)s).""" % {'group': group, 'style': style})

def handle_sample(group, beer, node):
	print_beer(group, beer)

	for k, v in node.iteritems():
		if k != 'Popular_Examples':
			print_attribute(beer, simplify(k), v)

def print_beer(group, beer):
	global_beers.append("""
beer(%(beer)s) :-
	group(%(group)s),
	taste_smell(%(beer)s),
	alcohol_by_volume_abv_range(%(beer)s),
	bitterness_ibu(%(beer)s),
	serving_temperature(%(beer)s),
	glassware(%(beer)s),
	cheese_pairing_ideas(%(beer)s),
	food_pairing_ideas(%(beer)s).""" % {'group': group, 'beer': beer})

def handle_group_attribute(group, _, node):
	for k, v in node.iteritems():
		print_attribute(group, simplify(k), v)

def find_keywords(attribute, text):
	replaced_split = text.replace(" and ", ";").replace(" or ", ";").replace(" to ", ";").replace(",", ";").replace(".", ";").replace(" - ", ";").replace("- ", ";").replace(" -", ";").split(";")

	return [x for x in [remap_keyword(attribute, simplify(keyword)) for keyword in replaced_split] if x != None] 

def remap_keyword(attribute, text):
	if text != "" and global_map[attribute].has_key(text):
		return global_map[attribute][text]
	else:
		return None

def print_attribute(group, attribute, value):
	keywords = find_keywords(attribute, value)

	save_attribute_goal(attribute, keywords)

	result = "\n%(attr)s(%(group)s) :-" % {'group': group, 'attr': attribute}
	result += ";".join(["\n\t%(attr)s(%(value)s)" % {'group': group, 'attr': attribute, 'value': v} for v in keywords if v != None]) + "."

	save_attribute(attribute, result)

def save_attribute(attribute, value):
	if not global_attributes.has_key(attribute):
		global_attributes[attribute] = []

	global_attributes[attribute].append(value)

def save_attribute_goal(attribute, values):
	if not goals_attributes.has_key(attribute):
		goals_attributes[attribute] = []

	goals_attributes[attribute] = list(set(goals_attributes[attribute] + values))

def main():
	data = None

	with open ("ontology-tavl.xml", "r") as myfile:
		data = myfile.read()

	print """
top_goal(X) :- beer(X)."""

	handle_root(xmltodict.parse(data)['beer'])

	for i in global_styles:
		print i
		break

	for i in global_groups:
		print i
		break

	for i in global_beers:
		print i
		break

	for k, v in global_attributes.iteritems():
		for i in v:
			print i
			break

	print ""

	options = {}

	menu = True

	for k, v in goals_attributes.iteritems():
		if menu:
			print "%(attr)s(X) :- menuask(%(attr)s, X, [%(options)s]).\n" % {'attr': k, 'options': ", ".join(v)}
		else:
			print "%(attr)s(X) :- ask(%(attr)s, X).\n" % {'attr': k}

		options[k] = dict([(i, i) for i in v])

	# print json.dumps(options, sort_keys = True, indent = 4, separators=(',', ': '))

if __name__ == "__main__":
	main()
