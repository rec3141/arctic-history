# Vessel kind: draft mapping for review

94 distinct values over 200 vessels, mapped to 22 codes.
Proposed: `kind` takes the code; what the code does not say moves to a new `kind_note`
column, so the wiki still reads `barque, purchased into the Navy`.
Rows marked with a diamond are judgement calls; please check those first.

The rule: the code names the rig or the hull where the entry names one, and the work
the vessel was built or fitted for where that is all the entry gives. So a whaling
barque is a `barque` whose note says whaler, while a whaler whose rig no source
records is a `whaler`. Anyone filtering for whaling vessels wants both the `whaler`
and `steam-whaler` codes and the notes.

| code | label | values | vessels |
|---|---|---:|---:|
| ship | full-rigged ship | 3 | 5 |
| barque | barque | 7 | 18 |
| brig | brig | 6 | 9 |
| schooner | schooner | 11 | 21 |
| sloop | sloop | 3 | 3 |
| yacht | yacht | 3 | 3 |
| bomb-vessel | bomb vessel | 1 | 4 |
| boat | ship's boat | 4 | 9 |
| umiak | umiak, an open skin boat | 1 | 1 |
| steamer | steamer | 7 | 9 |
| tender | tender | 1 | 2 |
| icebreaker | icebreaker | 7 | 14 |
| submarine | submarine | 2 | 2 |
| whaler | whaler | 5 | 52 |
| steam-whaler | steam whaler | 2 | 7 |
| sealer | sealer | 5 | 11 |
| research-vessel | research or survey vessel | 3 | 3 |
| cruise-ship | cruise ship | 2 | 4 |
| transport | transport or supply ship | 4 | 6 |
| freighter | freighter | 1 | 1 |
| tanker | tanker | 1 | 1 |
| aircraft | aircraft | 15 | 15 |

## ship

| n | value | kind_note | reads as |
|---:|---|---|---|
| 3 | ship |  | full-rigged ship |
| 1 | frigate | frigate ◆ no frigate code: a frigate is full-rigged, so she is filed as a ship | full-rigged ship, frigate |
| 1 | ship of the Queen's navy | of the Queen's navy | full-rigged ship, of the Queen's navy |

## barque

| n | value | kind_note | reads as |
|---:|---|---|---|
| 6 | barque |  | barque |
| 5 | barque, purchased into the Navy | purchased into the Navy | barque, purchased into the Navy |
| 3 | bark |  ◆ the Elizabethan 'bark' means a small vessel, not the later barque rig | barque |
| 1 | barque, transport | transport | barque, transport |
| 1 | barque, whaler | whaler | barque, whaler |
| 1 | busse | busse ◆ a busse is an Elizabethan fishing vessel; filed with the small Elizabethan hulls | barque, busse |
| 1 | whaling barque | whaler ◆ rig stated, so the rig is the code and the trade the note | barque, whaler |

## brig

| n | value | kind_note | reads as |
|---:|---|---|---|
| 4 | brig |  | brig |
| 1 | brig, strengthened for discovery service | strengthened for discovery service | brig, strengthened for discovery service |
| 1 | brig, whaler | whaler | brig, whaler |
| 1 | brigantine, former whaler | brigantine, formerly a whaler ◆ brigantine folded into brig; the rig is kept in the note | brig, brigantine, formerly a whaler |
| 1 | gun-brig | gun-brig | brig, gun-brig |
| 1 | whaling brig | whaler ◆ rig stated, so the rig is the code and the trade the note | brig, whaler |

## schooner

