# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import json
from typing import Dict, Optional

import dontmanage
from dontmanage import _
from dontmanage.query_builder.functions import CombineDatetime
from dontmanage.utils import cstr, flt, get_link_to_form, nowdate, nowtime

import dontmanageerp
from dontmanageerp.stock.valuation import FIFOValuation, LIFOValuation

BarcodeScanResult = Dict[str, Optional[str]]


class InvalidWarehouseCompany(dontmanage.ValidationError):
	pass


class PendingRepostingError(dontmanage.ValidationError):
	pass


def get_stock_value_from_bin(warehouse=None, item_code=None):
	values = {}
	conditions = ""
	if warehouse:
		conditions += """ and `tabBin`.warehouse in (
						select w2.name from `tabWarehouse` w1
						join `tabWarehouse` w2 on
						w1.name = %(warehouse)s
						and w2.lft between w1.lft and w1.rgt
						) """

		values["warehouse"] = warehouse

	if item_code:
		conditions += " and `tabBin`.item_code = %(item_code)s"

		values["item_code"] = item_code

	query = (
		"""select sum(stock_value) from `tabBin`, `tabItem` where 1 = 1
		and `tabItem`.name = `tabBin`.item_code and ifnull(`tabItem`.disabled, 0) = 0 %s"""
		% conditions
	)

	stock_value = dontmanage.db.sql(query, values)

	return stock_value


def get_stock_value_on(warehouse=None, posting_date=None, item_code=None):
	if not posting_date:
		posting_date = nowdate()

	values, condition = [posting_date], ""

	if warehouse:

		lft, rgt, is_group = dontmanage.db.get_value("Warehouse", warehouse, ["lft", "rgt", "is_group"])

		if is_group:
			values.extend([lft, rgt])
			condition += "and exists (\
				select name from `tabWarehouse` wh where wh.name = sle.warehouse\
				and wh.lft >= %s and wh.rgt <= %s)"

		else:
			values.append(warehouse)
			condition += " AND warehouse = %s"

	if item_code:
		values.append(item_code)
		condition += " AND item_code = %s"

	stock_ledger_entries = dontmanage.db.sql(
		"""
		SELECT item_code, stock_value, name, warehouse
		FROM `tabStock Ledger Entry` sle
		WHERE posting_date <= %s {0}
			and is_cancelled = 0
		ORDER BY timestamp(posting_date, posting_time) DESC, creation DESC
	""".format(
			condition
		),
		values,
		as_dict=1,
	)

	sle_map = {}
	for sle in stock_ledger_entries:
		if not (sle.item_code, sle.warehouse) in sle_map:
			sle_map[(sle.item_code, sle.warehouse)] = flt(sle.stock_value)

	return sum(sle_map.values())


@dontmanage.whitelist()
def get_stock_balance(
	item_code,
	warehouse,
	posting_date=None,
	posting_time=None,
	with_valuation_rate=False,
	with_serial_no=False,
):
	"""Returns stock balance quantity at given warehouse on given posting date or current date.

	If `with_valuation_rate` is True, will return tuple (qty, rate)"""

	from dontmanageerp.stock.stock_ledger import get_previous_sle

	if posting_date is None:
		posting_date = nowdate()
	if posting_time is None:
		posting_time = nowtime()

	args = {
		"item_code": item_code,
		"warehouse": warehouse,
		"posting_date": posting_date,
		"posting_time": posting_time,
	}

	last_entry = get_previous_sle(args)

	if with_valuation_rate:
		if with_serial_no:
			serial_nos = get_serial_nos_data_after_transactions(args)

			return (
				(last_entry.qty_after_transaction, last_entry.valuation_rate, serial_nos)
				if last_entry
				else (0.0, 0.0, None)
			)
		else:
			return (
				(last_entry.qty_after_transaction, last_entry.valuation_rate) if last_entry else (0.0, 0.0)
			)
	else:
		return last_entry.qty_after_transaction if last_entry else 0.0


