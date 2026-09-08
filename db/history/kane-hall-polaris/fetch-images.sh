#!/bin/bash
# Fetch queued Commons originals one at a time with long pauses (Commons 429s this address).
cd /data/dev/arctic-history || exit 1
fetch () {
  name="$1"; shift
  file="$1"; shift
  url="https://commons.wikimedia.org/wiki/Special:FilePath/${file}"
  echo "=== $name"
  python3 tools/history-fetch.py "$url" --topic kane-hall-polaris --name "$name"
  sleep 25
}
fetch kane-hall-polaris-hall-photo.jpg "Charles%20Francis%20Hall%20only%20known%20photo.jpg"
fetch kane-hall-polaris-ebierbing-tookoolito-tintype.png "Tintype%20of%20Ebierbing%20(Joe)%20and%20Tookoolito%20(Hannah).png"
fetch kane-hall-polaris-polaris-ship.jpg "Captain%20Hall's%20Arctic%20Expedition%20--%20The%20Polaris.jpg"
fetch kane-hall-polaris-hall-grave.jpg "Sciencerecordcom1874beac%200536%20The%20grave%20of%20Captain%20Hall.jpg"
fetch kane-hall-polaris-hall-funeral.jpg "The%20funeral%20of%20Captain%20Charles%20Francis%20Hall.jpg"
fetch kane-hall-polaris-hans-hendrik.jpg "Hans%20Hendrik%20(cropped).jpg"
fetch kane-hall-polaris-polaris-ice-drift.jpg "Polaris%20ice%20drift.jpg"
fetch kane-hall-polaris-kalutunah.jpg "Gordon%201907%20Round%20about%20the%20North%20Pole%200363%20Kalutunah.jpg"
fetch kane-hall-polaris-ebierbing-nourse.jpg "Ebierbing%20Nourse.jpg"
fetch kane-hall-polaris-tookoolito-nourse.jpg "Tookoolito%20Nourse.jpg"
fetch kane-hall-polaris-polaris-at-godhavn.jpg "The%20Polaris%20and%20Congress%20at%20Godhaven,%20Disco%20Island.jpg"
fetch kane-hall-polaris-life-in-the-brig.jpg "Life%20in%20the%20brig.jpg"
fetch kane-hall-polaris-budington-hall-tyson.jpg "Captain%20Sidney%20O.%20Budington,%20Charles%20Francis%20Hall,%20and%20George%20E.%20Tyson.jpg"
fetch kane-hall-polaris-polaris-crew.jpg "SS%20Polaris%20crew%20(cropped).jpg"
fetch kane-hall-polaris-hall-kodlunarn.png "Charles%20Francis%20Hall%20with%20Inuit%20on%20Kodlunarn%20Island,%20c.%201862.png"
fetch kane-hall-polaris-ebierbing-sealing.jpg "Ebierbing%20waiting%20a%20seal's%20%22blow%22%20(Life%20with%20the%20Esquimaux,%201864).jpg"
echo "=== DONE"
