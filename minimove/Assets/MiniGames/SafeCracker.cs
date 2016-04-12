using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public enum SolveState {
	Searching,
	Found,
	Activated,
	Afterglow,
}

public class SafeCracker : MiniGame {
	private System.Random rnd = new System.Random ();
	private static readonly Color SafeColor = new Color (0.7f, 0.6f, 0f);
	int [] angles;
	int [] targetAngles;
	int [] lastClickAngles;
	int [] solvedLocks;
	SolveState [] solveState;
	int angleSteps = 12;
	int numberOfLocks = 2;
	int playersReady = 0;

	public SafeCracker(GameFlow gameFlow) : base(gameFlow) {
	}

	public override string StatusMessage() {
		string result = "";
		for (int i = 0; i < angles.Length; i++) {
			result += "[" + i + "] = " + angles [i] + ", ";
		}/*
		result += "\n";
		for (int i = 0; i < targetAngles.Length; i++) {
			result += "targetAngles[" + i + "] = " + targetAngles [i] + ", ";
		}
		result += "\n";
		for (int i = 0; i < solvedLocks.Length; i++) {
			result += "solvedLocks[" + i + "] = " + solvedLocks [i] + ", ";
		}*/

		return result;
	}

	public override void StartGame () {
		OnFinished onIntroBlinkingFinished = delegate() {
			playersReady++;

			if (playersReady == gameFlow.Players.Count) {
				angles = new int[gameFlow.Players.Count];
				foreach (var player in gameFlow.Players) {
					angles [player.PlayerNumber] = 0;
				}

				targetAngles = new int[gameFlow.Players.Count];
				foreach (var player in gameFlow.Players) {
					targetAngles [player.PlayerNumber] = rnd.Next (angleSteps) * 360 / angleSteps;
				}

				lastClickAngles = new int[gameFlow.Players.Count];
				foreach (var player in gameFlow.Players) {
					lastClickAngles [player.PlayerNumber] = 0;
				}

				solvedLocks = new int[gameFlow.Players.Count];
				foreach (var player in gameFlow.Players) {
					solvedLocks [player.PlayerNumber] = 0;
				}

				solveState = new SolveState[gameFlow.Players.Count];
				foreach (var player in gameFlow.Players) {
					solveState [player.PlayerNumber] = SolveState.Searching;
				}
			}
		};

		gameFlow.PlaySound("SafeAnnounceSound");

		foreach (var player in gameFlow.Players) {
			List<AnimationPart> parts = new List<AnimationPart> ();
			parts.Add(new AnimationPart(SafeColor*0.2f, 0.4f, 0.6f));
			parts.Add(new AnimationPart(SafeColor, 0.5f, 0.7f));
			parts.Add(new AnimationPart(Color.black, 0.4f));

			gameFlow.StartCoroutine(player.SphereColorAnimation (parts, onIntroBlinkingFinished));
		}
	}

	public IEnumerator ResetSearch(MovePlayer player, float delay) {
		yield return new WaitForSeconds (delay);

		solvedLocks [player.PlayerNumber]++;
		if (solvedLocks [player.PlayerNumber] == numberOfLocks) {
			gameFlow.endCurrentGame (player);
		} else {
			targetAngles [player.PlayerNumber] = rnd.Next (angleSteps) * 360 / angleSteps;
			solveState [player.PlayerNumber] = SolveState.Searching;
		}
	}

	public override void Update () {
		if (playersReady < gameFlow.Players.Count) {
			return;
		}

		int threshold = 360 / angleSteps;
		foreach (var player in gameFlow.Players) {
			int newAngle = (int)player.SafeAngle ();
			if (Mathf.Abs(newAngle - lastClickAngles [player.PlayerNumber]) > 20f ) {
				gameFlow.PlaySound ("SafeClickSound", 0.3f);
				lastClickAngles [player.PlayerNumber] = newAngle;
			}
			angles [player.PlayerNumber] = newAngle;

			bool isNear = (angles [player.PlayerNumber] >= targetAngles [player.PlayerNumber] &&
			               angles [player.PlayerNumber] <= targetAngles [player.PlayerNumber] + threshold);

			// State transitions
			switch (solveState [player.PlayerNumber]) {
				case SolveState.Searching:
					if (isNear && !player.IsTriggerPressed()) {
						solveState [player.PlayerNumber] = SolveState.Found;
					}
					break;
				case SolveState.Found:
					if (!isNear) {
						solveState [player.PlayerNumber] = SolveState.Searching;
					} else if (player.IsTriggerPressed ()) {
						solveState [player.PlayerNumber] = SolveState.Activated;
					}
					break;
				case SolveState.Activated:
					gameFlow.StartCoroutine (ResetSearch (player, 0.2f));
					solveState [player.PlayerNumber] = SolveState.Afterglow;
					break;
				case SolveState.Afterglow:
					break;
			}

			// State actions
			switch (solveState [player.PlayerNumber]) {
				case SolveState.Searching:
					player.LEDColor = Color.black;
					player.Rumble = 0f;
					break;
				case SolveState.Found:
					player.LEDColor = Color.black;
					player.Rumble = 0.5f;
					break;
				case SolveState.Activated:
					player.LEDColor = SafeColor;
					player.Rumble = 0.5f;
					break;
				case SolveState.Afterglow:
					player.LEDColor = SafeColor;
					player.Rumble = 1f;
					break;
			}

			/*
			if () {
				player.Rumble = 0.5f;
				if (player.IsTriggerPressed ()) {
					player.LEDColor = SafeColor;
				} else {
					player.LEDColor = Color.black;
				}
			} else {
				player.LEDColor = Color.black;
				player.Rumble = 0f;
			}*/
		}
	}

	public override bool CanSupportPlayers(int players) {
		return true;
	}
}
