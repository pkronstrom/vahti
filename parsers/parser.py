import shelve
from config import save_file

class Parser():

	def _get_list_diff(self, list1, list2):
		"""
			Compares two given lists and returns the difference
		"""
		return (set(list1) - set(list2))

	def compare_to_local(self, query, data):
		"""
			Compares the given data to the database, usign query as a key
		"""

		local_storage = shelve.open(save_file)

		try:
			saved_query_data = local_storage[query]
		except KeyError:
			saved_query_data = []
			local_storage[query] = saved_query_data

		diff = self._get_list_diff(data, saved_query_data)

		if len(diff) > 0:
			local_storage[query] += diff 	# save the diff to stash

			print "[parser.py] DIFF:"
			for item in diff:
				print "[parser.py]" + item
		else:
			print "[parser.py] No new items found"

		local_storage.close()

		return diff
