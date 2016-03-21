using UnityEngine;
using System.Collections;

public abstract class MiniGame {
	GameFlow gameFlow;

	public MiniGame(GameFlow gameFlow) {
		this.gameFlow = gameFlow;
	}

	public void StartGame() {
		// ...
	}

	public abstract void Update ();
}