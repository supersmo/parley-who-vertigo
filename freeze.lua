FreezingBlue = color(0.0, 0.4, 0.9)
Off = color(0.0, 0.0, 0.0)

function intro()
    for i=1,4 do
        sfx('CycleBlipSound')
        led(FreezingBlue)
        wait(0.4)

        sfx('CycleBlipSound')
        led(Off)
        wait(0.2)
    end

    sfx('BeepSound')
    color(FreezingBlue)
end

function gameplay()
    if alive and is_unstable then
        sfx('BalloonExplosionSound')
        alive = false
    end

    color(alive and FreezingBlue or Off)
end
