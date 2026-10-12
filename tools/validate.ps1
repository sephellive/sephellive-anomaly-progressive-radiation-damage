$ErrorActionPreference = "Stop"

$repository = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$script = Join-Path $repository "gamedata\scripts\zzz_sep_progressive_radiation_damage_mcm.script"
$localizations = @(
	(Join-Path $repository "gamedata\configs\text\eng\ui_st_sep_progressive_radiation_damage.xml"),
	(Join-Path $repository "gamedata\configs\text\rus\ui_st_sep_progressive_radiation_damage.xml")
)

foreach ($required in @($script) + $localizations) {
	if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
		throw "Missing required file: $required"
	}
}

$source = Get-Content -LiteralPath $script -Raw
foreach ($token in @(
	'TICK_INTERVAL_MS = 1000',
	'radiation > 0.25',
	'radiation > 0.50',
	'radiation > 0.75',
	'actor:set_health_ex',
	'RegisterScriptCallback("actor_on_update"',
	'function on_mcm_load()'
)) {
	if ($source -notmatch [regex]::Escape($token)) {
		throw "Required implementation token missing: $token"
	}
}

if (Test-Path -LiteralPath (Join-Path $repository "gamedata\configs\creatures\actor.ltx")) {
	throw "The addon must not replace actor.ltx."
}
if (Test-Path -LiteralPath (Join-Path $repository "gamedata\scripts\arszi_radiation.script")) {
	throw "The addon must not replace Arszi's main script."
}

foreach ($xmlPath in $localizations) {
	$document = New-Object System.Xml.XmlDocument
	$document.Load($xmlPath)
	if ($document.string_table.string.Count -lt 10) {
		throw "Localization is incomplete: $xmlPath"
	}
}

Write-Output "Static validation passed: fixed radiation tick, three EGUI damage tiers, MCM and localization found."
