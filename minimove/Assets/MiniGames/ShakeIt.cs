using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class ShakeIt : MiniGame {
	private static readonly Color PumpingColor = Color.green;
	private int[] counters;
	private int playersReady = 0;

	public ShakeIt(GameFlow gameFlow) : base(gameFlow) {
		
	}

	public override void StartGame() {
		OnFinished onIntroBlinkingFinished = delegate() {
			playersReady++;

			if (playersReady == gameFlow.Players.Count) {
				counters = new int[gameFlow.Players.Count];
				for (int i = 0; i < gameFlow.Players.Count; i++) {
					counters [i] = 0;
				}
			}
		};

		gameFlow.PlaySound ("BalloonAnnounceSound");

		foreach (var player in gameFlow.Players) {
			List<AnimationPart> parts = new List<AnimationPart> ();
			int iterations = 20;
			for (int i=0; i<iterations; i++) {
				parts.Add(new AnimationPart(PumpingColor * (float)(iterations - 1 - i)/(float)iterations, 0.1f));
			}
			gameFlow.StartCoroutine(player.SphereColorAnimation (parts, onIntroBlinkingFinished));
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
		if (playersReady < gameFlow.Players.Count) {
			return;
		}

		TunableVariables tunables = gameFlow.GetTunables ();

		foreach (var player in gameFlow.Players) {
			if (player.NowShaking(tunables)) {
				counters [player.PlayerNumber]++;
				int currentValue = counters [player.PlayerNumber];
				int mod = 7;
				if (currentValue == tunables.ShakeItWinThreshold) {
					gameFlow.PlaySound ("BalloonExplosionSound");
					player.Rumble = 1f;
				} else if (currentValue % mod == 0) {
					int mode = (currentValue / mod) % 2;
					//gameFlow.PlaySound ("InflateSound", 3f * (float)currentValue / 100f);
					gameFlow.PlaySound ("SqueakSound", 3f * (float)currentValue / 100f,
						(mode == 0) ? 1f : 1.5f);
				}
			} 

			player.LEDColor = PumpingColor * (float)counters [player.PlayerNumber] / (float)tunables.ShakeItWinThreshold;

			if (counters [player.PlayerNumber] >= tunables.ShakeItWinThreshold) {
				gameFlow.endCurrentGame (player);
			}
		}
	}

	public override bool CanSupportPlayers(int players) {
		return true;
	}
}
