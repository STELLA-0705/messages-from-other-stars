"""
MESSAGES FROM OTHER STARS
A book-like, multi-ending Python narrative game.

Inspired by the uploaded story "Messages From Other Stars."

HOW TO PLAY
-----------
- Run this file with Python 3.
- Type the number of the choice you want.
- Your choices change flags and can lead to different endings.
- Type "save" at a choice prompt to save your progress.
- Type "load" to restore your last save.
- Type "restart" to begin again.
- Type "quit" to leave.

This is an original game adaptation. It does NOT reproduce the source text.
The game keeps the central ideas and atmosphere while giving you new
choices and branching outcomes.
"""

import json
import os
import textwrap
import time

SAVE_FILE = "messages_from_other_stars_save.json"

# ---------------------------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------------------------

WIDTH = 76


def slow_print(text, delay=0.012):
    """Print text like a book/recording transcript."""
    for paragraph in text.strip().split("\n"):
        paragraph = paragraph.rstrip()
        if not paragraph:
            print()
            continue

        # Wrap long lines so the game stays readable in a terminal.
        wrapped = textwrap.wrap(paragraph, WIDTH) or [""]
        for line in wrapped:
            print(line)
            if delay:
                time.sleep(delay)


def divider():
    print("\n" + "─" * WIDTH + "\n")


def chapter(title):
    divider()
    print(title.upper().center(WIDTH))
    divider()


def choice(prompt, options, state):
    """
    Ask the player for a numbered choice.

    Special commands are intentionally simple so this remains a terminal
    game and can run without third-party packages.
    """
    while True:
        print()
        slow_print(prompt)

        for number, option in enumerate(options, 1):
            print(f"  [{number}] {option}")

        print("\n  Commands: save / load / restart / quit")
        answer = input("\n> ").strip().lower()

        if answer == "save":
            save_game(state)
            continue

        if answer == "load":
            if load_game(state):
                print("\n[Progress loaded.]\n")
            continue

        if answer == "restart":
            print("\nRestarting...\n")
            return "__RESTART__"

        if answer == "quit":
            print("\nThe recording clicks off.\n")
            raise SystemExit

        if answer.isdigit():
            number = int(answer)
            if 1 <= number <= len(options):
                return number

        print("\nPlease choose one of the numbered options.")


# ---------------------------------------------------------------------------
# SAVE / LOAD
# ---------------------------------------------------------------------------

def save_game(state):
    """Save the important story flags, not temporary display data."""
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)
        print(f"\n[Saved to {SAVE_FILE}]")
    except OSError as error:
        print(f"\n[Could not save: {error}]")


def load_game(state):
    """Load a previous save into the current state dictionary."""
    if not os.path.exists(SAVE_FILE):
        print("\n[No save file exists yet.]")
        return False

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        state.clear()
        state.update(saved)
        return True
    except (OSError, json.JSONDecodeError) as error:
        print(f"\n[Could not load save: {error}]")
        return False


def new_state():
    """Create the flags used by the branching story."""
    return {
        "chapter": 1,

        # The two versions of Rei gradually become aware of one another.
        "trust": 0,
        "curiosity": 0,

        # The player can decide whether to cling to logic, memory, or
        # connection.
        "logic": 0,
        "memory": 0,
        "connection": 0,

        # These flags unlock special endings.
        "followed_signal": False,
        "kept_key": False,
        "left_message": False,
        "entered_hole": False,
        "waited": False,
        "shared_food": False,
        "rejected_hole": False,
    }



# ---------------------------------------------------------------------------
# DELTARUNE-STYLE ENCOUNTERS
# ---------------------------------------------------------------------------

def battle_box(lines):
    """Draw a simple RPG-style text box."""
    print("\n+" + "-" * 68 + "+")
    for line in lines:
        for wrapped in textwrap.wrap(line, 66) or [""]:
            print("| " + wrapped.ljust(66) + " |")
    print("+" + "-" * 68 + "+")


