pumping_color = color(0.0, 1.0, 0.0)

function intro()
    player.counter = 0
    sfx(balloon_announce)

    steps = 20 duration = 2
    for intensity=0,1,1/steps do
        led(pumping_color, 1 - intensity)
        wait(duration / steps)
    end

    led(off)
end

function gameplay()
    if player.now_shaking then
        player.counter = player.counter + 1
        intensity = player.counter / tunables.shake_it_win_threshold
        led(pumping_color, intensity)

        if intensity == 1 then
            sfx(balloon_explosion) player:wins()
        elseif player.counter % 7 == 0 then
            sfx(squeak, intensity)
        end
    end
end
