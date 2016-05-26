using UnityEngine;
using System.Collections;

public class TunableVariables : MonoBehaviour {
	// Number of blinks when the winning animation runs
	public int WinAnimationBlinks = 10;
	public float BlinkDurationSec = .1f;
	public Color WinAnimationColor = Color.white;

	// Accelerometer magnitude threshold to detect "shaking"
	public float ShakeThreshold = 3.5f;

	// Accelerometer magnitude for detecting "unstable" (not frozen)
	public float UnstableThreshold = 1.2f;

	// Shake it win threshold
	public int ShakeItWinThreshold = 100;

	// How many mini games a round is
	public int DefaultNumberOfGames = 10;

	// How many color-to-color fades we have
	public int GameWinAnimationFades = 25;

	// How many steps we have between two color fades
	public int GameWinAnimationFadeSteps = 5;

	// How long a single fade step takes
	public float FadeDurationSec = 0.02f;

	// How long to make the controller black before the game win animation
	public float GameWinAnimationWaitBeforeSec = .5f;

	// How long to make the controller black after the game win animation
	public float GameWinAnimationWaitAfterSec = 2f;

	// Disable and enable minigames on the fly
	public bool EnableFreeze = true;
	public bool EnableMoveSays = true;
	public bool EnableSafeCracker = true;
	public bool EnableShakeIt = true;

	// Intensity multiplicator for games where the controller is usually dark
	// (e.g. in SafeCracker, the intensity when users are searching for the code)
	public float ColorIntensityDuringGameplay = 0.2f;
}
