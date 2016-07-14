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
    cycle_blip='CycleBlipSound',
    beep='BeepSound',
    ballon_explosion='BalloonExplosionSound',
}

function env.wait(wait_seconds)
    if wait_seconds then
        coroutine.yield(wait_seconds)
    end
end

function env.sfx(sound)
    print('Would play', sound)
end

function env.led(color)
    print('Would set color to', color.r, color.g, color.b)
end

function env.load_from(player)
    env.alive = player.alive
    env.is_unstable = player.is_unstable
end

function env.save_to(player)
    player.alive = env.alive
end

function env.color(r, g, b)
    return {r=r, g=g, b=b}
end

env.off = env.color(0.0, 0.0, 0.0)

constructor = loadfile('freeze.lua', 'bt', env)
constructor()
print(dump(env))

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
    return {index=index, alive=true, is_unstable=false}
end

players = {}
for i=1,2 do
    players[i] = Player(i)
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

function loop_runner(func)
    return function ()
        while gameplay_active() do
            for _, player in pairs(players) do
                current_player = player
                env.load_from(current_player)
                func()
                env.save_to(current_player)
            end
            env.wait(1 / 60)
        end
    end
end

function PlayerCoroutine(player, func)
    local self = {player=player, co=coroutine.create(func), next_run=now(), running=true}
    function self:schedule()
        if self.next_run <= now() then
            running, wait_time = coroutine.resume(self.co)
            if not running then
                print('Error:', wait_time)
            elseif wait_time then
                self.next_run = now() + wait_time
                print('next run is now:', self.next_run)
            end

            self.running = (running and wait_time)
        end
    end
    return self
end

function once_runner(func)
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
            env.wait(wait_time)
        until not wait_time
    end
end

schedule(once_runner(env.intro))
schedule(loop_runner(env.gameplay))
