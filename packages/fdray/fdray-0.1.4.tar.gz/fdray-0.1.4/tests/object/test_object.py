from fdray.object import Difference, Intersection, Merge, Sphere, Union


def test_args():
    x = Sphere((0, 0, 0), 1)
    assert x.args == [(0, 0, 0), 1]
    assert x.attrs == []


def test_attrs():
    x = Sphere((0, 0, 0), 1, "a", "b")
    assert x.args == [(0, 0, 0), 1]
    assert x.attrs == ["a", "b"]


def test_object_add_object():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a + b
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_object_sub():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a - b
    assert isinstance(x, Difference)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_object_mul():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a * b
    assert isinstance(x, Intersection)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_object_or():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a | b
    assert isinstance(x, Merge)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_union_add_str():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a + b + "abc"
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] == "abc"


def test_union_add_object():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a + b + c
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_intersection_mul_object():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a * b * c
    assert isinstance(x, Intersection)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_difference_sub_object():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a - b - c
    assert isinstance(x, Difference)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_merge_or_object():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a | b | c
    assert isinstance(x, Merge)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_object_texture():
    from fdray.texture import Texture

    x = Sphere((0, 0, 0), 1).texture("abc")
    t = x.attrs[0]
    assert isinstance(t, Texture)
    assert t.attrs == ["abc"]


def test_object_pigment():
    from fdray.texture import Pigment

    x = Sphere((0, 0, 0), 1).pigment("abc")
    p = x.attrs[0]
    assert isinstance(p, Pigment)
    assert p.attrs == ["abc"]


def test_object_normal():
    from fdray.texture import Normal

    x = Sphere((0, 0, 0), 1).normal("abc")
    n = x.attrs[0]
    assert isinstance(n, Normal)
    assert n.attrs == ["abc"]


def test_object_finish():
    from fdray.texture import Finish

    x = Sphere((0, 0, 0), 1).finish(ambient=1)
    f = x.attrs[0]
    assert isinstance(f, Finish)
    assert f.ambient == 1


def test_csg_transform():
    x = Sphere((0, 0, 0), 1) + Sphere((1, 0, 0), 2)
    x = x.scale(1, 2, 3).rotate(2, 3, 4).translate(3, 4, 5)
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 5
    assert x.attrs[2].scale == (1, 2, 3)
    assert x.attrs[3].rotate == (2, 3, 4)
    assert x.attrs[4].translate == (3, 4, 5)


def test_box():
    from fdray.object import Box

    x = Box((0, 0, 0), (1, 1, 1), "a")
    assert str(x) == "box { <0, 0, 0>, <1, 1, 1> a }"


def test_cone():
    from fdray.object import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2)
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 }"


def test_cone_open_kwarg():
    from fdray.object import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2, open=True)
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 open }"


def test_cone_open_arg():
    from fdray.object import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2, "open")
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 open }"


def test_cylinder():
    from fdray.object import Cylinder

    x = Cylinder((0, 0, 0), (1, 0, 0), 1)
    assert str(x) == "cylinder { <0, 0, 0>, <1, 0, 0>, 1 }"


def test_plane():
    from fdray.object import Plane

    x = Plane((0, 0, 1), 1)
    assert str(x) == "plane { <0, 0, 1>, 1 }"


def test_cuboid():
    from fdray.object import Cuboid

    x = Cuboid((1, 2, 3), (1, 2, 3))
    assert str(x) == "box { <0.5, 1, 1.5>, <1.5, 3, 4.5> }"


def test_cuboid_add_str():
    from fdray.object import Cuboid

    x = Cuboid((1, 2, 3), (1, 2, 3)) + "abc"
    assert str(x) == "box { <0.5, 1, 1.5>, <1.5, 3, 4.5> abc }"


def test_cube():
    from fdray.object import Cube

    x = Cube((1, 2, 3), 1)
    assert str(x) == "box { <0.5, 1.5, 2.5>, <1.5, 2.5, 3.5> }"


def test_cube_add_str():
    from fdray.object import Cube

    x = Cube((1, 2, 3), 1) + "abc"
    assert str(x) == "box { <0.5, 1.5, 2.5>, <1.5, 2.5, 3.5> abc }"
