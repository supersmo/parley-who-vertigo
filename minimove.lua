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

env = {}

function env.wait(seconds)
    coroutine.yield(seconds)
end

function env.sfx(sound)
    print('Would play', sound)
end

function env.led(color)
    print('Would set color to', color.r, color.g, color.b)
end

function env.color(r, g, b)
    return {r=r, g=g, b=b}
end

constructor = loadfile('freeze.lua', 'bt', env)
constructor()
print(dump(env))

function busy_wait(seconds)
    local started = os.clock()
    repeat until os.clock() - started >= seconds
end

co = coroutine.create(env.intro)
print(co)
repeat
    running, wait_time = coroutine.resume(co)
    if running and wait_time then
        busy_wait(wait_time)
    end
until not running
