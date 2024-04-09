from ...world.goals.Goal import CylinderGoal

class GoalFactory:
    @staticmethod
    def create(d):
        if d["type"] == "CylinderGoal":
            return CylinderGoal(
                d["center"][0],
                d["center"][1],
                d["r"],
                color=tuple(d["color"]) if "color" in d else None,
                remove_agents_at_goal=d["remove_at"],
                range=d["range"]
            )