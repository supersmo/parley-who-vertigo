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

env = {
    -- For debugging
    print=print,
    dump=dump,

    -- Sound effects
    cycle_blip='CycleBlipSound',
    beep='BeepSound',
    ballon_explosion='BalloonExplosionSound',
    player=nil,
}

function env.wait(seconds)
    coroutine.yield(seconds)
end

function env.sfx(sound)
    print('Would play', sound)
end

function env.led(color)
    print('Would set color of', env.player.index, 'to', color.r, color.g, color.b)
end

function env.color(r, g, b)
    return {r=r, g=g, b=b}
end

env.off = env.color(0.0, 0.0, 0.0)

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
    local self = {index=index, alive=true, is_unstable=false}
    return self
end

function gameplay_active()
    alive_players = 0
    for _, player in pairs(players) do
        if player.alive then
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
                env.wait(wait_time)
            end
        until not wait_time
    end
end

function loop_runner(func)
    return function ()
        while gameplay_active() do
            func()
            env.wait(1 / 60)
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

    schedule(parallel_each_runner(env.intro))
    schedule(parallel_each_runner(loop_runner(env.gameplay)))
end

run_minigame(3, 'freeze.lua')
