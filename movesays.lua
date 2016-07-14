function intro()
    for i=1,10 do
        sfx(cycle_blip) led(random(button_colors)) wait(0.1)
        sfx(cycle_blip) led(off) wait(0.1)
    end

    led(random(button_colors))
end

function gameplay()
    if player.pressed_color == player.color then
        sfx(beep_sound, 0.5) player:wins()
    elseif player.pressed_color then
        led(off) player:dies()
    end
end
