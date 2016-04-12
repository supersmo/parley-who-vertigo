using UnityEngine;
using System.Collections;
using System.Collections.Generic;


public delegate void OnFinished();

public class AnimationPart {
	public Color color;
	public float duration;

	public AnimationPart(Color color, float duration) {
		this.color = color;
		this.duration = duration;
	}
}

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

	public bool Valid() {
		return (move.ConnectionType == PSMoveConnectionType.Bluetooth);
	}

	public void Update() {
		//
	}

	public IEnumerator SphereColorAnimation(List<AnimationPart> parts, OnFinished onFinished, OnFinished onChanged=null) {
		foreach (AnimationPart part in parts) {
			LEDColor = part.color;
			if (onChanged != null) {
				onChanged.Invoke ();
			}
			yield return new WaitForSeconds (part.duration);
		}

		onFinished.Invoke ();
	}
		

	public IEnumerator WinAnimation(TunableVariables tunables, OnFinished onFinished) {
		List<AnimationPart> parts = new List<AnimationPart>();

		for (int i=0; i<tunables.WinAnimationBlinks; i++) {
			parts.Add (new AnimationPart (tunables.WinAnimationColor, tunables.BlinkDurationSec));
			parts.Add (new AnimationPart (Color.black, tunables.BlinkDurationSec));
		}

		return SphereColorAnimation (parts, onFinished);

	}

	public bool NowShaking(TunableVariables tunables) {
		return (move.Acceleration.magnitude >= tunables.ShakeThreshold);
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