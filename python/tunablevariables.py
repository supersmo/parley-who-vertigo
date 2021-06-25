#
# Parley Who Vertigo
# Copyright 2016, 2017 Thomas Perl, Josef Who
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#


from color import Color

class TunableVariables(object):
    # Number of blinks when the winning animation runs
    WinAnimationBlinks = 10
    BlinkDurationSec = 0.1
    WinAnimationColor = Color.WHITE

    # Accelerometer magnitude threshold to detect "shaking"
    ShakeThreshold = 3.5

    # Accelerometer magnitude for detecting "unstable" (not frozen)
    UnstableThreshold = 1.2

    # Shake it win threshold
    ShakeItWinThreshold = 100

    # How many mini games a round is
    DefaultNumberOfGames = 10

    # How many color-to-color fades we have
    GameWinAnimationFades = 25

    # How many steps we have between two color fades
    GameWinAnimationFadeSteps = 5

    # How long a single fade step takes
    FadeDurationSec = 0.02

    # How long to make the controller black before the game win animation
    GameWinAnimationWaitBeforeSec = 0.5

    # How long to make the controller black after the game win animation
    GameWinAnimationWaitAfterSec = 2.0

    # Intensity multiplicator for games where the controller is usually dark
    # (e.g. in SafeCracker, the intensity when users are searching for the code)
    ColorIntensityDuringGameplay = 0.2

    # Time (in seconds) that each controller lights up in attract mode
    AttractLoopDelaySec = 0.4

    # Seconds the game start is delayed after everyone is ready
    AttractStartDelaySec = 3.0
