import Bomb_Sim
def test_first():
    assert 1 == 1

def test_second():
    s=Bomb_Sim.Body(mass=1, position=[1, 2, 3], velocity=[4, 5, 6], angle = 7, drag=(8, 9, 10), target=(11,12))
    assert s.mass == 1
    assert s.position == [1, 2, 3]
    assert s.velocity == [4, 5, 6]
    assert s.angle == 7
    assert s.drag == (8, 9, 10)
    assert s.target == (11,12)
    
