from ...world.objects.Wall import Wall


class ObjectFactory:
    @staticmethod
    def create(d):
        if d["type"] == "Wall":
            return Wall(
                None, d["x"], d["y"], d["w"], d["h"],
                angle=d["angle"],
                color=tuple(d["color"])
            )

