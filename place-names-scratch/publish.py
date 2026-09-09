import subprocess,sqlite3
D='place-names-scratch/pages/'
PEOPLE={
'place-names-overview-northern-half':"William Edward Parry;Otto Sverdrup;Edward Belcher;Robert Edwin Peary;James White;Robert Dundas, 2nd Viscount Melville",
'place-names-inuit-and-inughuit-names-of-the-north':"Lynn Peplinski;Zipporah Ungalaq;Patrick Aqiattusuk;Qitdlarssuaq;Knud Rasmussen",
'place-names-parrys-names-1819-20':"William Edward Parry;Matthew Liddon;John Barrow;Robert Dundas, 2nd Viscount Melville",
'place-names-the-franklin-searchs-names':"Edward Belcher;William Penny;Sherard Osborn;George Frederick Mecham;Francis Leopold McClintock;George Henry Richards;Horatio Thomas Austin",
'place-names-sverdrups-norwegian-archipelago':"Otto Sverdrup;Ivar Fosheim;Per Schei;Victor Baumann;Axel Heiberg;Amund Ringnes;Ellef Ringnes",
'place-names-american-names-on-smith-sound-and-ellesmere':"Elisha Kent Kane;Isaac Israel Hayes;Charles Francis Hall;George Strong Nares;Adolphus Washington Greely;Robert Edwin Peary;Donald Baxter MacMillan",
'place-names-twentieth-century-names-in-the-queen-elizabeth-islands':"Joseph-Elzear Bernier;Vilhjalmur Stefansson;Storker Storkerson;Ole Andreasen;Harry Stallworthy;John Davidson Craig",
'place-names-what-nunavut-has-renamed':"Otto Sverdrup;Harry Stallworthy;Lynn Peplinski",
'place-names-the-inuit-names-of-the-south':"Franz Boas;Lynn Peplinski;Zipporah Ungalaq;Iligliuk;Ikmallik;Apelagliu",
'place-names-the-elizabethan-names':"Martin Frobisher;John Davis;Michael Lok;Christopher Hall;Charles Jackman;Anne Dudley, Countess of Warwick;William Sanderson",
'place-names-the-merchants-names':"Henry Hudson;Robert Bylot;William Baffin;Luke Foxe;John Wolstenholme;Dudley Digges;Thomas Button",
'place-names-whalers-and-the-company':"William Penny;Eenoolooapik;William Adams;Joseph-Elzear Bernier;William Hogarth",
'place-names-parry-and-ross':"William Edward Parry;John Ross;Iligliuk;Felix Booth;James Clark Ross;Ikmallik;Apelagliu",
'place-names-king-william-and-boothia':"James Clark Ross;Francis Leopold McClintock;John Franklin;Jane Franklin;Roald Amundsen;Louie Kamookak;Robert McClure",
'place-names-what-the-communities-are-called-now':"Solomon Malliki;Lorne Kusugak;Donald Havioyak;Peter Irniq",
'place-names-who-decides':"James White;John Davis;William Penny;Lynn Peplinski;Zipporah Ungalaq",
'place-names-the-greenland-shore':"John Davis;William Sanderson;Knud Rasmussen",
}
def publish(status='good', only=None):
    c=sqlite3.connect('file:db/history/history.sqlite?mode=ro',uri=True); c.row_factory=sqlite3.Row
    for r in c.execute("select * from pages where topic='place-names' order by ordering"):
        s=r['slug']
        if only and s not in only: continue
        cmd=['/usr/bin/python3','tools/history-db.py','page','--slug',s,'--title',r['title'],'--topic','place-names',
             '--summary',r['summary'],'--ordering',str(r['ordering']),'--file',D+s+'.md','--status',status]
        if PEOPLE.get(s): cmd += ['--people',PEOPLE[s]]
        p=subprocess.run(cmd,capture_output=True,text=True)
        print('%-3s %-60s %s %s' % (r['ordering'], s, p.returncode, (p.stdout+p.stderr).strip()[:120]))
