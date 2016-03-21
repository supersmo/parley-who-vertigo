using UnityEngine;
using System.Collections;

public abstract class MiniGame {
	protected GameFlow gameFlow;

	public MiniGame(GameFlow gameFlow) {
		this.gameFlow = gameFlow;
	}

	public virtual void ButtonPressed(MovePlayer player, PSMoveButton button) {
	}

	public abstract void StartGame ();
	public abstract void Update ();
}