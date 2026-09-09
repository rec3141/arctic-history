import sys; sys.path.insert(0,'amundsen-gjoa-review-scratch')
from q import find
QS=[("obs finished","September 26th"),("hut 29th","September 29th"),("250 feet","250 feet"),
("sixty cases","sixty packing cases"),("Uranienborg","Uranienborg"),("2 Nov","November 2nd"),
("Potsdam","Potsdam"),("66 lbs","66 lbs"),("6 April 1904","April 6th"),("22 below","22"),
("Abva","Abva"),("Mount Matheson","Matheson"),("May 7","May 7th"),("Tasmania","Tasmania Islands"),
("Victoria Harbour","Victoria Harbour"),("May 21","May 21st"),("Kaumallo","Kaumallo"),("Kalakchie","Kalakchie"),
("eleven pounds","eleven pounds"),("May 27","May 27th"),("Booth Point","Booth Point"),
("Neumayer","Neumayer"),("Cape Nansen","Cape Nansen"),("thirteen","thirteen"),
("Charles Hanson","Charles Hanson"),("Charles Hansson","Charles Hansson"),
("McKenna","McKenna"),("Mogg","Mogg"),("Sten","Sten"),("Kataksina","Kataksina"),
("Manni","Manni"),("Herschel","Herschel"),("Anni","Anni"),("Frank N. Smith","Smith"),
("Uckermann","Uckermann"),("Horten","Horten"),("Fort McPherson","McPherson"),
("Nelson Head","Nelson Head"),("Eta","Eta"),("RGS Islands","Royal Geographical Society"),
]
for tag,text in QS:
    r=find(text,50)
    print(("OK  " if r else "MISS"),tag,"|", ", ".join(k for k,_,_ in r))
