using UnityEngine;
using System.Collections;


public class MovePlayer {
	int playerNumber;
	public UniMoveController move;
	Color color;

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
	}

	public void Update() {
		//
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
}