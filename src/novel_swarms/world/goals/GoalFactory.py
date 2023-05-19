from src.novel_swarms.world.goals.Goal import CylinderGoal

class GoalFactory:
    @staticmethod
    def create(d):
        if d["type"] == "CylinderGoal":
            return CylinderGoal(
                d["center"][0],
                d["center"][1],
                d["r"],
                color=tuple(d["color"]),
                remove_agents_at_goal=d["remove_at"],
                range=d["range"]
            )