def bullet_phase(pattern="calm"):
    """
    A tiny text version of a bullet-dodging phase.

    It is deliberately simple: instead of requiring real-time keyboard
    controls, the player chooses where the heart moves. This keeps the game
    compatible with ordinary Python/Notepad/PowerShell setups.
    """
    positions = ["LEFT", "CENTER", "RIGHT"]

    print("\n      +-------------------------------+")
    print("      |       *   .       *           |")
    print("      |   .       [ HEART ]     .     |")
    print("      |        *       .              |")
    print("      +-------------------------------+")

    while True:
        print("\nThe red heart is in the CENTER.")
        print("[1] LEFT     [2] CENTER     [3] RIGHT")
        answer = input("> ").strip()

        if answer in ("1", "2", "3"):
            position = positions[int(answer) - 1]

            # Different attacks have different "safe" spots.
            if pattern == "left":
                safe = "RIGHT"
            elif pattern == "right":
                safe = "LEFT"
            else:
                safe = "CENTER"

            if position == safe:
                print("\n* The heart slips safely through the attack.")
                return True

            print("\n* The heart bumps into a stray spark.")
            print("* You take 1 damage.")
            return False

        print("Choose 1, 2, or 3.")


def encounter_rei(state):
    """
    A major encounter with the other Rei.

    The menu intentionally uses the familiar FIGHT / ACT / ITEM / MERCY
    structure, but the actual mechanics are original to this game.
    """
    chapter("A Strange Encounter")

    battle_box([
        "* ADACHI REI appears.",
        "* She looks exactly like you.",
        "* She is holding a recording device.",
        "* She doesn't attack.",
        "* ...yet."
    ])

    spared = False
    encounter_turns = 0

    while True:
        encounter_turns += 1

        print("\n             [ FIGHT ] [ ACT ]")
        print("             [ ITEM  ] [ MERCY ]")
        action = input("\n> ").strip().lower()

        if action in ("fight", "1"):
            battle_box([
                "* You raise your hand.",
                "* Rei flinches.",
                "* She doesn't understand why you're doing that.",
            ])

            if bullet_phase("left"):
                print("\n* You stop yourself.")
                print("* You don't want to hurt her.")
                state["connection"] += 2
                continue
            else:
                print("\n* Rei takes a step backward.")
                state["trust"] -= 1
                continue

        elif action in ("act", "2"):
            print("\nACT")
            print("[1] ASK ABOUT THE RECORDINGS")
            print("[2] TALK ABOUT HOME")
            print("[3] TELL HER SHE ISN'T ALONE")
            print("[4] COMPLIMENT HER RIBBON")

            act = input("> ").strip()

            if act == "1":
                battle_box([
                    "* You ask about the recordings.",
                    "* Rei checks the device.",
                    '* "They are all real."',
                    '* "That is the problem."',
                ])
                state["curiosity"] += 1
                state["trust"] += 1

            elif act == "2":
                battle_box([
                    "* You compare memories.",
                    "* She remembers a different childhood.",
                    "* Somehow, both memories feel familiar.",
                ])
                state["memory"] += 2
                state["connection"] += 1

            elif act == "3":
                battle_box([
                    "* You tell Rei she isn't alone.",
                    "* She stops.",
                    '* "...What?"',
                    "* Her grip on the recorder loosens.",
                ])
                state["connection"] += 3
                state["trust"] += 2

            elif act == "4":
                battle_box([
                    "* You point at her white ribbon.",
                    '* "I like it."',
                    "* She looks genuinely confused.",
                    '* "...You do?"',
                    "* She smiles a little.",
                ])
                state["connection"] += 2
                state["trust"] += 1

            else:
                print("* Rei waits.")

        elif action in ("item", "3"):
            print("\nITEM")
            print("[1] WATER")
            print("[2] OLD CANDY WRAPPER")
            print("[3] THE CAR KEY")
            item = input("> ").strip()

            if item == "1":
                battle_box([
                    "* You offer Rei some water.",
                    "* She stares at it.",
                    '* "You can have it."',
                    '* "...Really?"',
                    "* She accepts it carefully.",
                ])
                state["shared_food"] = True
                state["connection"] += 2
                state["trust"] += 1

            elif item == "2":
                battle_box([
                    "* You show her an old candy wrapper.",
                    "* She laughs.",
                    '* "I used to keep things like that too."',
                    "* For a moment, the two of you remember being children.",
                ])
                state["memory"] += 2
                state["connection"] += 2

            elif item == "3":
                battle_box([
                    "* You show her the old key.",
                    "* Rei goes completely still.",
                    '* "You kept it."',
                    "* Somehow, she already knew.",
                ])
                state["kept_key"] = True
                state["memory"] += 2
                state["trust"] += 1

            else:
                print("* You don't have anything useful.")

        elif action in ("mercy", "4"):
            if state["connection"] >= 3 and state["trust"] >= 2:
                battle_box([
                    "* You lower your hands.",
                    "* Rei lowers hers.",
                    "* The recording device stops buzzing.",
                    "* ...",
                    "* Nobody wins.",
                    "* Nobody has to.",
                ])
                spared = True
                break

            battle_box([
                "* You choose MERCY.",
                "* Rei doesn't understand.",
                '* "Why?"',
                "* You don't have an answer yet.",
            ])
            state["connection"] += 1

        else:
            print("* The encounter waits for your decision.")

    if spared:
        state["connection"] += 2
        state["trust"] += 2
        slow_print("""
The room becomes quiet.

Not peaceful.

Just quiet.

Then Rei looks at you.

* She smiles.

"I think..."

She hesitates.

"...I think we can figure this out."
""")


