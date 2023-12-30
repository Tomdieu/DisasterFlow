from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from accounts.models import Citizen, EmergencyResponder
else:
    Citizen = EmergencyResponder = None


class Visitor:

    def visit_citizen(self, citizen: 'Citizen'):
        pass

    def visit_emergency_responder(self, emergency_responder: 'EmergencyResponder'):
        pass


class NotifyVisitor(Visitor):

    def visit_citizen(self, citizen: 'Citizen'):
        pass

    def visit_emergency_responder(self, emergency_responder: 'EmergencyResponder'):
        pass
