from minimove import sfx, players, color

FreezingBlue = color(0., 0.4, 0.9)

def intro():
    for i in range(4):
        sfx('CycleBlipSound')
        color(FreezingBlue)
        yield 0.4

        sfx('CycleBlipSound')
        off()
        yield 0.2

    sfx('BeepSound')
    color(FreezingBlue)

def gameplay():
    if alive and is_unstable:
        sfx('BalloonExplosionSound')
        dead()

    color(FreezingBlue if alive else None)

def end():
    return n_alive < 2
