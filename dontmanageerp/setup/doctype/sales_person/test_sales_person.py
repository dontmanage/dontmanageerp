# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

test_dependencies = ["Employee"]

import dontmanage

test_records = dontmanage.get_test_records("Sales Person")

test_ignore = ["Item Group"]
