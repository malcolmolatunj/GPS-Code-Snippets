import operator


class User:
    def __init__(self, name):
        self.name = name
        self.roles = set()


class Role:
    def __init__(self, name):
        self.name = name

    def users(self):
        return (user for user in USERS if self.name in user.roles)


ENTITY = {"Contract": 1, "Amendment": 2, "Task_Order": 3}
CONTRACT_TYPE = {
    "PO": 1,
    "FFP": 2,
    "LH": 3,
    "CR": 4,
    "TM": 5,
    "OL": 6,
    "BOC": 7,
    "IQC": 8,
}


class Workflow:
    def __init__(self, name, entity, order):
        self.name = name
        self.criteria = []
        self.active = True
        self.route_to = None
        self.entity = entity
        self.order = order


class Criteria:
    def __init__(self, field, op, value):
        self.field = field
        self.op = op
        self.value = value

    def comparison(self, a, b):
        return self.op(b, a) if self.op == operator.contains else self.op(a, b)


# create dummy users
malcolm = User("malcolm")
parker = User("parker")

USERS = (malcolm, parker)


# create dummy roles
role1 = Role("CI DC A&C")
role2 = Role("CI FACS")
role3 = Role("CI Procurement Manager")
role4 = Role("CI DC A&C Mgr")
role5 = Role("CI ADO")
role6 = Role("CI Country Director")
role7 = Role("KE Country Director")
role8 = Role("KE Procurement Manager")
role9 = Role("KE Finance Manager")
role10 = Role("KE JDC Manager")
role11 = Role("KE FACS")
role12 = Role("KE DC A&C")
role13 = Role("KE Director of Operations")

# assign roles
malcolm.roles.add(role1.name)
parker.roles.add(role2.name)

# create dummy workflows
wf1 = Workflow("CI DC A&C <100K", ENTITY["Contract"], 6000)
wf1.criteria.extend(
    [
        Criteria("value", operator.ge, 50000),
        Criteria("value", operator.lt, 100000),
        Criteria("country", operator.eq, "CDI"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["PO"],
                CONTRACT_TYPE["FFP"],
                CONTRACT_TYPE["CR"],
                CONTRACT_TYPE["LH"],
                CONTRACT_TYPE["OL"],
                CONTRACT_TYPE["TM"],
            ),
        ),
    ]
)
wf1.route_to = role1

wf4 = Workflow("CI DC A&C Mgr <100K", ENTITY["Contract"], 6100)
wf4.criteria.extend(
    [
        Criteria("value", operator.ge, 50000),
        Criteria("value", operator.lt, 100000),
        Criteria("country", operator.eq, "CDI"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["PO"],
                CONTRACT_TYPE["FFP"],
                CONTRACT_TYPE["CR"],
                CONTRACT_TYPE["LH"],
                CONTRACT_TYPE["OL"],
                CONTRACT_TYPE["TM"],
            ),
        ),
    ]
)
wf4.route_to = role4

wf2 = Workflow("CI FACS", ENTITY["Contract"], 4000)
wf2.criteria.extend(
    [
        Criteria("value", operator.ge, 50000),
        Criteria("country", operator.eq, "CDI"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["PO"],
                CONTRACT_TYPE["FFP"],
                CONTRACT_TYPE["CR"],
                CONTRACT_TYPE["LH"],
                CONTRACT_TYPE["OL"],
                CONTRACT_TYPE["TM"],
            ),
        ),
    ]
)
wf2.route_to = role2

wf3 = Workflow("CI P&L Mgr", ENTITY["Contract"], 1000)
wf3.criteria.append(
    Criteria("country", operator.eq, "CDI"),
)
wf3.route_to = role3

wf5 = Workflow("CI ADO", ENTITY["Contract"], 8000)
wf5.criteria.append(
    Criteria("country", operator.eq, "CDI"),
)
wf5.route_to = role5

wf6 = Workflow("CI Country Director", ENTITY["Contract"], 9000)
wf6.criteria.extend(
    [
        Criteria("value", operator.ge, 10000),
        Criteria("country", operator.eq, "CDI"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["PO"],
                CONTRACT_TYPE["FFP"],
                CONTRACT_TYPE["CR"],
                CONTRACT_TYPE["LH"],
                CONTRACT_TYPE["TM"],
            ),
        ),
    ]
)
wf6.route_to = role6

wf7 = Workflow("CI Country Director BOC/IQC/Lease", ENTITY["Contract"], 9000)
wf7.criteria.extend(
    [
        Criteria("country", operator.eq, "CDI"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["IQC"],
                CONTRACT_TYPE["BOC"],
                CONTRACT_TYPE["OL"],
            ),
        ),
    ]
)
wf7.route_to = role6

wf8 = Workflow("CI Country Director", ENTITY["Contract"], 9000)
wf8.criteria.extend(
    [
        Criteria("value", operator.ge, 25000),
        Criteria("country", operator.eq, "Kenya"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["PO"],
                CONTRACT_TYPE["FFP"],
                CONTRACT_TYPE["CR"],
                CONTRACT_TYPE["LH"],
                CONTRACT_TYPE["TM"],
            ),
        ),
    ]
)
wf8.route_to = role7

wf9 = Workflow("KE P&L Mgr", ENTITY["Amendment"], 1000)
wf9.criteria.append(
    Criteria("country", operator.eq, "Kenya"),
)
wf9.route_to = role8

wf10 = Workflow("KE Finance Manager", ENTITY["Amendment"], 2000)
wf10.criteria.extend(
    [
        Criteria("value", operator.ge, 5000),
        Criteria("country", operator.eq, "Kenya"),
        Criteria(
            "type",
            operator.contains,
            (
                CONTRACT_TYPE["PO"],
                CONTRACT_TYPE["FFP"],
                CONTRACT_TYPE["CR"],
                CONTRACT_TYPE["LH"],
                CONTRACT_TYPE["OL"],
                CONTRACT_TYPE["TM"],
            ),
        ),
    ]
)
wf10.route_to = role9

wf11 = Workflow("KE JDC Manager", ENTITY["Amendment"], 3000)
wf11.criteria.extend(
    [
        Criteria("value", operator.ne, 0),
        Criteria("country", operator.eq, "Kenya"),
        Criteria(
            "funding agreement",
            operator.eq,
            "JDC",
        ),
    ]
)
wf11.route_to = role10

WORKFLOWS = (wf1, wf2, wf3, wf4, wf5, wf6, wf7, wf8, wf9, wf10, wf11)


def list_approvers(item):
    applicable_workflows = iter(
        wf for wf in WORKFLOWS if wf.entity == item["entity"] and wf.active
    )
    ordered_workflows = sorted(applicable_workflows, key=lambda x: x.order)

    approvers = []
    for wf in ordered_workflows:
        if all(crit.comparison(item[crit.field], crit.value) for crit in wf.criteria):
            approvers.extend(user.name for user in wf.route_to.users())

    print(approvers)


def list_approval_roles(item):
    applicable_workflows = iter(
        wf for wf in WORKFLOWS if wf.entity == item["entity"] and wf.active
    )
    ordered_workflows = sorted(applicable_workflows, key=lambda x: x.order)

    approvers = [
        wf.route_to.name
        for wf in ordered_workflows
        if all(crit.comparison(item[crit.field], crit.value) for crit in wf.criteria)
    ]

    print(approvers)


contract = {
    "value": 0,
    "country": "Kenya",
    "type": CONTRACT_TYPE["PO"],
    "entity": ENTITY["Amendment"],
    "funding agreement": "JDC",
}

if __name__ == "__main__":
    list_approval_roles(contract)
