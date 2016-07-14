pumping_color = color(0.0, 1.0, 0.0)

function intro()
    sfx(balloon_announce)
    for intensity=1,0,-0.05 do
        led(pumping_color, intensity) wait(0.1)
    end
    led(off) player.counter = 0
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