| n | value | kind_note | reads as |
|---:|---|---|---|
| 8 | schooner |  | schooner |
| 3 | schooner, whaler | whaler | schooner, whaler |
| 2 | motor schooner | motor | schooner, motor |
| 1 | Gloucester fishing schooner | Gloucester fishing | schooner, Gloucester fishing |
| 1 | auxiliary schooner, ice-strengthened | auxiliary, ice-strengthened | schooner, auxiliary, ice-strengthened |
| 1 | mail schooner | mail | schooner, mail |
| 1 | schooner, purpose-built for the ice | purpose-built for the ice | schooner, purpose-built for the ice |
| 1 | steam schooner, purpose-built for ice | steam, purpose-built for ice | schooner, steam, purpose-built for ice |
| 1 | three-masted auxiliary schooner | three-masted, auxiliary | schooner, three-masted, auxiliary |
| 1 | three-masted schooner, purpose-built for the ice | three-masted, purpose-built for the ice | schooner, three-masted, purpose-built for the ice |
| 1 | walrus schooner | walrus hunting | schooner, walrus hunting |

## sloop

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | sloop |  | sloop |
| 1 | sloop, converted for ice | converted for ice | sloop, converted for ice |
| 1 | sloop, converted herring boat | converted herring boat | sloop, converted herring boat |

## yacht

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | screw schooner yacht | screw schooner | yacht, screw schooner |
| 1 | screw steam yacht | screw steam | yacht, screw steam |
| 1 | yacht |  | yacht |

## bomb-vessel

| n | value | kind_note | reads as |
|---:|---|---|---|
| 4 | bomb vessel |  | bomb vessel |

## boat

| n | value | kind_note | reads as |
|---:|---|---|---|
| 3 | pinnace | pinnace | ship's boat, pinnace |
| 3 | ship's boat |  | ship's boat |
| 2 | ship's boats |  | ship's boat |
| 1 | steam launch | steam launch | ship's boat, steam launch |

## umiak

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | open skin boat |  | umiak, an open skin boat |

## steamer

| n | value | kind_note | reads as |
|---:|---|---|---|
| 3 | steamer |  | steamer |
| 1 | government steamer | government | steamer, government |
| 1 | naval gunboat | naval gunboat ◆ no warship code: a screw gunboat is filed as a steamer, the service in the note | steamer, naval gunboat |
| 1 | paddle steamer | paddle | steamer, paddle |
| 1 | revenue cutter | revenue cutter ◆ no cutter code: a steam revenue cutter is filed as a steamer, the service in the note | steamer, revenue cutter |
| 1 | screw steam tug, rebuilt | screw steam tug, rebuilt | steamer, screw steam tug, rebuilt |
| 1 | screw steamer | screw | steamer, screw |

## tender

| n | value | kind_note | reads as |
|---:|---|---|---|
| 2 | screw steam tender | screw steam | tender, screw steam |

## icebreaker

| n | value | kind_note | reads as |
|---:|---|---|---|
| 6 | icebreaker, Wind class | Wind class | icebreaker, Wind class |
| 3 | icebreaker |  | icebreaker |
| 1 | heavy icebreaker | heavy | icebreaker, heavy |
| 1 | heavy icebreaker, Polar class | heavy, Polar class | icebreaker, heavy, Polar class |
| 1 | icebreaker and polar research vessel | also a polar research vessel ◆ an icebreaker that also does science: coded by the hull, the science in the note | icebreaker, also a polar research vessel |
| 1 | medium icebreaker and research vessel, Arctic Class 3 | medium; research vessel, Arctic Class 3 ◆ an icebreaker that also does science: coded by the hull, the science in the note | icebreaker, medium; research vessel, Arctic Class 3 |
| 1 | steel screw semi-icebreaker | steel screw semi-icebreaker ◆ a semi-icebreaker: ice-strengthened rather than a true icebreaker, so the note keeps 'semi' | icebreaker, steel screw semi-icebreaker |

## submarine

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | nuclear submarine | nuclear | submarine, nuclear |
| 1 | nuclear submarine, Skate class | nuclear, Skate class | submarine, nuclear, Skate class |

## whaler

| n | value | kind_note | reads as |
|---:|---|---|---|
| 48 | whaler |  | whaler |
| 1 | whaler, converted | converted | whaler, converted |
| 1 | whaler, later a steam whaler | later a steam whaler | whaler, later a steam whaler |
| 1 | whaler, purchased into the Navy | purchased into the Navy | whaler, purchased into the Navy |
| 1 | whaler, strengthened for discovery service | strengthened for discovery service | whaler, strengthened for discovery service |

