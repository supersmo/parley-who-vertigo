﻿using UnityEngine;
using System.Collections;


public class MovePlayer {
	int playerNumber;
	public UniMoveController move;
	Color color;
	int score;

	public MovePlayer(GameObject gameObject, int playerNumber) {
		this.playerNumber = playerNumber;
		this.move = gameObject.AddComponent<UniMoveController> ();
		for (int j=0; j<100; j++) {
			if (!move.Init (playerNumber)) {
				Debug.Log ("Failed to init controller#" + playerNumber);
			} else {
				Debug.Log ("Connected");
				break;
			}
		}
		this.color = Color.white;
		this.score = 0;
	}

	public void Update() {
		//
	}

	public IEnumerator WinAnimation(TunableVariables tunables) {
		for (int i=0; i<tunables.WinAnimationBlinks; i++) {
			LEDColor = tunables.WinAnimationColor;
			yield return new WaitForSeconds(tunables.BlinkDurationSec);
			LEDColor = Color.black;
			yield return new WaitForSeconds(tunables.BlinkDurationSec);
		}
	}
		
	public Color LEDColor
	{
		get { return color; }
		set { color = value; move.SetLED (color); }
	}

	public int PlayerNumber
	{
		get { return playerNumber; }
	}

	public int Score
	{
		get { return score; }
		set { score = value; }
	}
}