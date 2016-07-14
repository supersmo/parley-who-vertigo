function dump(o)
    if type(o) == 'table' then
        local s = '{ '
        for k,v in pairs(o) do
            if type(k) ~= 'number' then k = '"'..k..'"' end
            s = s .. '['..k..'] = ' .. dump(v) .. ','
        end
        return s .. '} '
    else
        return tostring(o)
    end
end

math.randomseed(os.time())

env = {
    -- For debugging
    print=print,
    dump=dump,

    -- Sound effects
    cycle_blip='CycleBlipSound',
    beep='BeepSound',
    balloon_explosion='BalloonExplosionSound',
    balloon_announce='BalloonAnnounceSound',
    squeak='SqueakSound',

    -- State
    player=nil,
    is_gameplay=false,
}

function wait(seconds)
    coroutine.yield(seconds)
end

function sfx(sound, volume)
    print('Would play', sound, 'at volume', volume or 1.0)
end

function led(color, intensity)
    -- color: the color to set to; intensity: the intensity of the color
    if intensity then
        base = env.is_gameplay and env.tunables.color_intensity_during_gameplay or 0
        color = color * (base + (1 - base) * intensity)
    end

    print('Would set color of', env.player.index, 'to', color.r, color.g, color.b)
    env.player.color = color
end

function random(choices)
    i = 0
    for _, _ in pairs(choices) do
        i = i + 1
    end
    return choices[math.random(i)]
end

color_op = {
    __mul=function (c, f) return color(c.r*f, c.g*f, c.b*f) end,
    __div=function (c, f) return color(c.r/f, c.g/f, c.b/f) end,
    __eq=function (a, b) return a.r == b.r and a.g == b.g and a.b == b.b end,
}

function color(r, g, b)
    local result = {r=r, g=g, b=b}
    setmetatable(result, color_op)
    return result
end

magenta = color(1., 0., 1.)
green = color(0., 1., 0.)
blue = color(0., 0., 1.)
red = color(1., 0., 0.)

env.sfx = sfx
env.led = led
env.random = random
env.color = color
env.wait = wait

env.button_colors = { magenta, green, blue, red }

env.button_to_color = {
    square=magenta,
    triangle=green,
    cross=blue,
    circle=red,
}

env.tunables = {
    win_animation_blinks=10,
    blink_duration_sec=0.1,
    win_animation_color=color(1.0, 1.0, 1.0),
    shake_threshold=3.5,
    unstable_threshold=1.2,
    shake_it_win_threshold=100,
    default_number_of_games=10,
    game_win_animation_fades=25,
    game_win_animation_fade_steps=5,
    fade_duration_sec=0.02,
    game_win_animation_wait_before_sec=0.5,
    game_win_animation_wait_after_sec=2,
    color_intensity_during_gameplay=0.2,
    attract_loop_delay_sec=0.4,
    attract_start_delay_sec=7.0,
}

off = color(0.0, 0.0, 0.0)
env.off = off

function now()
    return os.clock()
end

function schedule(func)
    local busy_wait = function (seconds)
        local started = now()
        repeat until now() - started >= seconds
    end

    co = coroutine.create(func)
    repeat
        running, wait_time = coroutine.resume(co)
        if not running then
            print('Error:', wait_time)
        elseif wait_time then
            busy_wait(wait_time)
        end
    until not (running and wait_time)
end

function Player(index)
    local self = {index=index, color=off, alive=true, is_unstable=true, now_shaking=true, winner=false, pressed_color=nil}
    function self:wins()
        self.winner = true
    end
    function self:dies()
        self.alive = false
    end
    return self
end

function gameplay_active()
    alive_players = 0
    for _, player in pairs(players) do
        if player.winner then
            return false
        elseif player.alive then
            alive_players = alive_players + 1
        end
    end

    return (alive_players > 1)
end

function PlayerCoroutine(player, func)
    local self = {player=player, co=coroutine.create(func), next_run=now(), running=true}
    function self:schedule()
        if self.next_run <= now() then
            env.player = self.player
            running, wait_time = coroutine.resume(self.co)

            if not running then
                print('Error:', wait_time)
            elseif wait_time then
                self.next_run = now() + wait_time
                --print('next run is now:', self.next_run)
            end

            self.running = (running and wait_time)
        end
    end
    return self
end

function parallel_each_runner(func)
    return function ()
        cos = {}
        for i, player in pairs(players) do
            cos[i] = PlayerCoroutine(player, func)
        end

        repeat
            wait_time = nil
            for _, co in pairs(cos) do
                co:schedule()
                if co.running then
                    any_running = true
                    co_wait_time = co.next_run - now()
                    if not wait_time or co_wait_time < wait_time then
                        wait_time = co_wait_time
                    end
                end
            end
            if wait_time then
                wait(wait_time)
            end
        until not wait_time
    end
end

function loop_runner(func)
    return function ()
        while gameplay_active() do
            func()
            wait(1 / 60)
        end
    end
end

function run_minigame(n_players, filename)
    players = {}
    for i=1,n_players do
        players[i] = Player(i)
    end

    constructor = loadfile(filename, 'bt', env)
    constructor()
    print(dump(env))

    env.is_gameplay = false
    schedule(parallel_each_runner(env.intro))
    env.is_gameplay = true
    schedule(parallel_each_runner(loop_runner(env.gameplay)))
end

run_minigame(3, 'freeze.lua')
run_minigame(3, 'shakeit.lua')
run_minigame(3, 'movesays.lua')