def weird_event(state):
    """
    Short DELTARUNE-like room event.

    The leading '*' is intentional: it gives the game that compact,
    expressive narration style the user asked for.
    """
    chapter("???")

    slow_print("""
* The recording device vibrates.

* Once.

* Twice.

* Then it stops.

* You wait.

* Nothing happens.

* ...

* Something is standing behind you.
""")

    print("\n[1] Turn around.")
    print("[2] Pretend you didn't notice.")
    print("[3] Say hello.")

    answer = input("> ").strip()

    if answer == "1":
        slow_print("""
* You turn around.

* There's nobody there.

* You look at the floor.

* There are two sets of footprints.

* Yours.

* And yours.
""")
        state["curiosity"] += 2

    elif answer == "2":
        slow_print("""
* You pretend you didn't notice.

* The footsteps stop.

* Good choice.

* Probably.
""")
        state["logic"] += 1

    else:
        slow_print("""
* "Hello?"

* Silence.

* Then, very quietly:

* "Hello."

* It sounds exactly like you.
""")
        state["connection"] += 2

# ---------------------------------------------------------------------------
# THE GAME
# ---------------------------------------------------------------------------

def ending_title(title):
    divider()
    print(("ENDING: " + title).center(WIDTH))
    divider()


def ending(state, kind):
    """Show one of the game's endings."""
    if kind == "signal":
        ending_title("THE SIGNAL CONTINUES")

        slow_print("""
The recorder does not go silent.

For the first time, there are two voices on the same channel.

Neither of you knows whether the starry opening is a doorway, a wound in
reality, or simply something that should never have existed.

You decide not to find out alone.

One message becomes two.

Two become dozens.

You trade memories instead of coordinates. A childhood joke. A description
of rain. The sound of a piano from another room. The shape of a ribbon tied
into hair.

The world outside is still broken.

But the recording device keeps blinking.

Someone is listening.

And, for now, someone is answering.

[THE END]
""")

    elif kind == "hole":
        ending_title("BETWEEN STARS")

        slow_print("""
You step toward the impossible opening.

The stars inside it do not look like the stars above.

For one strange moment, you can see two homes at once: two living rooms,
two red skies, two lives that should never have touched.

Then the signal becomes a voice.

Not a warning.

Not an order.

A question.

You realize the hole was never asking you to disappear.

It was asking whether you would cross a boundary without knowing what waited
on the other side.

You turn back.

The opening remains.

So does the other voice.

You leave the impossible door open and walk away from it together.

[THE END]
""")

    elif kind == "alone":
        ending_title("NO ANSWER")

        slow_print("""
The recorder waits.

You wait.

The red sky slowly becomes darker.

You tell yourself that the other voice was interference. A damaged memory.
A trick produced by a dying machine.

Maybe that is true.

But every few minutes, the recorder gives a tiny electronic click.

As if someone, somewhere, is trying to speak.

You never answer.

[THE END]
""")

    elif kind == "memory":
        ending_title("THE THINGS THAT STAY")

        slow_print("""
You sit beneath the red sky and begin recording.

Not because the recording will save the world.

It won't.

You record the little things.

The taste of cheap candy.

The sound of someone laughing in another room.

A childhood drawing.

A key that no longer opens anything.

The name of someone you still remember.

When the device finally runs out of power, you have filled its last space.

There is no miracle.

There is no restored world.

But there is a record.

Someone was here.

Someone remembered.

[THE END]
""")

    elif kind == "shared":
        ending_title("TWO VOICES")

        slow_print("""
You find the other Rei.

Neither of you speaks at first.

It is unsettling to look at a person who has your face and your voice but
none of your memories.

Then she laughs.

You laugh too.

For a moment, the world feels almost ordinary.

You cannot repair the star.

You cannot resurrect everyone.

You cannot undo the years that made you both who you are.

But you can sit in the same room.

You can share the food.

You can take turns recording.

And when one of you says, "Are you still there?"

the other answers:

"Yeah."

[THE END]
""")

    else:
        ending_title("STATIC")

        slow_print("""
The signal dissolves into static.

Maybe the worlds separated.

Maybe they never existed together.

Maybe some things are not meant to be understood.

The recorder keeps running until there is nothing left to record.

[THE END]
""")


