# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition
from redis.commands.search.query import Query
from frappe.utils import strip_html_tags
from frappe.utils.redis_wrapper import RedisWrapper
from redis.exceptions import ResponseError

INDEX_NAME = "discussions_index"
PREFIX = 'discussions_search_doc'

def create_index():
	delete_index()
	r = frappe.cache()
	# Options for index creation
	index_def = IndexDefinition(
		prefix = [f"{r.make_key(PREFIX).decode()}:"],
		score = 0.5,
		score_field = "doc_score"
	)
	schema = (
		TextField("title", weight=2.0),
		TextField("content"),
		TextField("modified"),
	)
	# Create an index and pass in the schema
	r.ft(INDEX_NAME).create_index(schema, definition=index_def)
	for d in frappe.db.get_all('Team Project Discussion', fields=['name', 'title', 'content', 'team', 'project', 'owner', 'modified']):
		key = r.make_key(f"{PREFIX}:{d.name}").decode()
		mapping = {
			"title": d.title,
			"content": strip_html_tags(d.content),
			"team": d.team or '',
			"project": d.project or '',
			"owner": d.owner,
			"modified": str(d.modified),
		}
		super(RedisWrapper, r).hset(key, mapping=mapping)

def delete_index():
	try:
		r = frappe.cache()
		r.ft(INDEX_NAME).dropindex(delete_documents=True)
	except ResponseError:
		pass

@frappe.whitelist()
def search(query):
	r = frappe.cache()
	query = Query(query).paging(0, 10).highlight(tags=["<mark>", "</mark>"]).sort_by("modified", asc=False)
	result = r.ft(INDEX_NAME).search(query)
	return {
		"docs": [{'title': d.title, 'content': d.content, 'project': d.project, 'team': d.team, 'modified': d.modified, 'name': d.id.split(PREFIX + ':')[1]} for d in result.docs],
		"total": result.total,
		"duration": result.duration
	}