## steam-whaler

| n | value | kind_note | reads as |
|---:|---|---|---|
| 6 | steam whaler |  | steam whaler |
| 1 | steam whaler and sealer | also a sealer | steam whaler, also a sealer |

## sealer

| n | value | kind_note | reads as |
|---:|---|---|---|
| 6 | sealing steamer | steam | sealer, steam |
| 2 | sealing steamer, purchased by the United States Navy | steam, purchased by the United States Navy ◆ bought for the Greely relief and kept in government service; coded by the trade she was built for | sealer, steam, purchased by the United States Navy |
| 1 | motor sealer | motor | sealer, motor |
| 1 | steam sealer | steam | sealer, steam |
| 1 | steam sealer, converted | steam, converted | sealer, steam, converted |

## research-vessel

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | ice-strengthened research and supply vessel | ice-strengthened, also a supply vessel | research or survey vessel, ice-strengthened, also a supply vessel |
| 1 | research vessel, used for expedition cruising | used for expedition cruising | research or survey vessel, used for expedition cruising |
| 1 | survey ship |  ◆ a full-rigged naval ship employed on survey: coded by her work, not her rig | research or survey vessel |

## cruise-ship

| n | value | kind_note | reads as |
|---:|---|---|---|
| 3 | expedition cruise ship | expedition cruising | cruise ship, expedition cruising |
| 1 | cruise ship |  | cruise ship |

## transport

| n | value | kind_note | reads as |
|---:|---|---|---|
| 2 | storeship | storeship | transport or supply ship, storeship |
| 2 | transport |  | transport or supply ship |
| 1 | Hudson's Bay Company supply vessel | Hudson's Bay Company | transport or supply ship, Hudson's Bay Company |
| 1 | government supply and hospital ship | government hospital ship | transport or supply ship, government hospital ship |

## freighter

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | freighter |  | freighter |

## tanker

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | oil tanker, ice-strengthened | oil, ice-strengthened | tanker, oil, ice-strengthened |

## aircraft

| n | value | kind_note | reads as |
|---:|---|---|---|
| 1 | aircraft, Avro Lancaster | Avro Lancaster | aircraft, Avro Lancaster |
| 1 | aircraft, Avro Lancaster Mk X | Avro Lancaster Mk X | aircraft, Avro Lancaster Mk X |
| 1 | aircraft, Boeing B-29 | Boeing B-29 | aircraft, Boeing B-29 |
| 1 | aircraft, Canadair North Star | Canadair North Star | aircraft, Canadair North Star |
| 1 | aircraft, Consolidated Canso amphibian | Consolidated Canso amphibian | aircraft, Consolidated Canso amphibian |
| 1 | aircraft, Curtiss C-46 Commando | Curtiss C-46 Commando | aircraft, Curtiss C-46 Commando |
| 1 | aircraft, DHC-2 Beaver | DHC-2 Beaver | aircraft, DHC-2 Beaver |
| 1 | aircraft, DHC-3 Otter | DHC-3 Otter | aircraft, DHC-3 Otter |
| 1 | aircraft, DHC-6 Twin Otter | DHC-6 Twin Otter | aircraft, DHC-6 Twin Otter |
| 1 | aircraft, Douglas C-47 / Dakota | Douglas C-47 / Dakota | aircraft, Douglas C-47 / Dakota |
| 1 | aircraft, Fairchild C-119 | Fairchild C-119 | aircraft, Fairchild C-119 |
| 1 | aircraft, Fokker Universal | Fokker Universal | aircraft, Fokker Universal |
| 1 | aircraft, Lockheed CC-130 Hercules | Lockheed CC-130 Hercules | aircraft, Lockheed CC-130 Hercules |
| 1 | aircraft, Piper PA-18 Super Cub | Piper PA-18 Super Cub | aircraft, Piper PA-18 Super Cub |
| 1 | aircraft, de Havilland Moth | de Havilland Moth | aircraft, de Havilland Moth |

