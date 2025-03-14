from django.test import TestCase
from storage.models import ActionType, Action


class ActionTypeModelTests(TestCase):
    def test_create_action_type(self):
        """Test creating an ActionType"""
        action_type = ActionType.objects.create(name="Conference")
        self.assertEqual(action_type.name, "Conference")
        self.assertEqual(str(action_type), "Conference")


class ActionModelTests(TestCase):
    def test_create_action(self):
        """Test creating an Action linked to ActionType"""
        action_type = ActionType.objects.create(name="Seminar")
        action = Action.objects.create(type=action_type, name="Django Workshop")

        self.assertEqual(action.name, "Django Workshop")
        self.assertEqual(action.type, action_type)
        self.assertEqual(str(action), "Seminar: Django Workshop")

    def test_delete_action_type_cascade(self):
        """Test that deleting an ActionType deletes associated Actions"""
        action_type = ActionType.objects.create(name="Project")
        action = Action.objects.create(type=action_type, name="New App Development")

        action_type.delete()

        self.assertFalse(Action.objects.filter(name="New App Development").exists())