def game():
    """Main game loop."""
    state = new_state()

    while True:
        # ---------------------------------------------------------------
        # CHAPTER 1
        # ---------------------------------------------------------------
        chapter("Chapter One — The Recording")

        slow_print("""
There is a recording device on the desk.

You have never seen it before.

It should not be here.

The government stopped distributing devices like this years ago. Yours
came from someone who is gone now, and you have kept it because throwing
things away has always felt like losing people twice.

The device has one new light.

A contact.

ADACHI REI.

You stare at the name.

Then the device plays a recording.

The voice is yours.

But you do not remember saying any of it.
""")

        c = choice(
            "What do you do?",
            [
                "Listen to the entire recording.",
                "Turn the device off.",
                "Check the contact information first.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["curiosity"] += 2
            state["connection"] += 1
            slow_print("""
The recording talks about a different childhood.

A family.

Food that was once ordinary.

A father who left behind a recording device.

A world that ended beneath a dying star.

Then the voice says something that makes your hands go cold:

"I think there's someone else here."

""")
        elif c == 2:
            state["logic"] += 1
            slow_print("""
You switch it off.

Silence.

Ten seconds later, the screen turns itself back on.

The same contact is still there.

The same name.

Your name.

Maybe it is broken.

You decide you will investigate later.
""")
        else:
            state["logic"] += 2
            slow_print("""
The contact record is impossible.

The timestamp is older than the device itself.

The voiceprint is yours.

The location attached to the message is somewhere that no longer exists.

You do not understand it.

That bothers you more than being afraid.
""")

        # ---------------------------------------------------------------
        # CHAPTER 2
        # ---------------------------------------------------------------
        chapter("Chapter Two — The Other Recording")

        slow_print("""
A second recording arrives.

This time, the voice sounds frightened.

"I know you're there."

A pause.

"You're not supposed to exist."

Then static.

The device displays a map.

The destination is a house that looks exactly like yours.

You can either follow the coordinates, or stay where you are and send a
message first.
""")

        c = choice(
            "How do you respond?",
            [
                "Go to the house.",
                "Send a message: 'I'm here.'",
                "Ignore the coordinates and study the recordings.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["followed_signal"] = True
            state["trust"] += 1
            slow_print("""
You take the old road.

The farther you travel, the stranger the world becomes.

The sky is still red.

Ash covers the ground.

And when you finally see the house, you realize something impossible:

Half of it is yours.

The other half is not.
""")
        elif c == 2:
            state["left_message"] = True
            state["connection"] += 2
            state["trust"] += 1
            slow_print("""
You speak into the recorder.

"Hey."

Your voice sounds embarrassingly small.

"I don't know who you are. But if you're hearing this... I'm here."

The answer arrives almost immediately.

"...You're real."

Then another message.

"I thought I was alone."

""")
        else:
            state["logic"] += 2
            state["memory"] += 1
            slow_print("""
You listen carefully.

The recordings describe two lives that should be impossible to share one
name.

One Rei remembers warmth.

The other remembers achievement without affection.

One remembers people.

The other remembers surviving them.

Neither remembers being the other.

You write one sentence in your notebook:

SAME PERSON. DIFFERENT LIFE.
""")

        # ---------------------------------------------------------------
        # CHAPTER 3
        # ---------------------------------------------------------------
        chapter("Chapter Three — The Red Sky")

        slow_print("""
Outside, the star hangs over the horizon.

It is enormous.

Dark at its center, surrounded by burning color.

You remember the announcement: the star's collapse should have killed
everyone.

And yet you are still here.

The recorder crackles.

A new message:

"There's something in my house."

Another:

"It's filled with stars."

You look toward the house.

There is a glow coming through one of the windows.
""")

        c = choice(
            "What do you investigate first?",
            [
                "The glowing room.",
                "The recorder's radio signal.",
                "The old memories stored on the device.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["curiosity"] += 2
            slow_print("""
The living room is split by a strange opening.

It is not a hole in the floor.

It is not a hole in the wall.

It is a hole in the idea of the room.

Stars move inside it.

You can see another house through them.

And someone is standing there.

Someone with your face.
""")
        elif c == 2:
            state["logic"] += 2
            slow_print("""
You tune the radio.

Static.

Then a voice.

"...If you can hear me, don't trust the hole."

Static.

Then:

"...But don't leave me alone."

The signal dies.

You are not sure which part of the message scares you more.
""")
        else:
            state["memory"] += 2
            slow_print("""
The recordings become older.

A birthday.

A family dinner.

A school day.

A forgotten joke.

The memories are ordinary.

That is what makes them hurt.

The end of the world did not erase the small things.

It only made them impossible to get back.
""")

        # A small strange-room event between chapters.
        weird_event(state)

        # ---------------------------------------------------------------
        # CHAPTER 4
        # ---------------------------------------------------------------
        chapter("Chapter Four — The Key")

        slow_print("""
On the floor, you find an old key.

You know what it opens.

A car.

The car is ruined, but the key survived.

You turn it over in your hand.

For some reason, the other Rei's recording begins playing.

"I kept the key."

A pause.

"I don't know why."

You understand.

Sometimes an object is not useful because of what it opens.

Sometimes it is useful because of what it remembers.
""")

        c = choice(
            "What do you do with the key?",
            [
                "Keep it.",
                "Leave it behind.",
                "Put it beside the recording device.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["kept_key"] = True
            state["memory"] += 2
            slow_print("""
You put the key in your pocket.

It is heavy.

Not physically.

Emotionally.

You keep walking.
""")
        elif c == 2:
            state["logic"] += 1
            state["rejected_hole"] = True
            slow_print("""
You leave it where you found it.

A useless key is still a useless key.

You do not need another object tying you to the past.

At least, that is what you tell yourself.
""")
        else:
            state["memory"] += 1
            state["connection"] += 1
            slow_print("""
You place the key beside the recorder.

A new message appears.

"You kept it too."

You stare at the screen.

There is no possible way she should know that.
""")

        # ---------------------------------------------------------------
        # CHAPTER 5
        # ---------------------------------------------------------------
        chapter("Chapter Five — Are You Still There?")

        slow_print("""
The other Rei speaks again.

"I don't know where I am."

A pause.

"I don't know if you're still there."

The recorder waits.

You realize this is no longer about proving whether parallel universes
exist.

There is a person on the other side.

Maybe.

And they are waiting for an answer.
""")

        c = choice(
            "What do you say?",
            [
                "I'm still here.",
                "Tell me who you are.",
                "I don't know if I can help you.",
                "Say nothing.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["connection"] += 3
            state["trust"] += 2
            state["left_message"] = True
            slow_print("""
"I'm still here."

The response takes several minutes.

Then:

"Thank you."

Only two words.

But you replay them three times.
""")
        elif c == 2:
            state["curiosity"] += 2
            state["connection"] += 1
            slow_print("""
"I've been asking myself that too."

The voice tells you about a childhood you never had.

Then she asks:

"Do you remember being happy?"

You don't know how to answer.
""")
        elif c == 3:
            state["logic"] += 1
            state["connection"] += 1
            slow_print("""
"I don't know if I can help you."

The reply is quiet.

"Neither do I."

Then:

"Maybe that's okay."

""")
        else:
            state["logic"] += 1
            state["rejected_hole"] = True
            slow_print("""
You say nothing.

The device waits.

Eventually, the contact goes quiet.

You wonder if silence can be an answer.

You hope it isn't.
""")

        # ---------------------------------------------------------------
        # CHAPTER 6
        # ---------------------------------------------------------------
        chapter("Chapter Six — The Meeting")

        slow_print("""
You return to the house.

The starry opening is still there.

The other Rei is on the opposite side.

For a second, neither of you moves.

Then she raises a hand.

You do the same.

Two people.

One face.

Two histories.

Neither of you knows what happens next.
""")

        c = choice(
            "What do you do?",
            [
                "Step closer.",
                "Ask her to stay where she is.",
                "Walk away from the opening.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["connection"] += 3
            state["trust"] += 2
            slow_print("""
The opening flickers.

For a heartbeat, you feel the two worlds touch.

Not physically.

Emotionally.

You understand something neither of you could explain through logic:

You are not the same person.

But you are not strangers either.
""")
        elif c == 2:
            state["logic"] += 1
            state["trust"] += 1
            slow_print("""
"Stay there."

She nods.

You both sit on opposite sides of the impossible boundary.

You begin talking.

Slowly.

Carefully.

You compare memories.

You discover that neither life was perfect.

But each of you remembers things the other never got to have.
""")
        else:
            state["rejected_hole"] = True
            state["memory"] += 1
            slow_print("""
You step away.

The hole remains behind you.

You are not sure whether you are escaping danger or abandoning the only
person who might understand you.

The recorder follows with one last message:

"Please don't leave."

""")

        # The two Reis finally get a proper RPG-style encounter.
        encounter_rei(state)

        # ---------------------------------------------------------------
        # CHAPTER 7 — FINAL CHOICE
        # ---------------------------------------------------------------
        chapter("Chapter Seven — The Last Message")

        slow_print("""
The star is getting brighter.

There may not be much time.

The recorder gives you three choices.

Stay.

Cross.

Or speak.

The strange thing is that none of them feel like the correct answer.

Maybe there isn't one.

Maybe the point is simply choosing what matters to you.
""")

        c = choice(
            "What will you do?",
            [
                "Stay and record the memories.",
                "Cross through the starry opening.",
                "Wait for the other Rei and try to live together.",
                "Leave the house and follow the radio signal.",
                "ACT: record one final message.",
            ],
            state,
        )

        if c == "__RESTART__":
            state = new_state()
            continue

        if c == 1:
            state["memory"] += 3
            ending(state, "memory")
            break

        if c == 2:
            if state["rejected_hole"]:
                slow_print("""
You hesitate.

You remember why you walked away before.

But this time, you choose to look.

Not because you know what is waiting.

Because you have decided that uncertainty is not automatically the same
thing as danger.
""")
            state["entered_hole"] = True
            ending(state, "hole")
            break

        if c == 3:
            state["waited"] = True
            state["shared_food"] = True
            ending(state, "shared")
            break

        # Choice 5 is the final ACT-style option.
        if c == 5:
            state["left_message"] = True
            state["memory"] += 2
            state["connection"] += 2

            battle_box([
                "* You press RECORD.",
                "* The red light comes on.",
                "* You take a breath.",
                '* "If anyone is listening..."',
                "* You stop.",
                "* You don't need a perfect ending.",
                "* You just need to leave something behind.",
            ])

            if state["connection"] >= 4:
                ending(state, "signal")
            else:
                ending(state, "memory")
            break

        # Choice 4: the ending depends on whether the player built a
        # meaningful connection.
        if state["connection"] >= 4 and state["trust"] >= 2:
            ending(state, "signal")
        else:
            ending(state, "alone")
        break


# ---------------------------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * WIDTH)
    print("MESSAGES FROM OTHER STARS".center(WIDTH))
    print("A branching terminal story".center(WIDTH))
    print("=" * WIDTH)

    slow_print("""
The recorder clicks on.

Somewhere, another version of you is listening.

Press Enter to begin.
""", delay=0.008)

    input()

    try:
        game()
    except KeyboardInterrupt:
        print("\n\nThe recording ends abruptly.")