def get_serial_nos_data_after_transactions(args):

	serial_nos = set()
	args = dontmanage._dict(args)
	sle = dontmanage.qb.DocType("Stock Ledger Entry")

	stock_ledger_entries = (
		dontmanage.qb.from_(sle)
		.select("serial_no", "actual_qty")
		.where(
			(sle.item_code == args.item_code)
			& (sle.warehouse == args.warehouse)
			& (
				CombineDatetime(sle.posting_date, sle.posting_time)
				< CombineDatetime(args.posting_date, args.posting_time)
			)
			& (sle.is_cancelled == 0)
		)
		.orderby(sle.posting_date, sle.posting_time, sle.creation)
		.run(as_dict=1)
	)

	for stock_ledger_entry in stock_ledger_entries:
		changed_serial_no = get_serial_nos_data(stock_ledger_entry.serial_no)
		if stock_ledger_entry.actual_qty > 0:
			serial_nos.update(changed_serial_no)
		else:
			serial_nos.difference_update(changed_serial_no)

	return "\n".join(serial_nos)


def get_serial_nos_data(serial_nos):
	from dontmanageerp.stock.doctype.serial_no.serial_no import get_serial_nos

	return get_serial_nos(serial_nos)


@dontmanage.whitelist()
def get_latest_stock_qty(item_code, warehouse=None):
	values, condition = [item_code], ""
	if warehouse:
		lft, rgt, is_group = dontmanage.db.get_value("Warehouse", warehouse, ["lft", "rgt", "is_group"])

		if is_group:
			values.extend([lft, rgt])
			condition += "and exists (\
				select name from `tabWarehouse` wh where wh.name = tabBin.warehouse\
				and wh.lft >= %s and wh.rgt <= %s)"

		else:
			values.append(warehouse)
			condition += " AND warehouse = %s"

	actual_qty = dontmanage.db.sql(
		"""select sum(actual_qty) from tabBin
		where item_code=%s {0}""".format(
			condition
		),
		values,
	)[0][0]

	return actual_qty


def get_latest_stock_balance():
	bin_map = {}
	for d in dontmanage.db.sql(
		"""SELECT item_code, warehouse, stock_value as stock_value
		FROM tabBin""",
		as_dict=1,
	):
		bin_map.setdefault(d.warehouse, {}).setdefault(d.item_code, flt(d.stock_value))

	return bin_map


def get_bin(item_code, warehouse):
	bin = dontmanage.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse})
	if not bin:
		bin_obj = _create_bin(item_code, warehouse)
	else:
		bin_obj = dontmanage.get_doc("Bin", bin, for_update=True)
	bin_obj.flags.ignore_permissions = True
	return bin_obj


def get_or_make_bin(item_code: str, warehouse: str) -> str:
	bin_record = dontmanage.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse})

	if not bin_record:
		bin_obj = _create_bin(item_code, warehouse)
		bin_record = bin_obj.name
	return bin_record


def _create_bin(item_code, warehouse):
	"""Create a bin and take care of concurrent inserts."""

	bin_creation_savepoint = "create_bin"
	try:
		dontmanage.db.savepoint(bin_creation_savepoint)
		bin_obj = dontmanage.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		bin_obj.flags.ignore_permissions = 1
		bin_obj.insert()
	except dontmanage.UniqueValidationError:
		dontmanage.db.rollback(save_point=bin_creation_savepoint)  # preserve transaction in postgres
		bin_obj = dontmanage.get_last_doc("Bin", {"item_code": item_code, "warehouse": warehouse})

	return bin_obj


