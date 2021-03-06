# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.utils import (flt, cstr)
from frappe.model.document import Document

class BSCPerspective(Document):

	def validate(self):
		self.validate_percentage()

	def validate_percentage(self):
		if flt(self.perspective_percentage) <= 0.0 :
			frappe.throw(_("The percentage % must to be > {0}").format(frappe.bold("0.0")))

		if not frappe.db.exists(self.doctype, self.name):
			sum_percentage = frappe.db.sql("""select sum(perspective_percentage) from `tabBSC Perspective`""")[0][0]
			if sum_percentage == 100:
				frappe.throw(_("You can't add this perspective, the total percentage % of others is 100%"))
		else :
			sum_percentage = frappe.db.sql("""select sum(perspective_percentage) from `tabBSC Perspective` where name <> %s""",self.name)[0][0]

		if (flt(flt(sum_percentage) + self.perspective_percentage)) > 100.0 :
			frappe.throw(_("The percentage % must to be < {0}, total of others is {1}").format(frappe.bold(str(100 - flt(sum_percentage))), \
				frappe.bold(str(flt(sum_percentage))) ))