freezing_blue = color(0.0, 0.4, 0.9)

function intro()
    for i=1,4 do
        sfx(cycle_blip) led(freezing_blue) wait(0.4)
        sfx(cycle_blip) led(off) wait(0.2)
    end

    sfx(beep) led(freezing_blue)
end

function gameplay()
    if player.alive and player.is_unstable then
        sfx(balloon_explosion) player.alive = false
    end

    led(player.alive and freezing_blue or off)
end
