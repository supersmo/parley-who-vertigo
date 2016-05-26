using UnityEngine;
using System.Collections;

public class AttractMode : MiniGame
{
	private static readonly Color ReadyColor = new Color(0.4f, 0.9f, 0.0f);
	private int ticks = 0;
	private float lastUpdate;
	private float accumulator;
	private bool everyoneReady;
	private float gameStartTime;
	private float[] intensities;
	private bool [] readyness;

	public AttractMode(GameFlow gameFlow) : base(gameFlow) {}

	public override void StartGame () {
		ticks = 0;
		lastUpdate = Time.fixedTime;
		accumulator = 0f;
		everyoneReady = false;
		gameStartTime = 0f;
		intensities = new float[gameFlow.Players.Count];
		for (int i = 0; i < intensities.Length; i++) {
			intensities [i] = 0f;
		}
		readyness = new bool[gameFlow.Players.Count];
		for (int i = 0; i < readyness.Length; i++) {
			readyness [i] = false;
		}
	}

	public override string StatusMessage() {
		if (everyoneReady) {
			return "Game Starts in " + (int)SecondsToStart() + " secs";
		} else {
			return "Come and Play! Press MOVE";
		}
	}

	private float SecondsToStart() {
		return (gameStartTime - Time.fixedTime);
	}

	public override void Update () {
		var tunables = gameFlow.GetTunables ();

		for (int i = 0; i < intensities.Length; i++) {
			intensities [i] *= 0.9f;
		}

		// Update timestep
		float now = Time.fixedTime;
		accumulator += (now - lastUpdate);
		lastUpdate = now;
		while (accumulator > tunables.AttractLoopDelaySec && tunables.AttractLoopDelaySec > 0.001f) {
			intensities [(ticks++) % intensities.Length] = 1f;
			accumulator -= tunables.AttractLoopDelaySec;
		}

		if (everyoneReady) {
			// Check if we're ready already
			if (now >= gameStartTime) {
				gameFlow.EveryoneIsReady ();
			} else {
				// Fade out the controllers
				float intensity = 2f * Mathf.Max(0f, (gameStartTime - now) / tunables.AttractStartDelaySec - 0.5f);
				foreach (var player in gameFlow.Players) {
					player.LEDColor = ReadyColor * intensity;
				}
			}

			return;
		}

		// Update controllers and count how many are active
		int numPressed = 0;
		foreach (var player in gameFlow.Players) {
			if (everyoneReady || player.IsMovePressed ()) {
				if (!readyness [player.PlayerNumber]) {
					gameFlow.PlaySound ("ReadySound");
				}
				intensities [player.PlayerNumber] = 1f;
				numPressed++;
				readyness [player.PlayerNumber] = true;
			} else {
				readyness [player.PlayerNumber] = false;
			}

			player.LEDColor = ReadyColor * intensities[player.PlayerNumber];
		}

		if (!everyoneReady && numPressed == gameFlow.Players.Count) {
			gameFlow.PlaySound ("GameWin1Sound");
			everyoneReady = true;
			gameStartTime = Time.fixedTime + tunables.AttractStartDelaySec;
		}
	}

	public override bool CanSupportPlayers(int players) {
		return true;
	}
}