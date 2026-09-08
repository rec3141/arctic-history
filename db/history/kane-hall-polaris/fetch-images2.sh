#!/bin/bash
# Second pass, much slower (Commons 429s this shared campus address hard).
cd /data/dev/arctic-history || exit 1
fetch () {
  name="$1"; file="$2"
  if [ -f "db/history/kane-hall-polaris/files/$name" ]; then echo "=== $name already have"; return; fi
  echo "=== $name"
  python3 tools/history-fetch.py "https://commons.wikimedia.org/wiki/Special:FilePath/${file}" --topic kane-hall-polaris --name "$name"
  sleep 90
}
fetch kane-hall-polaris-kalutunah.jpg "Gordon%201907%20Round%20about%20the%20North%20Pole%200363%20Kalutunah.jpg"
fetch kane-hall-polaris-ebierbing-nourse.jpg "Ebierbing%20Nourse.jpg"
fetch kane-hall-polaris-tookoolito-nourse.jpg "Tookoolito%20Nourse.jpg"
fetch kane-hall-polaris-polaris-at-godhavn.jpg "The%20Polaris%20and%20Congress%20at%20Godhaven,%20Disco%20Island.jpg"
fetch kane-hall-polaris-life-in-the-brig.jpg "Life%20in%20the%20brig.jpg"
fetch kane-hall-polaris-budington-hall-tyson.jpg "Captain%20Sidney%20O.%20Budington,%20Charles%20Francis%20Hall,%20and%20George%20E.%20Tyson.jpg"
fetch kane-hall-polaris-polaris-crew.jpg "SS%20Polaris%20crew%20(cropped).jpg"
fetch kane-hall-polaris-hall-kodlunarn.png "Charles%20Francis%20Hall%20with%20Inuit%20on%20Kodlunarn%20Island,%20c.%201862.png"
fetch kane-hall-polaris-ebierbing-sealing.jpg "Ebierbing%20waiting%20a%20seal's%20%22blow%22%20(Life%20with%20the%20Esquimaux,%201864).jpg"
fetch kane-hall-polaris-ship-in-ice.jpg "-Ship%20in%20Ice,%20Greenland%20Expedition-%20MET%20DP116744.jpg"
echo "=== DONE"
