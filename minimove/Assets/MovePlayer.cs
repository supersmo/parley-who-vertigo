using UnityEngine;
using System.Collections;
using System.Collections.Generic;


public delegate void OnFinished();

public class AnimationPart {
	public Color color;
	public float duration;
	public float rumble;

	public AnimationPart(Color color, float duration, float rumble=0f) {
		this.color = color;
		this.duration = duration;
		this.rumble = rumble;
	}
}

public class MovePlayer {
	int playerNumber;
	public UniMoveController move;
	Color color;
	float rumble;
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
		this.rumble = 0f;
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
			Rumble = part.rumble;
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

	public bool IsUnstable(TunableVariables tunables) {
		return (move.Acceleration.magnitude >= tunables.UnstableThreshold);
	}

	public float SafeAngle() {
		Vector2 v = new Vector2 (move.Acceleration.x, move.Acceleration.y);
		v.Normalize ();
		float result =  Mathf.Atan2 (v.x, v.y) * 180f / Mathf.PI;
		if (result < 0) {
			result += 360f;
		}
		return result;
	}

	public bool IsTriggerPressed() {
		return move.GetButton (PSMoveButton.Trigger);
	}
		
	public Color LEDColor
	{
		get { return color; }
		set { color = value; move.SetLED (color); }
	}

	public float Rumble
	{
		get { return rumble; }
		set {
			rumble = value;
			move.SetRumble (Rumble);
		}
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