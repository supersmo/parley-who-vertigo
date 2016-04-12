using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Freeze : MiniGame {
	private static readonly Color FreezingBlue = new Color (0f, 0.4f, 0.9f);
	private bool[] alive;
	private int alivePlayers;
	private int playersReady = 0;

	public Freeze(GameFlow gameFlow) : base(gameFlow) {}

	public override string StatusMessage() {
		return "Freeze!";
	}

	public override void StartGame () {
		OnFinished onIntroBlinkingFinished = delegate() {
			gameFlow.PlaySound("BeepSound");

			playersReady++;

			if (playersReady == gameFlow.Players.Count) {
				alive = new bool[gameFlow.Players.Count];

				foreach (var player in gameFlow.Players) {
					alive [player.PlayerNumber] = true;
					player.LEDColor = FreezingBlue;
				}

				alivePlayers = gameFlow.Players.Count;
			}
		};

		foreach (var player in gameFlow.Players) {
			List<AnimationPart> parts = new List<AnimationPart> ();
			for (int i=0; i<4; i++) {
				parts.Add(new AnimationPart(FreezingBlue, 0.4f));
				parts.Add(new AnimationPart(Color.black, 0.2f));
			}
			OnFinished onChanged = delegate() {
				gameFlow.PlaySound("CycleBlipSound");
			};
			gameFlow.StartCoroutine(player.SphereColorAnimation (parts, onIntroBlinkingFinished, onChanged));
		}
	}

	public override void Update () {
		foreach (var player in gameFlow.Players) {
			if (alive [player.PlayerNumber] && player.IsUnstable (gameFlow.GetTunables ())) {
				alive [player.PlayerNumber] = false;
				alivePlayers--;
				player.LEDColor = Color.black;
				gameFlow.PlaySound ("BalloonExplosionSound");

				if (alivePlayers == 1) {
					foreach (var winner in gameFlow.Players) {
						if (alive[winner.PlayerNumber]) {
							gameFlow.endCurrentGame (winner);
						}
					}
				}
			}
		}
	}

	public override bool CanSupportPlayers(int players) {
		return true;
	}
}