@dontmanage.whitelist()
def get_incoming_rate(args, raise_error_if_no_rate=True):
	"""Get Incoming Rate based on valuation method"""
	from dontmanageerp.stock.stock_ledger import (
		get_batch_incoming_rate,
		get_previous_sle,
		get_valuation_rate,
	)

	if isinstance(args, str):
		args = json.loads(args)

	voucher_no = args.get("voucher_no") or args.get("name")

	in_rate = None
	if (args.get("serial_no") or "").strip():
		in_rate = get_avg_purchase_rate(args.get("serial_no"))
	elif args.get("batch_no") and dontmanage.db.get_value(
		"Batch", args.get("batch_no"), "use_batchwise_valuation", cache=True
	):
		in_rate = get_batch_incoming_rate(
			item_code=args.get("item_code"),
			warehouse=args.get("warehouse"),
			batch_no=args.get("batch_no"),
			posting_date=args.get("posting_date"),
			posting_time=args.get("posting_time"),
		)
	else:
		valuation_method = get_valuation_method(args.get("item_code"))
		previous_sle = get_previous_sle(args)
		if valuation_method in ("FIFO", "LIFO"):
			if previous_sle:
				previous_stock_queue = json.loads(previous_sle.get("stock_queue", "[]") or "[]")
				in_rate = (
					_get_fifo_lifo_rate(previous_stock_queue, args.get("qty") or 0, valuation_method)
					if previous_stock_queue
					else 0
				)
		elif valuation_method == "Moving Average":
			in_rate = previous_sle.get("valuation_rate") or 0

	if in_rate is None:
		in_rate = get_valuation_rate(
			args.get("item_code"),
			args.get("warehouse"),
			args.get("voucher_type"),
			voucher_no,
			args.get("allow_zero_valuation"),
			currency=dontmanageerp.get_company_currency(args.get("company")),
			company=args.get("company"),
			raise_error_if_no_rate=raise_error_if_no_rate,
			batch_no=args.get("batch_no"),
		)

	return flt(in_rate)


def get_avg_purchase_rate(serial_nos):
	"""get average value of serial numbers"""

	serial_nos = get_valid_serial_nos(serial_nos)
	return flt(
		dontmanage.db.sql(
			"""select avg(purchase_rate) from `tabSerial No`
		where name in (%s)"""
			% ", ".join(["%s"] * len(serial_nos)),
			tuple(serial_nos),
		)[0][0]
	)


def get_valuation_method(item_code):
	"""get valuation method from item or default"""
	val_method = dontmanage.db.get_value("Item", item_code, "valuation_method", cache=True)
	if not val_method:
		val_method = (
			dontmanage.db.get_value("Stock Settings", None, "valuation_method", cache=True) or "FIFO"
		)
	return val_method


def get_fifo_rate(previous_stock_queue, qty):
	"""get FIFO (average) Rate from Queue"""
	return _get_fifo_lifo_rate(previous_stock_queue, qty, "FIFO")


def get_lifo_rate(previous_stock_queue, qty):
	"""get LIFO (average) Rate from Queue"""
	return _get_fifo_lifo_rate(previous_stock_queue, qty, "LIFO")


def _get_fifo_lifo_rate(previous_stock_queue, qty, method):
	ValuationKlass = LIFOValuation if method == "LIFO" else FIFOValuation

	stock_queue = ValuationKlass(previous_stock_queue)
	if flt(qty) >= 0:
		total_qty, total_value = stock_queue.get_total_stock_and_value()
		return total_value / total_qty if total_qty else 0.0
	else:
		popped_bins = stock_queue.remove_stock(abs(flt(qty)))

		total_qty, total_value = ValuationKlass(popped_bins).get_total_stock_and_value()
		return total_value / total_qty if total_qty else 0.0


def get_valid_serial_nos(sr_nos, qty=0, item_code=""):
	"""split serial nos, validate and return list of valid serial nos"""
	# TODO: remove duplicates in client side
	serial_nos = cstr(sr_nos).strip().replace(",", "\n").split("\n")

	valid_serial_nos = []
	for val in serial_nos:
		if val:
			val = val.strip()
			if val in valid_serial_nos:
				dontmanage.throw(_("Serial number {0} entered more than once").format(val))
			else:
				valid_serial_nos.append(val)

	if qty and len(valid_serial_nos) != abs(qty):
		dontmanage.throw(_("{0} valid serial nos for Item {1}").format(abs(qty), item_code))

	return valid_serial_nos


