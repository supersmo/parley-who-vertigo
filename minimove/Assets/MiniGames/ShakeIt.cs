using UnityEngine;
using System.Collections;

public class ShakeIt : MiniGame {
	private int[] counters;

	public ShakeIt(GameFlow gameFlow) : base(gameFlow) {
		
	}

	public override void StartGame() {
		counters = new int[gameFlow.Players.Count];
		for (int i = 0; i < gameFlow.Players.Count; i++) {
			counters [i] = 0;
		}
	}

	public override string StatusMessage() {
		string result = "";
		for (int i = 0; i < counters.Length; i++) {
			result += "counters[" + i + "] = " + counters [i] + ", ";
		}
		return result;
	}

	public override void Update() {
		TunableVariables tunables = gameFlow.GetTunables ();

		foreach (var player in gameFlow.Players) {
			if (player.NowShaking(tunables)) {
				counters [player.PlayerNumber]++;
			}

			player.LEDColor = Color.green * (float)counters [player.PlayerNumber] / (float)tunables.ShakeItWinThreshold;

			if (counters [player.PlayerNumber] >= tunables.ShakeItWinThreshold) {
				gameFlow.endCurrentGame (player);
			}
		}
	}
}
