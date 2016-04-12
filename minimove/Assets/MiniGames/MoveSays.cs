using UnityEngine;
using System.Collections.Generic;
using System.Collections;

public class MoveSays : MiniGame {
	private int playersReady = 0;
	private int playersRemaining = 0;

	public MoveSays(GameFlow gameFlow) : base(gameFlow) {
	}

	public override void StartGame() {
		OnFinished onIntroBlinkingFinished = delegate() {
			playersReady++;

			if (playersReady == gameFlow.Players.Count) {
				foreach (var player in gameFlow.Players) {
					Debug.Log ("Start GAME PLAYER " + player);
					player.LEDColor = PSMoveColor.getRandomColor ();
				}

				playersRemaining = playersReady;
			}
		};

		foreach (var player in gameFlow.Players) {
			List<AnimationPart> parts = new List<AnimationPart> ();
			for (int i=0; i<10; i++) {
				parts.Add(new AnimationPart(PSMoveColor.getRandomColor(), 0.1f));
				parts.Add(new AnimationPart(Color.black, 0.1f));
			}
			OnFinished onChanged = delegate() {
				gameFlow.PlaySound("CycleBlipSound");
			};
			gameFlow.StartCoroutine(player.SphereColorAnimation (parts, onIntroBlinkingFinished, onChanged));
		}
	}

	public override void ButtonPressed(MovePlayer player, PSMoveButton button) {
		if (playersReady < gameFlow.Players.Count) {
			return;
		}

		if (PSMoveColor.isColorButton (button)) {
			Color color = PSMoveColor.colorForButton (button);

			if (color == player.LEDColor) {
				gameFlow.PlaySound ("BeepSound", 0.5f);
				gameFlow.endCurrentGame (player);
			} else {
				gameFlow.PlaySound ("BadBeepSound", 0.5f);
				// TODO: Play "dead" animation
				player.LEDColor = Color.black;
				playersRemaining--;
				if (playersRemaining == 0) {
					gameFlow.endCurrentGameNoWinner ();
				}
			}
		}
	}

	public override void Update() {
	}

	public override bool CanSupportPlayers(int players) {
		return true;
	}
}