def validate_warehouse_company(warehouse, company):
	warehouse_company = dontmanage.db.get_value("Warehouse", warehouse, "company", cache=True)
	if warehouse_company and warehouse_company != company:
		dontmanage.throw(
			_("Warehouse {0} does not belong to company {1}").format(warehouse, company),
			InvalidWarehouseCompany,
		)


def is_group_warehouse(warehouse):
	if dontmanage.db.get_value("Warehouse", warehouse, "is_group", cache=True):
		dontmanage.throw(_("Group node warehouse is not allowed to select for transactions"))


def validate_disabled_warehouse(warehouse):
	if dontmanage.db.get_value("Warehouse", warehouse, "disabled", cache=True):
		dontmanage.throw(
			_("Disabled Warehouse {0} cannot be used for this transaction.").format(
				get_link_to_form("Warehouse", warehouse)
			)
		)


def update_included_uom_in_report(columns, result, include_uom, conversion_factors):
	if not include_uom or not conversion_factors:
		return

	convertible_cols = {}
	is_dict_obj = False
	if isinstance(result[0], dict):
		is_dict_obj = True

	convertible_columns = {}
	for idx, d in enumerate(columns):
		key = d.get("fieldname") if is_dict_obj else idx
		if d.get("convertible"):
			convertible_columns.setdefault(key, d.get("convertible"))

			# Add new column to show qty/rate as per the selected UOM
			columns.insert(
				idx + 1,
				{
					"label": "{0} (per {1})".format(d.get("label"), include_uom),
					"fieldname": "{0}_{1}".format(d.get("fieldname"), dontmanage.scrub(include_uom)),
					"fieldtype": "Currency" if d.get("convertible") == "rate" else "Float",
				},
			)

	update_dict_values = []
	for row_idx, row in enumerate(result):
		data = row.items() if is_dict_obj else enumerate(row)
		for key, value in data:
			if key not in convertible_columns:
				continue
			# If no conversion factor for the UOM, defaults to 1
			if not conversion_factors[row_idx]:
				conversion_factors[row_idx] = 1

			if convertible_columns.get(key) == "rate":
				new_value = flt(value) * conversion_factors[row_idx]
			else:
				new_value = flt(value) / conversion_factors[row_idx]

			if not is_dict_obj:
				row.insert(key + 1, new_value)
			else:
				new_key = "{0}_{1}".format(key, dontmanage.scrub(include_uom))
				update_dict_values.append([row, new_key, new_value])

	for data in update_dict_values:
		row, key, value = data
		row[key] = value


def get_available_serial_nos(args):
	return dontmanage.db.sql(
		""" SELECT name from `tabSerial No`
		WHERE item_code = %(item_code)s and warehouse = %(warehouse)s
		 and timestamp(purchase_date, purchase_time) <= timestamp(%(posting_date)s, %(posting_time)s)
	""",
		args,
		as_dict=1,
	)


def add_additional_uom_columns(columns, result, include_uom, conversion_factors):
	if not include_uom or not conversion_factors:
		return

	convertible_column_map = {}
	for col_idx in list(reversed(range(0, len(columns)))):
		col = columns[col_idx]
		if isinstance(col, dict) and col.get("convertible") in ["rate", "qty"]:
			next_col = col_idx + 1
			columns.insert(next_col, col.copy())
			columns[next_col]["fieldname"] += "_alt"
			convertible_column_map[col.get("fieldname")] = dontmanage._dict(
				{"converted_col": columns[next_col]["fieldname"], "for_type": col.get("convertible")}
			)
			if col.get("convertible") == "rate":
				columns[next_col]["label"] += " (per {})".format(include_uom)
			else:
				columns[next_col]["label"] += " ({})".format(include_uom)

	for row_idx, row in enumerate(result):
		for convertible_col, data in convertible_column_map.items():
			conversion_factor = conversion_factors[row.get("item_code")] or 1
			for_type = data.for_type
			value_before_conversion = row.get(convertible_col)
			if for_type == "rate":
				row[data.converted_col] = flt(value_before_conversion) * conversion_factor
			else:
				row[data.converted_col] = flt(value_before_conversion) / conversion_factor

		result[row_idx] = row


