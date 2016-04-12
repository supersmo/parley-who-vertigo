﻿using UnityEngine;
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
}
