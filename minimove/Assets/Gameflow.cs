using UnityEngine;
using System.Collections.Generic;
using System.Collections;


public class GameFlow {
	private static readonly System.Random rnd = new System.Random();
	List<MovePlayer> players = new List<MovePlayer>();
	MiniGame currentGame = null;
	MonoBehaviour behaviour = null;
	int remainingGames = 0;

	public GameFlow(GameObject gameObject, MonoBehaviour behaviour) {
		int count = UniMoveController.GetNumConnected ();
		Debug.Log ("Connected controllers: " + count);

		int player = 0;
		for (int i = 0; i < count; i++) {
			MovePlayer mp = new MovePlayer (gameObject, player);
			if (mp.Valid()) {
				player++;
				players.Add (mp);
			}
		}

		this.behaviour = behaviour;
		this.remainingGames = GetTunables ().DefaultNumberOfGames;

		SelectNewGame ();
	}

	public void SelectNewGame() {
		// TODO: "New game starts sound"

		foreach (var player in players) {
			player.LEDColor = Color.black;
		}

		Debug.Log("Selecting new game");
		if (remainingGames == 0) {
			Debug.Log ("Session ends");
		} else {
			List<MiniGame> games = new List<MiniGame> ();
			games.Add (new MoveSays (this));
			//games.Add (new ShakeIt (this));

			MiniGame candidate = null;
			do {
				candidate = games [rnd.Next (games.Count)];
			} while (!candidate.CanSupportPlayers(players.Count));

			currentGame = candidate;
				
			currentGame.StartGame ();
			remainingGames--;
		}
	}

	void UpdateControllers() {
		/*
		Color[] colors = { Color.cyan, Color.red, Color.blue, Color.green, Color.magenta };
*/
		foreach (var player in players) {
			// Geht L2, L1, R1, ... (alle PSMoveButton-Werte) durch
			foreach (PSMoveButton button in System.Enum.GetValues(typeof(PSMoveButton))) {
				if (player.move.GetButtonDown (button)) {
					if (currentGame != null) {
						currentGame.ButtonPressed (player, button);
					}
				}
			}

			/*player.LEDColor = colors [player.PlayerNumber % colors.Length];

			if (player.move.GetButtonDown (PSMoveButton.Cross)) {
				Debug.Log ("Button pressed");
			}*/

			player.Update ();
		}
	}

	public IEnumerator DestroySoundLater(GameObject go, AudioSource src) {
		while (src.isPlaying) {
			yield return new WaitForSeconds (0.01f);
		}

		Object.Destroy (go);
	}
		
	public void PlaySound(string sound, float volume=1.0f, float pitch=1.0f) {
		GameObject soundObject = GameObject.Find (sound);
		AudioSource soundSource = soundObject.GetComponent<AudioSource> ();

		GameObject go = new GameObject ("Playing:" + sound);
		AudioSource src = go.AddComponent<AudioSource> ();
		src.volume = volume;
		src.pitch = pitch;
		src.clip = soundSource.clip;
		src.Play ();
		behaviour.StartCoroutine (DestroySoundLater (go, src));
	}

	public void Update () {
		UpdateControllers ();

		if (currentGame != null) {
			currentGame.Update ();
		}
	}

	public TunableVariables GetTunables() {
		return behaviour.GetComponent<TunableVariables> ();
	}

	public void endCurrentGameNoWinner() {
		endCurrentGame (new List<MovePlayer>() {});
	}

	public void endCurrentGame(MovePlayer winner) {
		endCurrentGame (new List<MovePlayer>() { winner });
	}

	public void endCurrentGame(List<MovePlayer> winners) {
		Debug.Log ("Game ends, winner(s): " + winners);

		foreach (var player in players) {
			player.LEDColor = Color.black;
		}
			
		// Disable access to "old" current game; new current game
		// will be set by the winner player 
		currentGame = null;

		if (winners.Count == 0) {
			// TODO: Play "nobody wins" sound/animation and wait a bit before new game
			SelectNewGame ();
		} else {
			OnFinished onFinished = delegate () {
				SelectNewGame();
			};

			foreach (var winner in winners) {
				//winner.LEDColor = Color.white;
				StartCoroutine (winner.WinAnimation (GetTunables (), onFinished));
				winner.Score++;
				onFinished = delegate() {
					// Do nothing
				};
			}
		}
	}

	public void StartCoroutine(IEnumerator coroutine) {
		behaviour.StartCoroutine (coroutine);
	}

	public List<MovePlayer> Players {
		get { return players; }
	}

	public string StatusMessage {
		get {
			string result = "";
			if (currentGame != null) {
				result += "current game: " + currentGame;
				result += "\n" + currentGame.StatusMessage ();
			} else {
				result += "no current game";
			}
			foreach (var player in players) {
				result += "\n";
				result += "Player " + (player.PlayerNumber + 1) + ": " + player.Score + " points";
			}
			return result;
		}
	}
}