def get_incoming_outgoing_rate_for_cancel(item_code, voucher_type, voucher_no, voucher_detail_no):
	outgoing_rate = dontmanage.db.sql(
		"""SELECT CASE WHEN actual_qty = 0 THEN 0 ELSE abs(stock_value_difference / actual_qty) END
		FROM `tabStock Ledger Entry`
		WHERE voucher_type = %s and voucher_no = %s
			and item_code = %s and voucher_detail_no = %s
			ORDER BY CREATION DESC limit 1""",
		(voucher_type, voucher_no, item_code, voucher_detail_no),
	)

	outgoing_rate = outgoing_rate[0][0] if outgoing_rate else 0.0

	return outgoing_rate


def is_reposting_item_valuation_in_progress():
	reposting_in_progress = dontmanage.db.exists(
		"Repost Item Valuation", {"docstatus": 1, "status": ["in", ["Queued", "In Progress"]]}
	)
	if reposting_in_progress:
		dontmanage.msgprint(
			_("Item valuation reposting in progress. Report might show incorrect item valuation."), alert=1
		)


def check_pending_reposting(posting_date: str, throw_error: bool = True) -> bool:
	"""Check if there are pending reposting job till the specified posting date."""

	filters = {
		"docstatus": 1,
		"status": ["in", ["Queued", "In Progress"]],
		"posting_date": ["<=", posting_date],
	}

	reposting_pending = dontmanage.db.exists("Repost Item Valuation", filters)
	if reposting_pending and throw_error:
		msg = _(
			"Stock/Accounts can not be frozen as processing of backdated entries is going on. Please try again later."
		)
		dontmanage.msgprint(
			msg,
			raise_exception=PendingRepostingError,
			title="Stock Reposting Ongoing",
			indicator="red",
			primary_action={
				"label": _("Show pending entries"),
				"client_action": "dontmanageerp.route_to_pending_reposts",
				"args": filters,
			},
		)

	return bool(reposting_pending)


@dontmanage.whitelist()
def scan_barcode(search_value: str) -> BarcodeScanResult:
	def set_cache(data: BarcodeScanResult):
		dontmanage.cache().set_value(f"dontmanageerp:barcode_scan:{search_value}", data, expires_in_sec=120)

	def get_cache() -> Optional[BarcodeScanResult]:
		if data := dontmanage.cache().get_value(f"dontmanageerp:barcode_scan:{search_value}"):
			return data

	if scan_data := get_cache():
		return scan_data

	# search barcode no
	barcode_data = dontmanage.db.get_value(
		"Item Barcode",
		{"barcode": search_value},
		["barcode", "parent as item_code", "uom"],
		as_dict=True,
	)
	if barcode_data:
		_update_item_info(barcode_data)
		set_cache(barcode_data)
		return barcode_data

	# search serial no
	serial_no_data = dontmanage.db.get_value(
		"Serial No",
		search_value,
		["name as serial_no", "item_code", "batch_no"],
		as_dict=True,
	)
	if serial_no_data:
		_update_item_info(serial_no_data)
		set_cache(serial_no_data)
		return serial_no_data

	# search batch no
	batch_no_data = dontmanage.db.get_value(
		"Batch",
		search_value,
		["name as batch_no", "item as item_code"],
		as_dict=True,
	)
	if batch_no_data:
		_update_item_info(batch_no_data)
		set_cache(batch_no_data)
		return batch_no_data

	return {}


def _update_item_info(scan_result: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
	if item_code := scan_result.get("item_code"):
		if item_info := dontmanage.get_cached_value(
			"Item",
			item_code,
			["has_batch_no", "has_serial_no"],
			as_dict=True,
		):
			scan_result.update(item_info)
	return scan_result
