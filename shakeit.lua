pumping_color = color(0.0, 1.0, 0.0)

function intro()
    player.counter = 0
    sfx(balloon_announce)

    for i=1,20 do
        led(pumping_color * (21 - i) / 20)
        wait(0.1)
    end
end

function gameplay()
    if player.now_shaking then
        player.counter = player.counter + 1
        if player.counter == tunables.shake_it_win_threshold then
            sfx(balloon_explosion)
            player:wins()
        elseif player.counter % 7 == 0 then
            sfx(squeak, player.counter / tunables.shake_it_win_threshold)
        end
    end

    base = tunables.color_intensity_during_gameplay
    led(pumping_color * (base + (1 - base) * (player.counter / tunables.shake_it_win_threshold)))
end
