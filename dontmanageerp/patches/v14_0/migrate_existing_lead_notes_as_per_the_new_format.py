import dontmanage
from dontmanage.utils import cstr, strip_html


def execute():
	for doctype in ("Lead", "Prospect", "Opportunity"):
		if not dontmanage.db.has_column(doctype, "notes"):
			continue

		dt = dontmanage.qb.DocType(doctype)
		records = (
			dontmanage.qb.from_(dt)
			.select(dt.name, dt.notes, dt.modified_by, dt.modified)
			.where(dt.notes.isnotnull() & dt.notes != "")
		).run(as_dict=True)

		for d in records:
			if strip_html(cstr(d.notes)).strip():
				doc = dontmanage.get_doc(doctype, d.name)
				doc.append("notes", {"note": d.notes, "added_by": d.modified_by, "added_on": d.modified})
				doc.update_child_table("notes")

		dontmanage.db.sql_ddl(f"alter table `tab{doctype}` drop column `notes`")
