# Progressive Radiation Damage

Standalone S.T.A.L.K.E.R. Anomaly 1.5.3 addon that makes accumulated radiation meaningfully damage the actor at the three dangerous EGUI radiation states.

The implementation is inspired by Grok's progressive radiation damage: it reads the canonical `db.actor.radiation` value and applies health loss on a fixed one-second timer, independent of frame rate. It does not replace Arszi's scripts or radiation-zone configuration.

## Damage model

EGUI divides accumulated radiation into four visual states with `ceil(radiation * 4)`. The first grey state remains a warning band. The following three states add progressively stronger damage:

- Yellow, above 25% through 50% radiation: 0.15% health per second.
- Orange, above 50% through 75% radiation: 0.60% health per second.
- Red, above 75% radiation: 2.00% health per second.

The rates are editable in MCM. Lowering radiation immediately moves the actor to a weaker tier; reaching 25% or less stops this addon's extra damage. Previously lost health is not restored.

## Requirements

- S.T.A.L.K.E.R. Anomaly 1.5.3
- Anomaly Mod Configuration Menu (MCM)

Recommended companions:

- Arszi's Dynamic Radiation Zones and Radiation Overhaul 2.1
- Enhanced Graphical User Interface 0.6.6a
- Arszi Radiation EGUI Indicator Compatibility
- BHRSO Compatibility

The addon also works with other setups that use the engine's canonical `db.actor.radiation` value.

## Installation

Install the release ZIP with Mod Organizer 2 after the radiation overhaul and UI compatibility addons. Restart the game. A new game is not required.

Configure it under **MCM -> Progressive Radiation Damage**.

The release archive starts directly with `gamedata/` and has no wrapper directory.

## Compatibility

- Uses a unique script and does not overwrite Arszi, EGUI, BHS, or BHRSO files.
- Applies global actor-health damage, matching Grok's approach; it does not directly damage individual BHS limbs.
- Arszi remains responsible for dose intake, removal, weather effects, equipment protection, symptoms, and its original very slow radiation damage.
- Removing the addon is save-safe because it stores no save data.

## Credits

- Grokitach — reference design for frame-rate-independent progressive radiation damage.
- Arszi — Dynamic Radiation Zones and Radiation Overhaul.
- INC and RavenAscendant — EGUI and its AltIcons radiation-state presentation.

## License

The original code in this repository is licensed under the MIT License. Third-party addons and game assets remain the property of their respective authors.
