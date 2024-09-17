# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class LoanNPALog(Document):
	pass


def delink_npa_logs(loan, posting_date):
	if not posting_date:
		posting_date = getdate()

	loan_logs = frappe.db.get_all(
		"Loan NPA Log",
		{
			"loan": loan,
			"npa_date": (">=", posting_date),
		},
		pluck="name",
	)

	loan_log = frappe.qb.DocType("Loan NPA Log")

	if loan_logs:
		frappe.qb.update(loan_log).set("delinked", 1).where(loan_log.name.isin(loan_logs)).run()
