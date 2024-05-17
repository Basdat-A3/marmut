-- AKUN
CREATE TABLE AKUN (
    email VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    gender INT NOT NULL,
    tempat_lahir VARCHAR(50) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    is_verified BOOLEAN NOT NULL,
    kota_asal VARCHAR(50) NOT NULL
);

-- PAKET
CREATE TABLE PAKET (
    jenis VARCHAR(50) PRIMARY KEY,
    harga INT NOT NULL
);

-- PREMIUM
CREATE TABLE PREMIUM (
    email VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (email) REFERENCES AKUN(email)
);

-- NON PREMIUM
CREATE TABLE NONPREMIUM (
    email VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (email) REFERENCES AKUN(email)
);

--TRANSACTION
CREATE TABLE TRANSACTION (
    id UUID PRIMARY KEY,
    jenis_paket VARCHAR(50),
    email VARCHAR(50),
    timestamp_dimulai TIMESTAMP NOT NULL,
    timestamp_berakhir TIMESTAMP NOT NULL,
    metode_bayar VARCHAR(50) NOT NULL,
    nominal INT NOT NULL,
    FOREIGN KEY (jenis_paket) REFERENCES PAKET(jenis),
    FOREIGN KEY (email) REFERENCES AKUN(email)
);


--KONTEN
CREATE TABLE KONTEN (
    id UUID PRIMARY KEY,
    judul VARCHAR(100) NOT NULL,
    tanggal_rilis DATE NOT NULL,
    tahun INT NOT NULL,
    durasi INT NOT NULL
);

--GENRE
CREATE TABLE GENRE (
    id_konten UUID REFERENCES KONTEN(id),
    genre VARCHAR(50),
    PRIMARY KEY (id_konten, genre)
);


--PODCASTER
CREATE TABLE PODCASTER (
    email VARCHAR(50) PRIMARY KEY REFERENCES AKUN(email)
);


--PODCAST
CREATE TABLE PODCAST (
    id_konten UUID PRIMARY KEY REFERENCES KONTEN(id),
    email_podcaster VARCHAR(50) REFERENCES PODCASTER(email)
);


--EPISODE
CREATE TABLE EPISODE (
    id_episode UUID PRIMARY KEY,
    id_konten_podcast UUID REFERENCES PODCAST(id_konten),
    judul VARCHAR(100) NOT NULL,
    deskripsi VARCHAR(500) NOT NULL,
    durasi INT NOT NULL,
    tanggal_rilis DATE NOT NULL
);

--Pemilik Hak Cipta
CREATE TABLE PEMILIK_HAK_CIPTA (
  id UUID PRIMARY KEY,
  rate_royalti INT NOT NULL
);

--ARTIST
CREATE TABLE ARTIST (
  id UUID PRIMARY KEY,
  email_akun VARCHAR(50),
  id_pemilik_hak_cipta UUID,
  FOREIGN KEY (email_akun) REFERENCES AKUN(email),
  FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id)
);

-- Songwriter
CREATE TABLE SONGWRITER (
  id UUID PRIMARY KEY,
  email_akun VARCHAR(50),
  id_pemilik_hak_cipta UUID,
  FOREIGN KEY (email_akun) REFERENCES AKUN(email),
  FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id)
);

--Label
CREATE TABLE LABEL (
  id UUID PRIMARY KEY,
  nama VARCHAR(100) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  kontak VARCHAR(50) NOT NULL,
  id_pemilik_hak_cipta UUID,
  FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id)
);

--Album
CREATE TABLE ALBUM (
  id UUID PRIMARY KEY,
  judul VARCHAR(100) NOT NULL,
  jumlah_lagu INT NOT NULL DEFAULT 0,
  id_label UUID NOT NULL,
  total_durasi INT NOT NULL DEFAULT 0,
  FOREIGN KEY (id_label) REFERENCES LABEL(id)
);


-- Song
CREATE TABLE SONG (
  id_konten UUID PRIMARY KEY,
  id_artist UUID NOT NULL,
  id_album UUID NOT NULL,
  total_play INT NOT NULL DEFAULT 0,
  total_download INT NOT NULL DEFAULT 0,
  FOREIGN KEY (id_konten) REFERENCES KONTEN(id),
  FOREIGN KEY (id_artist) REFERENCES ARTIST(id),
  FOREIGN KEY (id_album) REFERENCES ALBUM(id)
);

--Songwriter write song
CREATE TABLE SONGWRITER_WRITE_SONG (
    id_songwriter UUID,
    id_song UUID,
    PRIMARY KEY (id_songwriter, id_song),
    FOREIGN KEY (id_songwriter) REFERENCES SONGWRITER(id),
    FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);

-- DOWNLOADED_SONG
CREATE TABLE DOWNLOADED_SONG (
    id_song UUID,
    email_downloader VARCHAR(50),
    PRIMARY KEY (id_song, email_downloader),
    FOREIGN KEY (id_song) REFERENCES SONG(id_konten),
    FOREIGN KEY (email_downloader) REFERENCES PREMIUM(email)
);



--Playlist
CREATE TABLE PLAYLIST (
    id UUID PRIMARY KEY
);

--CHART
CREATE TABLE CHART (
    tipe VARCHAR(50) PRIMARY KEY,
    id_playlist UUID REFERENCES PLAYLIST(id)
);

--User Playlist
CREATE TABLE USER_PLAYLIST (
    email_pembuat VARCHAR(50) REFERENCES AKUN(email),
    id_user_playlist UUID,
    judul VARCHAR(100) NOT NULL,
    deskripsi VARCHAR(500) NOT NULL,
    jumlah_lagu INT NOT NULL,
    tanggal_dibuat DATE NOT NULL,
    id_playlist UUID REFERENCES PLAYLIST(id),
    total_durasi INT NOT NULL DEFAULT 0,
    PRIMARY KEY (email_pembuat, id_user_playlist)
);

--Royalti
CREATE TABLE ROYALTI (
  id_pemilik_hak_cipta UUID,
  id_song UUID,
  jumlah INT NOT NULL,
  PRIMARY KEY (id_pemilik_hak_cipta, id_song),
  FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES PEMILIK_HAK_CIPTA(id),
  FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);

--Akun play user playlist
CREATE TABLE AKUN_PLAY_USER_PLAYLIST (
    email_pemain VARCHAR(50),
    id_user_playlist UUID,
    email_pembuat VARCHAR(50),
    waktu TIMESTAMP,
    PRIMARY KEY (email_pemain, id_user_playlist, waktu),
    FOREIGN KEY (email_pemain) REFERENCES AKUN(email),
    FOREIGN KEY (id_user_playlist, email_pembuat) REFERENCES USER_PLAYLIST(id_user_playlist, email_pembuat)
);

--Akun play song
CREATE TABLE AKUN_PLAY_SONG (
    email_pemain VARCHAR(50),
    id_song UUID,
    waktu TIMESTAMP,
    PRIMARY KEY (email_pemain, id_song, waktu),
    FOREIGN KEY (email_pemain) REFERENCES AKUN(email),
    FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);

--Playlist song
CREATE TABLE PLAYLIST_SONG (
    id_playlist UUID,
    id_song UUID,
    PRIMARY KEY (id_playlist, id_song),
    FOREIGN KEY (id_playlist) REFERENCES PLAYLIST(id),
    FOREIGN KEY (id_song) REFERENCES SONG(id_konten)
);

INSERT INTO AKUN VALUES ('john.doe@example.com','secret123','John Doe',1.0,'New York City','1990-01-01 00:00:00','True','Los Angeles'),
	('jane.smith@outlook.com','securepass','Jane Smith',0.0,'London','1995-02-15 00:00:00','False','Paris'),
	('michael.lee@yahoo.com','passw0rd','Michael Lee',1.0,'Tokyo','1985-12-24 00:00:00','True','Berlin'),
	('sarah.jones@gmail.com','s@fep@ssw0rd','Sarah Jones',0.0,'Sydney','2000-05-07 00:00:00','False','Madrid'),
	('david.miller@protonmail.com','ilovesecurity','David Miller',1.0,'Toronto','1978-03-19 00:00:00','True','Rome'),
	('emily.garcia@hotmail.com','coffeelover','Emily Garcia',0.0,'Sao Paulo','1982-10-21 00:00:00','False','Amsterdam'),
	('william.davis@aol.com','teamplayer','William Davis',1.0,'Mumbai','1992-08-10 00:00:00','True','Stockholm'),
	('ashley.hernandez@icloud.com','alwayslearning','Ashley Hernandez',0.0,'Berlin','1987-06-04 00:00:00','False','Vienna'),
	('matthew.johnson@fastmail.com','bookworm','Matthew Johnson',1.0,'Singapore','1975-09-27 00:00:00','True','Prague'),
	('jennifer.lopez@riseup.net','travelholic','Jennifer Lopez',0.0,'Cape Town','2002-04-12 00:00:00','False','Budapest'),
	('daniel.williams@tutamail.com','musicfan','Daniel Williams',1.0,'Mexico City','1980-07-16 00:00:00','True','Warsaw'),
	('elizabeth.robinson@yandex.com','gamer','Elizabeth Robinson',0.0,'Melbourne','1998-01-31 00:00:00','False','Copenhagen'),
	('andrew.garcia@hushmail.com','artist@soul','Andrew Garcia',1.0,'Buenos Aires','1973-02-05 00:00:00','True','Helsinki'),
	('margaret.miller@tutanota.com','naturelover','Margaret Miller',0.0,'Beijing','1988-11-23 00:00:00','False','Oslo'),
	('christopher.thomas@posteo.net','techguru','Christopher Thomas',1.0,'Seoul','1970-05-18 00:00:00','True','Zurich'),
	('samantha.hernandez@disroot.org','fashionista','Samantha Hernandez',0.0,'Lagos','2001-12-14 00:00:00','False','Brussels'),
	('joseph.davis@countermail.com','foodie','Joseph Davis',1.0,'Cairo','1993-09-09 00:00:00','True','Dublin'),
	('katherine.johnson@mailbox.org','fitnessfreak','Katherine Johnson',0.0,'Milan','1986-03-22 00:00:00','False','Lisbon'),
	('robert.williams@runbox.com','scientist','Robert Williams',1.0,'Bangkok','1979-04-17 00:00:00','True','Athens'),
	('victoria.robinson@cock.li','entrepreneur','Victoria Robinson',0.0,'Kuala Lumpur','2003-11-01 00:00:00','False','Belgrade'),
	('david.garcia@aktivix.org','optimist','David Garcia',1.0,'Istanbul','1972-08-06 00:00:00','True','Bratislava'),
	('elizabeth.miller@riseup.net','dreamer','Elizabeth Miller',0.0,'Chennai','1985-02-20 00:00:00','False','Ljubljana'),
	('richard.thomas@tutanota.com','historybuff','Richard Thomas',1.0,'Jakarta','1981-06-25 00:00:00','True','Luxembourg'),
	('sarah.hernandez@disroot.org','musician','Sarah Hernandez',0.0,'Montreal','1999-01-10 00:00:00','False','Riga'),
	('james.davis@posteo.net','animallover','James Davis',1.0,'Delhi','1974-01-19 00:00:00','True','Vilnius'),
	('robert.williams@countermail.com','writer','Robert Williams',1.0,'Chicago','1976-12-28 00:00:00','True','Bern'),
	('victoria.robinson@runbox.com','coder','Victoria Robinson',0.0,'Dubai','2004-08-04 00:00:00','True','Bogor'),
	('alina.nguyen@protonmail.com','hopeful123','Alina Nguyen',0.0,'Hanoi','1997-07-03 00:00:00','True','Vancouver'),
	('omar.khan@riseup.net','cricketfan','Omar Khan',1.0,'Karachi','1984-01-26 00:00:00','False','Ottawa'),
	('elena.fernandez@posteo.net','bookclub','Elena Fernandez',0.0,'Madrid','1977-05-12 00:00:00','True','Rio de Janeiro'),
	('benjamin.schmidt@tutanota.com','cyclist','Benjamin Schmidt',1.0,'Berlin','1991-09-18 00:00:00','False','Tokyo'),
	('isabella.wang@yandex.com','artist','Isabella Wang',0.0,'Shanghai','2001-03-05 00:00:00','True','San Francisco'),
	('ethan.lee@disroot.org','gamerboy','Ethan Lee',1.0,'Hong Kong','1995-11-21 00:00:00','False','London'),
	('sophia.garcia@countermail.com','fashionista','Sophia Garcia',0.0,'Barcelona','2000-08-07 00:00:00','True','Milan'),
	('lucas.martin@mailbox.org','historybuff','Lucas Martin',1.0,'Paris','1983-02-14 00:00:00','False','New York City'),
	('charlotte.nguyen@cock.li','wanderlust','Charlotte Nguyen',0.0,'Ho Chi Minh City','1994-06-29 00:00:00','True','Sydney'),
	('adam.lee@aktivix.org','techie','Adam Lee',1.0,'Taipei','1989-12-10 00:00:00','False','Melbourne'),
	('chloe.fernandez@riseup.net','chef','Chloe Fernandez',0.0,'Buenos Aires','1979-10-24 00:00:00','True','Berlin'),
	('noah.schmidt@posteo.net','musician','Noah Schmidt',1.0,'Munich','1998-04-02 00:00:00','False','Chicago'),
	('olivia.wang@tutanota.com','naturelover','Olivia Wang',0.0,'Beijing','2002-02-08 00:00:00','True','Montreal'),
	('liam.lee@yandex.com','bookworm','Liam Lee',1.0,'Singapore','1990-08-20 00:00:00','False','Los Angeles'),
	('mia.garcia@disroot.org','yogaenthusiast','Mia Garcia',0.0,'Mexico City','1982-01-11 00:00:00','True','Rome'),
	('william.martin@countermail.com','entrepreneur','William Martin',1.0,'London','1976-07-17 00:00:00','False','Paris'),
	('ava.nguyen@mailbox.org','artist','Ava Nguyen',0.0,'Da Nang','1996-09-22 00:00:00','True','Tokyo'),
	('jacob.lee@cock.li','athlete','Jacob Lee',1.0,'Kuala Lumpur','1987-03-09 00:00:00','False','Berlin'),
	('sophia.fernandez@aktivix.org','veterinarian','Sophia Fernandez',0.0,'Santiago','1981-11-06 00:00:00','True','New York City'),
	('lucas.schmidt@riseup.net','pilot','Lucas Schmidt',1.0,'Hamburg','1992-05-15 00:00:00','False','Sydney'),
	('alexia.sasaki@tutanota.com','gamergirl','Alexia Sasaki',0.0,'Tokyo','2003-01-21 00:00:00','True','Amsterdam'),
	('omar.diaz@yandex.com','bookreader','Omar Diaz',1.0,'Havana','1980-06-04 00:00:00','False','Barcelona'),
	('evelyn.taylor@posteo.net','photographer','Evelyn Taylor',0.0,'New York City','1975-12-25 00:00:00','True','Dublin'),
	('gabriel.nguyen@disroot.org','techlover','Gabriel Nguyen',1.0,'Hanoi','1999-10-12 00:00:00','False','Los Angeles'),
	('clara.martin@countermail.com','architect','Clara Martin',0.0,'Rome','1985-04-08 00:00:00','True','Berlin');


INSERT INTO PAKET VALUES ('1 bulan',35000.0),
	('3 bulan',100000.0),
	('6 bulan',190000.0),
	('1 tahun',375000.0);

INSERT INTO PREMIUM VALUES ('james.davis@posteo.net'),
	('william.martin@countermail.com'),
	('sophia.garcia@countermail.com'),
	('samantha.hernandez@disroot.org'),
	('chloe.fernandez@riseup.net'),
	('andrew.garcia@hushmail.com'),
	('david.miller@protonmail.com'),
	('elizabeth.miller@riseup.net'),
	('william.davis@aol.com'),
	('matthew.johnson@fastmail.com');


INSERT INTO NONPREMIUM VALUES ('matthew.johnson@fastmail.com'),
	('jane.smith@outlook.com'),
	('adam.lee@aktivix.org'),
	('alexia.sasaki@tutanota.com'),
	('andrew.garcia@hushmail.com'),
	('david.miller@protonmail.com'),
	('benjamin.schmidt@tutanota.com'),
	('robert.williams@countermail.com'),
	('jacob.lee@cock.li'),
	('charlotte.nguyen@cock.li'),
	('lucas.schmidt@riseup.net'),
	('isabella.wang@yandex.com'),
	('sophia.garcia@countermail.com'),
	('john.doe@example.com'),
	('ashley.hernandez@icloud.com'),
	('liam.lee@yandex.com'),
	('david.garcia@aktivix.org'),
	('william.davis@aol.com'),
	('victoria.robinson@runbox.com'),
	('olivia.wang@tutanota.com'),
	('elizabeth.robinson@yandex.com'),
	('omar.khan@riseup.net'),
	('robert.williams@runbox.com'),
	('samantha.hernandez@disroot.org'),
	('elena.fernandez@posteo.net');



INSERT INTO TRANSACTION VALUES ('a366bb00-49ee-4024-8ee3-2b1e126643b7','3 bulan','andrew.garcia@hushmail.com','2024-04-25 01:09:58','2024-07-25 01:09:58','Transfer Bank',35000.0),
	('248a9e1e-edcd-4d48-8a32-e2d739a65aa4','3 bulan','robert.williams@countermail.com','2024-04-02 00:33:09','2024-07-02 00:33:09','Transfer Bank',375000.0),
	('38d9b34d-e958-45d8-85a5-82a8dff0df07','3 bulan','ava.nguyen@mailbox.org','2024-04-28 16:24:23','2024-07-28 16:24:23','OVO',100000.0),
	('0ef30206-7e44-4b95-89ca-02f2a622b417','6 bulan','chloe.fernandez@riseup.net','2024-04-25 18:53:52','2024-10-25 18:53:52','Transfer Bank',100000.0),
	('c3238dcf-5a23-4df9-884a-2137f2ae2daa','3 bulan','michael.lee@yahoo.com','2024-04-27 13:06:14','2024-07-27 13:06:14','OVO',35000.0),
	('568e6415-5cf2-4366-ac68-ebb6bd989244','1 tahun','gabriel.nguyen@disroot.org','2024-04-04 03:51:25','2025-04-04 03:51:25','OVO',190000.0),
	('1587d541-9b3c-48d4-87b6-0485cd85e202','3 bulan','noah.schmidt@posteo.net','2024-04-20 12:08:39','2024-07-20 12:08:39','OVO',375000.0),
	('b017b26e-22e2-4718-a662-7a3c6e16a003','6 bulan','matthew.johnson@fastmail.com','2024-04-13 20:31:51','2024-10-13 20:31:51','DANA',190000.0),
	('45b225dd-dee9-45db-aeab-ecd862a80973','1 tahun','lucas.martin@mailbox.org','2024-04-21 21:46:08','2025-04-21 21:46:08','DANA',375000.0),
	('f310e5b8-4ea3-4e98-8776-af8db239f5d7','1 tahun','john.doe@example.com','2024-04-12 05:43:22','2025-04-12 05:43:22','OVO',35000.0);

INSERT INTO KONTEN VALUES ('ac1fb9b0-08dc-41e1-b6e9-82b1e4d5fb90','Close The Mic','2001-03-15 00:00:00',2001.0,25.0),
	('91b2fd8d-f0b5-47e8-a7b9-4391ce11427d','Roe Jogan Podcast','2009-07-22 00:00:00',2009.0,34.0),
	('1a833dc6-5673-42e9-ba52-2cf60017c144','Podcast Warung Teh','2005-11-10 00:00:00',2005.0,30.0),
	('13bf5841-df0e-4720-8e35-432e9d22b2bd','Kick Marlo','2018-05-03 00:00:00',2018.0,28.0),
	('f08ec68b-34c3-4423-a5d3-cbf71a30dd6c','Podcast Topar','2003-09-28 00:00:00',2003.0,37.0),
	('ca6587f9-907c-416f-b422-ecd327d6a608','Ocean Breeze','2012-12-19 00:00:00',2012.0,3.0),
	('588c1c03-b771-4d7d-9948-f9ec8ac39c04','Sunshine Symphony','2015-04-07 00:00:00',2015.0,7.0),
	('d53b9c05-136e-4007-9527-64fc1765eac9','Lost in Melody','2010-08-25 00:00:00',2010.0,5.0),
	('5addeedf-da52-475d-b1cc-b987b6cecc2d','Firefly Waltz','2007-02-14 00:00:00',2007.0,4.0),
	('ef1e1d93-ab50-4a99-9f75-eaa4a02408ca','Serendipity Sonata','2002-10-31 00:00:00',2002.0,4.0),
	('926cc99b-201b-4ec2-8705-504ca2438664','Enchanted Dreams','2017-06-09 00:00:00',2017.0,8.0),
	('c554e84a-dc98-47e5-b604-d3db58b01ff9','Twilight Tango','2016-01-26 00:00:00',2016.0,7.0),
	('ca243463-e5bd-47f5-a156-e6cf734da889','Velvet Sky','2019-10-18 00:00:00',2019.0,4.0),
	('0d45673a-0f42-4b4c-be64-f493d2b29680','Crystal Clear','2008-06-02 00:00:00',2008.0,3.0),
	('c856ed0e-d74e-4b1f-b610-91183a20c2e3','Secret Garden','2011-09-05 00:00:00',2011.0,5.0),
	('223c9cb5-3d73-44d6-9fbb-3078176f590f','Aurora Lullaby','2006-07-31 00:00:00',2006.0,3.0),
	('77d83b03-c833-48d9-9fd7-713c648904db','River of Memories','2004-12-11 00:00:00',2004.0,4.0),
	('65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f','Eternal Embrace','2014-03-24 00:00:00',2014.0,8.0),
	('43234184-9da4-4211-a9ba-fe38b5c6e3e5','Radiant Reflections','2000-04-28 00:00:00',2000.0,7.0),
	('4e072859-dd24-4b43-8817-270a5cd97ed7','Moonlit Sonata','2013-08-13 00:00:00',2013.0,4.0),
	('40ec85b5-e3d4-464f-be7b-e5817f29657d','Whispering Willow','2018-02-08 00:00:00',2018.0,6.0),
	('056e0b9c-0f70-4489-a765-ba700c4ab3df','Golden Horizon','2010-11-30 00:00:00',2010.0,7.0),
	('0eb36cad-4b62-4d52-b135-c1cc54cbd1fb','Echoes of Eternity','2009-01-17 00:00:00',2009.0,6.0),
	('b529f128-98d7-47c4-846c-568ff1251058','Serenade of the Stars','2007-06-27 00:00:00',2007.0,6.0),
	('b006f49c-e12c-4078-a2e2-30213c6f73ab','Dancing Shadows','2006-10-04 00:00:00',2006.0,7.0),
	('0696f292-ff09-4143-b210-3a11a8d7b4a5','Misty Morning Melody','2016-09-01 00:00:00',2016.0,5.0),
	('03e313c1-4bbf-4f37-9cf6-0791ed78fb42','Enigma of the Night','2012-05-20 00:00:00',2012.0,7.0),
	('86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf','Serenity Call','2004-01-23 00:00:00',2004.0,4.0),
	('8de50413-f7a1-4eeb-a181-2588f9080b8f','Harmonic Horizon','2003-06-14 00:00:00',2003.0,5.0),
	('9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f','Celestial Symphony','2013-12-07 00:00:00',2013.0,4.0),
	('c6ca5238-0095-42a5-b065-099dc7737018','Whispers of Wonder','2001-08-09 00:00:00',2001.0,5.0),
	('2aea8119-67af-460b-9498-135a1075b04c','Melancholy Moonlight','2005-02-16 00:00:00',2005.0,7.0),
	('9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2','Dreamer Delight','2017-04-01 00:00:00',2017.0,6.0),
	('d78a5e84-93e1-4a3c-9d3d-216381f810ac','Ethereal Echoes','2002-12-25 00:00:00',2002.0,5.0),
	('9acbcc65-b371-4297-895b-ee80fb13c5b1','Siren Serenade','2015-11-02 00:00:00',2015.0,4.0),
	('7b8ba308-d499-417c-aa87-39b3e00f90a3','Enchanted Melodies','2019-01-30 00:00:00',2019.0,7.0),
	('b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c','Cascading Dreams','2008-09-21 00:00:00',2008.0,3.0),
	('5dba73f8-ff13-4a0b-8ab7-98b251fd1087','Serene Serenade','2011-03-12 00:00:00',2011.0,6.0),
	('30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4','Moonlit Mirage','2014-07-26 00:00:00',2014.0,8.0),
	('6d0f0dde-e082-4800-99c4-58701db8881c','Stardust Sonata','2020-10-07 00:00:00',2020.0,8.0),
	('2546000b-e257-47b8-b7ba-da787e024c41','Echoes of Eden','2000-08-04 00:00:00',2000.0,6.0),
	('44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc','Dancing Fireflies','2018-12-14 00:00:00',2018.0,5.0),
	('e58bf4b4-2277-4d8a-b43a-4009af7a29b1','Symphony of Silence','2013-05-06 00:00:00',2013.0,5.0),
	('dec44cc1-f24a-46be-adc0-24fe34f26d9e','Whispered Whimsy','2019-07-19 00:00:00',2019.0,3.0),
	('b5fffa7d-a1ca-44a4-9127-16cd706677f3','Enchanted Evening','2004-04-02 00:00:00',2004.0,8.0),
	('e2dc44cc-01bd-441c-8b11-a8b6aeabb3db','Midnight Reverie','2005-10-23 00:00:00',2005.0,8.0),
	('823c9948-1d10-45cf-a923-10be08f5511a','Oceanic Overture','2001-06-15 00:00:00',2001.0,4.0),
	('ea381cb5-9539-42fa-9015-fef196021ad8','Dreamcatcher Dance','2011-04-20 00:00:00',2011.0,6.0),
	('5f23eaad-140a-4d87-a914-db1fe945779d','Twilight Whispers','2003-11-08 00:00:00',2003.0,3.0),
	('53d50695-9c0c-41c8-aac3-89405899e8c4','Celestial Cascade','2010-02-05 00:00:00',2010.0,3.0),
	('46c41473-738a-42b0-bb08-0bbe9ea3b114','Aurora Anthem','2006-04-17 00:00:00',2006.0,7.0),
	('547ad9fb-9c7a-4b0a-889f-a897409ebf42','Symphony of Stardust','2008-01-01 00:00:00',2008.0,8.0),
	('249502b0-6eea-4469-b595-bdb33bc2eba0','Cosmic Carousel','2012-08-28 00:00:00',2012.0,6.0),
	('513f0176-d330-4278-8886-5c9195aabe93','Twilight Reverie','2009-10-10 00:00:00',2009.0,5.0),
	('fc5cf983-e28f-4614-b546-9345af86e2fe','Serenade of Solitude','2017-08-06 00:00:00',2017.0,3.0);

INSERT INTO GENRE VALUES ('ac1fb9b0-08dc-41e1-b6e9-82b1e4d5fb90','Technology'),
	('91b2fd8d-f0b5-47e8-a7b9-4391ce11427d','Education'),
	('1a833dc6-5673-42e9-ba52-2cf60017c144','Sports'),
	('13bf5841-df0e-4720-8e35-432e9d22b2bd','History'),
	('f08ec68b-34c3-4423-a5d3-cbf71a30dd6c','Comedy'),
	('ca6587f9-907c-416f-b422-ecd327d6a608','Pop'),
	('588c1c03-b771-4d7d-9948-f9ec8ac39c04','Rock'),
	('d53b9c05-136e-4007-9527-64fc1765eac9','Jazz'),
	('5addeedf-da52-475d-b1cc-b987b6cecc2d','Blues'),
	('ef1e1d93-ab50-4a99-9f75-eaa4a02408ca','Reggae'),
	('926cc99b-201b-4ec2-8705-504ca2438664','Country'),
	('c554e84a-dc98-47e5-b604-d3db58b01ff9','Rap'),
	('ca243463-e5bd-47f5-a156-e6cf734da889','Metal'),
	('0d45673a-0f42-4b4c-be64-f493d2b29680','Funk'),
	('c856ed0e-d74e-4b1f-b610-91183a20c2e3','Soul'),
	('223c9cb5-3d73-44d6-9fbb-3078176f590f','Pop'),
	('77d83b03-c833-48d9-9fd7-713c648904db','Rock'),
	('65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f','Jazz'),
	('43234184-9da4-4211-a9ba-fe38b5c6e3e5','Blues'),
	('4e072859-dd24-4b43-8817-270a5cd97ed7','Reggae'),
	('40ec85b5-e3d4-464f-be7b-e5817f29657d','Country'),
	('056e0b9c-0f70-4489-a765-ba700c4ab3df','Rap'),
	('0eb36cad-4b62-4d52-b135-c1cc54cbd1fb','Metal'),
	('b529f128-98d7-47c4-846c-568ff1251058','Funk'),
	('b006f49c-e12c-4078-a2e2-30213c6f73ab','Soul'),
	('0696f292-ff09-4143-b210-3a11a8d7b4a5','Pop'),
	('03e313c1-4bbf-4f37-9cf6-0791ed78fb42','Rock'),
	('86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf','Jazz'),
	('8de50413-f7a1-4eeb-a181-2588f9080b8f','Blues'),
	('9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f','Reggae'),
	('c6ca5238-0095-42a5-b065-099dc7737018','Country'),
	('2aea8119-67af-460b-9498-135a1075b04c','Rap'),
	('9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2','Metal'),
	('d78a5e84-93e1-4a3c-9d3d-216381f810ac','Funk'),
	('9acbcc65-b371-4297-895b-ee80fb13c5b1','Soul'),
	('7b8ba308-d499-417c-aa87-39b3e00f90a3','Pop'),
	('b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c','Rock'),
	('5dba73f8-ff13-4a0b-8ab7-98b251fd1087','Jazz'),
	('30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4','Blues'),
	('6d0f0dde-e082-4800-99c4-58701db8881c','Reggae'),
	('2546000b-e257-47b8-b7ba-da787e024c41','Country'),
	('44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc','Rap'),
	('e58bf4b4-2277-4d8a-b43a-4009af7a29b1','Metal'),
	('dec44cc1-f24a-46be-adc0-24fe34f26d9e','Funk'),
	('b5fffa7d-a1ca-44a4-9127-16cd706677f3','Soul'),
	('e2dc44cc-01bd-441c-8b11-a8b6aeabb3db','Pop'),
	('823c9948-1d10-45cf-a923-10be08f5511a','Rock'),
	('ea381cb5-9539-42fa-9015-fef196021ad8','Jazz'),
	('5f23eaad-140a-4d87-a914-db1fe945779d','Blues'),
	('53d50695-9c0c-41c8-aac3-89405899e8c4','Reggae'),
	('46c41473-738a-42b0-bb08-0bbe9ea3b114','Country'),
	('547ad9fb-9c7a-4b0a-889f-a897409ebf42','Rap'),
	('249502b0-6eea-4469-b595-bdb33bc2eba0','Metal'),
	('513f0176-d330-4278-8886-5c9195aabe93','Funk'),
	('fc5cf983-e28f-4614-b546-9345af86e2fe','Soul'),
	('46c41473-738a-42b0-bb08-0bbe9ea3b114','Pop'),
	('547ad9fb-9c7a-4b0a-889f-a897409ebf42','Rock'),
	('249502b0-6eea-4469-b595-bdb33bc2eba0','Jazz'),
	('ac1fb9b0-08dc-41e1-b6e9-82b1e4d5fb90','Comedy'),
	('91b2fd8d-f0b5-47e8-a7b9-4391ce11427d','Mystery');


INSERT INTO PODCASTER VALUES ('william.martin@countermail.com'),
	('ava.nguyen@mailbox.org'),
	('jacob.lee@cock.li'),
	('sophia.fernandez@aktivix.org'),
	('lucas.schmidt@riseup.net'),
	('alexia.sasaki@tutanota.com'),
	('omar.diaz@yandex.com'),
	('evelyn.taylor@posteo.net'),
	('gabriel.nguyen@disroot.org'),
	('clara.martin@countermail.com');

INSERT INTO PODCAST VALUES ('ac1fb9b0-08dc-41e1-b6e9-82b1e4d5fb90','alexia.sasaki@tutanota.com'),
	('91b2fd8d-f0b5-47e8-a7b9-4391ce11427d','omar.diaz@yandex.com'),
	('1a833dc6-5673-42e9-ba52-2cf60017c144','evelyn.taylor@posteo.net'),
	('13bf5841-df0e-4720-8e35-432e9d22b2bd','gabriel.nguyen@disroot.org'),
	('f08ec68b-34c3-4423-a5d3-cbf71a30dd6c','clara.martin@countermail.com');

INSERT INTO EPISODE VALUES ('25605e5a-ce53-4e7f-816b-0cf3008a1cdc','ac1fb9b0-08dc-41e1-b6e9-82b1e4d5fb90','Pesan Dedi','Dengarkan pesan mendalam dari Dedi dalam episode terbaru kami! Dari pengalaman hidup hingga cerita inspiratif, Dedi berbagi insight yang tak terduga.',13.0,'2001-03-15 00:00:00'),
	('bee8b56e-2176-4735-a2ea-ad3d1a54eec9','ac1fb9b0-08dc-41e1-b6e9-82b1e4d5fb90','Dedi Vidi Ngobrol','Jelajahi percakapan menarik antara Dedi dan Vidi dalam episode podcast kami yang penuh energi ini! Temukan sudut pandang unik mereka tentang berbagai topik yang menarik.',12.0,'2001-03-16 00:00:00'),
	('b7559267-1c80-4e13-9d59-2b30bbd576cf','91b2fd8d-f0b5-47e8-a7b9-4391ce11427d','RJE 1 with Melon Rusk','Tonton wawancara seru pertama kami dengan Melon Rusk di podcast RJE! Dari cerita inspiratif hingga tips praktis, episode ini akan menginspirasi dan menghibur Anda.',17.0,'2009-07-22 00:00:00'),
	('09f5641c-92e5-4068-9acb-3b156f9d4c13','91b2fd8d-f0b5-47e8-a7b9-4391ce11427d','RJE 2 with RDJ','Saksikan diskusi mendalam dengan RDJ dalam episode kedua podcast RJE kami! Jelajahi topik menarik dan dapatkan wawasan berharga dari tamu spesial kami.',17.0,'2009-07-23 00:00:00'),
	('562bd35e-d4b1-4ff9-bcce-97dac88ed87d','1a833dc6-5673-42e9-ba52-2cf60017c144','PKW 1 Rahasia Marlo','Dalam episode ini, kita mengungkap rahasia menarik tentang Marlo di podcast PKW! Saksikan dan temukan misteri yang menarik dalam pembicaraan kami.',15.0,'2005-11-10 00:00:00'),
	('af7f7173-4924-49c9-a81d-99aac07cda0e','1a833dc6-5673-42e9-ba52-2cf60017c144','PKW 2 Codered','Mari bahas keamanan digital dan kode merah dalam episode kedua podcast PKW kami! Temukan tips penting untuk melindungi diri Anda di dunia online.',15.0,'2005-11-11 00:00:00'),
	('22d9412d-d9a9-4c74-88ac-d368d9e01cd9','13bf5841-df0e-4720-8e35-432e9d22b2bd','Christmas tapi Horror','Nikmati suasana Natal dengan sentuhan horor dalam episode istimewa ini! Dari cerita seram hingga film-film Natal menakutkan, siapkan diri Anda untuk sensasi yang menegangkan.',14.0,'2018-05-03 00:00:00'),
	('2e66efe7-44c2-4859-9b40-d5ad45f4b3a1','13bf5841-df0e-4720-8e35-432e9d22b2bd','Pakar Cinta Tangsel','Dengarkan pandangan ahli tentang cinta dan hubungan dalam konteks Tangsel di episode podcast kami yang menarik ini! Dapatkan wawasan berharga untuk kehidupan asmara Anda.',14.0,'2018-05-04 00:00:00'),
	('2ea10936-5735-480c-a33b-6ba26c9020f8','f08ec68b-34c3-4423-a5d3-cbf71a30dd6c','Hasil Rapot 1','Lihat hasil rapot pertama kami dalam seri evaluasi kami! Temukan pencapaian dan tantangan dalam perjalanan kami menuju kesuksesan.',20.0,'2003-09-28 00:00:00'),
	('0297602a-8b6e-42b0-84da-da51b1e16fbc','f08ec68b-34c3-4423-a5d3-cbf71a30dd6c','Hasil Topar 2','Jelajahi hasil evaluasi kedua kami dalam episode podcast ini! Temukan perkembangan terbaru dan pelajaran berharga yang kami dapatkan dalam perjalanan kami.',17.0,'2003-09-29 00:00:00');

INSERT INTO PEMILIK_HAK_CIPTA VALUES ('772674b1-db75-4354-a51e-78de4d7c9e13',59.0),
	('0cb866dd-c813-498a-91fd-4278fe8c93e3',93.0),
	('1196655f-c498-4aa8-ae10-ee74793eb286',49.0),
	('4c21ba53-94e0-47b7-8276-dc315af335bb',9.0),
	('faf742f5-89f1-48a8-ab97-dde3e3aad785',36.0),
	('559e9f4e-b593-42ea-b972-e63d1fc9b8b9',20.0),
	('848ff684-694e-4d6c-82e3-4f7e66cf73e7',100.0),
	('475549e9-3788-4ace-88c2-33ad4ab20a51',7.0),
	('05c9e593-752d-4d6e-9ff0-45a1eb7f8933',65.0),
	('ec20d800-6bb8-4b44-a87e-56424c84c880',35.0),
	('0ef94c5c-22a2-465a-bbff-609c5b28e12f',39.0),
	('940c2b47-f81e-47e5-9bfd-6d3a1a2e1798',31.0),
	('99423623-c237-42c9-af64-eda3e19ec9d6',5.0),
	('ed6205c5-7ac0-4f4b-8767-a654567f75d5',40.0),
	('97275574-c016-4315-8ec8-e99a03e7bc25',31.0),
	('0482276b-e3f6-4866-a3f9-c69268090491',33.0),
	('f7573215-946c-4cfd-a44c-5e794feaa189',72.0),
	('5d230609-d9e6-4f57-932e-b041ba0d620d',7.0),
	('77f88810-71dd-4a93-aed5-6c0840dc3384',66.0),
	('b847fb4a-af70-4550-9262-8f655f3e8045',82.0),
	('3b89915d-4c4e-44f3-a69c-6b5915aec8ba',4.0),
	('2bcb6a1e-b931-4e04-ada5-2dd6385cf248',41.0),
	('a5554896-2e18-47e2-ab5f-de87f9c3bee6',95.0),
	('35caf18e-c66f-44e3-a8b2-1f3974b86f43',97.0),
	('98ddeffc-7018-4566-ab4c-d3988c461877',35.0);


INSERT INTO ARTIST VALUES ('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','john.doe@example.com','772674b1-db75-4354-a51e-78de4d7c9e13'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','jane.smith@outlook.com','0cb866dd-c813-498a-91fd-4278fe8c93e3'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','michael.lee@yahoo.com','1196655f-c498-4aa8-ae10-ee74793eb286'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','sarah.jones@gmail.com','4c21ba53-94e0-47b7-8276-dc315af335bb'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','david.miller@protonmail.com','faf742f5-89f1-48a8-ab97-dde3e3aad785'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','emily.garcia@hotmail.com','559e9f4e-b593-42ea-b972-e63d1fc9b8b9'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','william.davis@aol.com','848ff684-694e-4d6c-82e3-4f7e66cf73e7'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','ashley.hernandez@icloud.com','475549e9-3788-4ace-88c2-33ad4ab20a51'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','matthew.johnson@fastmail.com','05c9e593-752d-4d6e-9ff0-45a1eb7f8933'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','jennifer.lopez@riseup.net','ec20d800-6bb8-4b44-a87e-56424c84c880');

INSERT INTO SONGWRITER VALUES ('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','john.doe@example.com','772674b1-db75-4354-a51e-78de4d7c9e13'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','jane.smith@outlook.com','0cb866dd-c813-498a-91fd-4278fe8c93e3'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','michael.lee@yahoo.com','1196655f-c498-4aa8-ae10-ee74793eb286'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','sarah.jones@gmail.com','4c21ba53-94e0-47b7-8276-dc315af335bb'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','david.miller@protonmail.com','faf742f5-89f1-48a8-ab97-dde3e3aad785'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','emily.garcia@hotmail.com','559e9f4e-b593-42ea-b972-e63d1fc9b8b9'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','william.davis@aol.com','848ff684-694e-4d6c-82e3-4f7e66cf73e7'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','ashley.hernandez@icloud.com','475549e9-3788-4ace-88c2-33ad4ab20a51'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','matthew.johnson@fastmail.com','05c9e593-752d-4d6e-9ff0-45a1eb7f8933'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','jennifer.lopez@riseup.net','ec20d800-6bb8-4b44-a87e-56424c84c880');

INSERT INTO LABEL VALUES ('034033a4-fedd-4d5b-9936-296a7d0e89c1','Harmony Records','harmonyrecords@gmail.com','basdatTeka33',12345678901,'772674b1-db75-4354-a51e-78de4d7c9e13'),
	('10b93da8-320e-413e-a21f-d4765c81e238','Sonic Beats','sonicbeats@gmail.com','basdatTeka34',12345678902,'848ff684-694e-4d6c-82e3-4f7e66cf73e7'),
	('5618ecbc-ebfa-402b-b0a2-6c79d4a77547','Melodic Sphere','melodicsphere@gmail.com','basdatTeka35',12345678903,'475549e9-3788-4ace-88c2-33ad4ab20a51'),
	('3a783de5-9555-4b14-b1d3-f0726e31bcf9','Rhythm Ethos ','rhythmethos@gmail.com','basdatTeka36',12345678904,'05c9e593-752d-4d6e-9ff0-45a1eb7f8933'),
	('b01b0ae4-a026-4a38-bdb7-a6ce4ff139dd','Quantum Eclipse ','quantumeclipse@gmail.com','basdatTeka37',12345678905,'ec20d800-6bb8-4b44-a87e-56424c84c880');

INSERT INTO ALBUM VALUES ('3b8a104e-c7f3-46fb-b539-6c14f26b7892','Echoes of Twilight',11.0,'034033a4-fedd-4d5b-9936-296a7d0e89c1',30.0),
	('48f5190b-4376-4cb7-80b6-f00343ead876','Horizon Tides',10.0,'10b93da8-320e-413e-a21f-d4765c81e238',34.0),
	('b8b11832-845e-4a98-b6e0-c9ba077470ca','Whispers of the Ancients',8.0,'5618ecbc-ebfa-402b-b0a2-6c79d4a77547',32.0),
	('9b7fbe33-73a4-4fe6-86f7-a7601ef6baea','Celestial Journeys',5.0,'3a783de5-9555-4b14-b1d3-f0726e31bcf9',17.0),
	('d5114437-8d91-4447-ad28-a1b182f13310','Rhythms of the Wild',8.0,'b01b0ae4-a026-4a38-bdb7-a6ce4ff139dd',38.0);



INSERT INTO SONG VALUES ('ca6587f9-907c-416f-b422-ecd327d6a608','c88a5789-170d-4e11-ba22-28556b34cd90','d5114437-8d91-4447-ad28-a1b182f13310',7309.0,1483.0),
	('588c1c03-b771-4d7d-9948-f9ec8ac39c04','f371c60a-c35a-4985-bfa9-01e42c671077','b8b11832-845e-4a98-b6e0-c9ba077470ca',3488.0,4191.0),
	('d53b9c05-136e-4007-9527-64fc1765eac9','097347af-29b3-44c1-b8f1-180b0fdc2e98','d5114437-8d91-4447-ad28-a1b182f13310',6635.0,4654.0),
	('5addeedf-da52-475d-b1cc-b987b6cecc2d','b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','3b8a104e-c7f3-46fb-b539-6c14f26b7892',2729.0,1936.0),
	('ef1e1d93-ab50-4a99-9f75-eaa4a02408ca','1b92522e-be80-4717-9ee0-c727d87eae71','3b8a104e-c7f3-46fb-b539-6c14f26b7892',9010.0,3277.0),
	('926cc99b-201b-4ec2-8705-504ca2438664','77c690b9-1191-409c-814d-69d26daeb4d3','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',9400.0,1171.0),
	('c554e84a-dc98-47e5-b604-d3db58b01ff9','cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','b8b11832-845e-4a98-b6e0-c9ba077470ca',2810.0,3372.0),
	('ca243463-e5bd-47f5-a156-e6cf734da889','076eb8ab-6575-42f9-a782-c4e0105b2025','3b8a104e-c7f3-46fb-b539-6c14f26b7892',2681.0,411.0),
	('0d45673a-0f42-4b4c-be64-f493d2b29680','f371c60a-c35a-4985-bfa9-01e42c671077','d5114437-8d91-4447-ad28-a1b182f13310',1306.0,3727.0),
	('c856ed0e-d74e-4b1f-b610-91183a20c2e3','c88a5789-170d-4e11-ba22-28556b34cd90','3b8a104e-c7f3-46fb-b539-6c14f26b7892',5927.0,4416.0),
	('223c9cb5-3d73-44d6-9fbb-3078176f590f','c88a5789-170d-4e11-ba22-28556b34cd90','48f5190b-4376-4cb7-80b6-f00343ead876',8817.0,223.0),
	('77d83b03-c833-48d9-9fd7-713c648904db','77c690b9-1191-409c-814d-69d26daeb4d3','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',7673.0,725.0),
	('65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f','6e5b9403-2ede-48c0-bf95-76b841d1de51','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',6882.0,1386.0),
	('43234184-9da4-4211-a9ba-fe38b5c6e3e5','77c690b9-1191-409c-814d-69d26daeb4d3','b8b11832-845e-4a98-b6e0-c9ba077470ca',794.0,629.0),
	('4e072859-dd24-4b43-8817-270a5cd97ed7','097347af-29b3-44c1-b8f1-180b0fdc2e98','b8b11832-845e-4a98-b6e0-c9ba077470ca',3772.0,3870.0),
	('40ec85b5-e3d4-464f-be7b-e5817f29657d','6e5b9403-2ede-48c0-bf95-76b841d1de51','3b8a104e-c7f3-46fb-b539-6c14f26b7892',3673.0,730.0),
	('056e0b9c-0f70-4489-a765-ba700c4ab3df','77c690b9-1191-409c-814d-69d26daeb4d3','d5114437-8d91-4447-ad28-a1b182f13310',6480.0,1000.0),
	('0eb36cad-4b62-4d52-b135-c1cc54cbd1fb','f371c60a-c35a-4985-bfa9-01e42c671077','d5114437-8d91-4447-ad28-a1b182f13310',3151.0,25.0),
	('b529f128-98d7-47c4-846c-568ff1251058','bfcba729-ebc2-4128-8402-ffa9dd21d133','3b8a104e-c7f3-46fb-b539-6c14f26b7892',7015.0,3933.0),
	('b006f49c-e12c-4078-a2e2-30213c6f73ab','77c690b9-1191-409c-814d-69d26daeb4d3','d5114437-8d91-4447-ad28-a1b182f13310',7663.0,3701.0),
	('0696f292-ff09-4143-b210-3a11a8d7b4a5','f371c60a-c35a-4985-bfa9-01e42c671077','3b8a104e-c7f3-46fb-b539-6c14f26b7892',6833.0,1727.0),
	('03e313c1-4bbf-4f37-9cf6-0791ed78fb42','bfcba729-ebc2-4128-8402-ffa9dd21d133','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',5874.0,1960.0),
	('86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf','6e5b9403-2ede-48c0-bf95-76b841d1de51','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',1477.0,4736.0),
	('8de50413-f7a1-4eeb-a181-2588f9080b8f','097347af-29b3-44c1-b8f1-180b0fdc2e98','48f5190b-4376-4cb7-80b6-f00343ead876',6056.0,1643.0),
	('9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f','b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',1232.0,849.0),
	('c6ca5238-0095-42a5-b065-099dc7737018','1b92522e-be80-4717-9ee0-c727d87eae71','b8b11832-845e-4a98-b6e0-c9ba077470ca',6274.0,2183.0),
	('2aea8119-67af-460b-9498-135a1075b04c','bfcba729-ebc2-4128-8402-ffa9dd21d133','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',4627.0,4627.0),
	('9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2','77c690b9-1191-409c-814d-69d26daeb4d3','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',9836.0,2000.0),
	('d78a5e84-93e1-4a3c-9d3d-216381f810ac','cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','3b8a104e-c7f3-46fb-b539-6c14f26b7892',4800.0,605.0),
	('9acbcc65-b371-4297-895b-ee80fb13c5b1','f371c60a-c35a-4985-bfa9-01e42c671077','3b8a104e-c7f3-46fb-b539-6c14f26b7892',7450.0,4008.0),
	('7b8ba308-d499-417c-aa87-39b3e00f90a3','bfcba729-ebc2-4128-8402-ffa9dd21d133','3b8a104e-c7f3-46fb-b539-6c14f26b7892',6386.0,3119.0),
	('b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c','cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',9634.0,527.0),
	('5dba73f8-ff13-4a0b-8ab7-98b251fd1087','097347af-29b3-44c1-b8f1-180b0fdc2e98','48f5190b-4376-4cb7-80b6-f00343ead876',5099.0,2922.0),
	('30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4','77c690b9-1191-409c-814d-69d26daeb4d3','d5114437-8d91-4447-ad28-a1b182f13310',124.0,432.0),
	('6d0f0dde-e082-4800-99c4-58701db8881c','6e5b9403-2ede-48c0-bf95-76b841d1de51','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',8909.0,2097.0),
	('2546000b-e257-47b8-b7ba-da787e024c41','097347af-29b3-44c1-b8f1-180b0fdc2e98','d5114437-8d91-4447-ad28-a1b182f13310',2208.0,822.0),
	('44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc','076eb8ab-6575-42f9-a782-c4e0105b2025','48f5190b-4376-4cb7-80b6-f00343ead876',4773.0,896.0),
	('e58bf4b4-2277-4d8a-b43a-4009af7a29b1','6e5b9403-2ede-48c0-bf95-76b841d1de51','48f5190b-4376-4cb7-80b6-f00343ead876',2871.0,3802.0),
	('dec44cc1-f24a-46be-adc0-24fe34f26d9e','1b92522e-be80-4717-9ee0-c727d87eae71','3b8a104e-c7f3-46fb-b539-6c14f26b7892',6891.0,4149.0),
	('b5fffa7d-a1ca-44a4-9127-16cd706677f3','076eb8ab-6575-42f9-a782-c4e0105b2025','3b8a104e-c7f3-46fb-b539-6c14f26b7892',2551.0,3719.0),
	('e2dc44cc-01bd-441c-8b11-a8b6aeabb3db','77c690b9-1191-409c-814d-69d26daeb4d3','b8b11832-845e-4a98-b6e0-c9ba077470ca',4533.0,2596.0),
	('823c9948-1d10-45cf-a923-10be08f5511a','097347af-29b3-44c1-b8f1-180b0fdc2e98','48f5190b-4376-4cb7-80b6-f00343ead876',9748.0,2864.0),
	('ea381cb5-9539-42fa-9015-fef196021ad8','076eb8ab-6575-42f9-a782-c4e0105b2025','48f5190b-4376-4cb7-80b6-f00343ead876',3118.0,2398.0),
	('5f23eaad-140a-4d87-a914-db1fe945779d','b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','b8b11832-845e-4a98-b6e0-c9ba077470ca',6523.0,256.0),
	('53d50695-9c0c-41c8-aac3-89405899e8c4','6e5b9403-2ede-48c0-bf95-76b841d1de51','3b8a104e-c7f3-46fb-b539-6c14f26b7892',3379.0,3148.0),
	('46c41473-738a-42b0-bb08-0bbe9ea3b114','77c690b9-1191-409c-814d-69d26daeb4d3','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',5260.0,1232.0),
	('547ad9fb-9c7a-4b0a-889f-a897409ebf42','b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','48f5190b-4376-4cb7-80b6-f00343ead876',608.0,4449.0),
	('249502b0-6eea-4469-b595-bdb33bc2eba0','c88a5789-170d-4e11-ba22-28556b34cd90','b8b11832-845e-4a98-b6e0-c9ba077470ca',4008.0,4244.0),
	('513f0176-d330-4278-8886-5c9195aabe93','b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','3b8a104e-c7f3-46fb-b539-6c14f26b7892',1277.0,1555.0),
	('fc5cf983-e28f-4614-b546-9345af86e2fe','6e5b9403-2ede-48c0-bf95-76b841d1de51','9b7fbe33-73a4-4fe6-86f7-a7601ef6baea',2499.0,92.0);


INSERT INTO SONGWRITER_WRITE_SONG VALUES ('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','ca6587f9-907c-416f-b422-ecd327d6a608'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','588c1c03-b771-4d7d-9948-f9ec8ac39c04'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','d53b9c05-136e-4007-9527-64fc1765eac9'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','5addeedf-da52-475d-b1cc-b987b6cecc2d'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','ef1e1d93-ab50-4a99-9f75-eaa4a02408ca'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','926cc99b-201b-4ec2-8705-504ca2438664'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','c554e84a-dc98-47e5-b604-d3db58b01ff9'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','ca243463-e5bd-47f5-a156-e6cf734da889'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','0d45673a-0f42-4b4c-be64-f493d2b29680'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','c856ed0e-d74e-4b1f-b610-91183a20c2e3'),
	('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','223c9cb5-3d73-44d6-9fbb-3078176f590f'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','77d83b03-c833-48d9-9fd7-713c648904db'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','43234184-9da4-4211-a9ba-fe38b5c6e3e5'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','4e072859-dd24-4b43-8817-270a5cd97ed7'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','40ec85b5-e3d4-464f-be7b-e5817f29657d'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','056e0b9c-0f70-4489-a765-ba700c4ab3df'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','0eb36cad-4b62-4d52-b135-c1cc54cbd1fb'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','b529f128-98d7-47c4-846c-568ff1251058'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','b006f49c-e12c-4078-a2e2-30213c6f73ab'),
	('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','0696f292-ff09-4143-b210-3a11a8d7b4a5'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','03e313c1-4bbf-4f37-9cf6-0791ed78fb42'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','8de50413-f7a1-4eeb-a181-2588f9080b8f'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','c6ca5238-0095-42a5-b065-099dc7737018'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','2aea8119-67af-460b-9498-135a1075b04c'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','d78a5e84-93e1-4a3c-9d3d-216381f810ac'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','9acbcc65-b371-4297-895b-ee80fb13c5b1'),
	('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','7b8ba308-d499-417c-aa87-39b3e00f90a3'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','5dba73f8-ff13-4a0b-8ab7-98b251fd1087'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','6d0f0dde-e082-4800-99c4-58701db8881c'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','2546000b-e257-47b8-b7ba-da787e024c41'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','e58bf4b4-2277-4d8a-b43a-4009af7a29b1'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','dec44cc1-f24a-46be-adc0-24fe34f26d9e'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','b5fffa7d-a1ca-44a4-9127-16cd706677f3'),
	('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','e2dc44cc-01bd-441c-8b11-a8b6aeabb3db'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','823c9948-1d10-45cf-a923-10be08f5511a'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','ea381cb5-9539-42fa-9015-fef196021ad8'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','5f23eaad-140a-4d87-a914-db1fe945779d'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','53d50695-9c0c-41c8-aac3-89405899e8c4'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','46c41473-738a-42b0-bb08-0bbe9ea3b114'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','547ad9fb-9c7a-4b0a-889f-a897409ebf42'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','249502b0-6eea-4469-b595-bdb33bc2eba0'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','513f0176-d330-4278-8886-5c9195aabe93'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','fc5cf983-e28f-4614-b546-9345af86e2fe'),
	('cd2f84a3-45b7-445f-bb0b-5d1a9ef9a20e','53d50695-9c0c-41c8-aac3-89405899e8c4'),
	('b9f10c1e-e250-4cbd-ac4a-ee7f7c937ff9','46c41473-738a-42b0-bb08-0bbe9ea3b114'),
	('77c690b9-1191-409c-814d-69d26daeb4d3','547ad9fb-9c7a-4b0a-889f-a897409ebf42'),
	('076eb8ab-6575-42f9-a782-c4e0105b2025','249502b0-6eea-4469-b595-bdb33bc2eba0'),
	('f371c60a-c35a-4985-bfa9-01e42c671077','513f0176-d330-4278-8886-5c9195aabe93'),
	('c88a5789-170d-4e11-ba22-28556b34cd90','fc5cf983-e28f-4614-b546-9345af86e2fe'),
	('1b92522e-be80-4717-9ee0-c727d87eae71','e2dc44cc-01bd-441c-8b11-a8b6aeabb3db'),
	('097347af-29b3-44c1-b8f1-180b0fdc2e98','823c9948-1d10-45cf-a923-10be08f5511a'),
	('6e5b9403-2ede-48c0-bf95-76b841d1de51','ea381cb5-9539-42fa-9015-fef196021ad8'),
	('bfcba729-ebc2-4128-8402-ffa9dd21d133','5f23eaad-140a-4d87-a914-db1fe945779d');


INSERT INTO DOWNLOADED_SONG VALUES ('056e0b9c-0f70-4489-a765-ba700c4ab3df','james.davis@posteo.net'),
	('9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2','william.martin@countermail.com'),
	('77d83b03-c833-48d9-9fd7-713c648904db','william.martin@countermail.com'),
	('ea381cb5-9539-42fa-9015-fef196021ad8','william.martin@countermail.com'),
	('ef1e1d93-ab50-4a99-9f75-eaa4a02408ca','sophia.garcia@countermail.com'),
	('dec44cc1-f24a-46be-adc0-24fe34f26d9e','sophia.garcia@countermail.com'),
	('03e313c1-4bbf-4f37-9cf6-0791ed78fb42','samantha.hernandez@disroot.org'),
	('9acbcc65-b371-4297-895b-ee80fb13c5b1','chloe.fernandez@riseup.net'),
	('e2dc44cc-01bd-441c-8b11-a8b6aeabb3db','andrew.garcia@hushmail.com'),
	('9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f','david.miller@protonmail.com');



INSERT INTO PLAYLIST VALUES ('123e4567-e89b-12d3-a456-426614174000'),
    ('123e4567-e89b-12d3-a456-426614174001'),
    ('123e4567-e89b-12d3-a456-426614174002'),
    ('123e4567-e89b-12d3-a456-426614174003'),
    ('123e4567-e89b-12d3-a456-426614174004'),
    ('123e4567-e89b-12d3-a456-426614174005'),
    ('123e4567-e89b-12d3-a456-426614174006'),
    ('123e4567-e89b-12d3-a456-426614174007'),
    ('123e4567-e89b-12d3-a456-426614174008'),
    ('123e4567-e89b-12d3-a456-426614174009'),
    ('123e4567-e89b-12d3-a456-426614174010'),
    ('123e4567-e89b-12d3-a456-426614174011'),
    ('123e4567-e89b-12d3-a456-426614174012'),
    ('123e4567-e89b-12d3-a456-426614174013'),
    ('123e4567-e89b-12d3-a456-426614174014'),
    ('123e4567-e89b-12d3-a456-426614174015');

INSERT INTO CHART VALUES ('Daily Top 20', '123e4567-e89b-12d3-a456-426614174012'),
    ('Weekly Top 20', '123e4567-e89b-12d3-a456-426614174013'),
    ('Monthly Top 20', '123e4567-e89b-12d3-a456-426614174014'),
    ('Yearly Top 20', '123e4567-e89b-12d3-a456-426614174015');

INSERT INTO USER_PLAYLIST VALUES ('john.doe@example.com','aaaaaaaa-bbbb-cccc-dddd-111111111111','My Favorites','Playlist lagu favorit saya',10.0,'2024-04-26 00:00:00','123e4567-e89b-12d3-a456-426614174000',210.0),
	('jane.smith@outlook.com','aaaaaaaa-bbbb-cccc-dddd-111111111112','Workout Mix','Playlist untuk berolahraga',15.0,'2024-04-13 00:00:00','123e4567-e89b-12d3-a456-426614174001',135.0),
	('michael.lee@yahoo.com','aaaaaaaa-bbbb-cccc-dddd-111111111113','Road Trip Tunes','Playlist untuk perjalanan',20.0,'2024-04-04 00:00:00','123e4567-e89b-12d3-a456-426614174002',110.0),
	('sarah.jones@gmail.com','aaaaaaaa-bbbb-cccc-dddd-111111111114','Study Session Sounds','Playlist untuk belajar',35.0,'2024-04-27 00:00:00','123e4567-e89b-12d3-a456-426614174003',120.0),
	('david.miller@protonmail.com','aaaaaaaa-bbbb-cccc-dddd-111111111115','Relaxing Vibes','Playlist untuk santai',22.0,'2024-04-09 00:00:00','123e4567-e89b-12d3-a456-426614174004',95.0),
	('ashley.hernandez@icloud.com','aaaaaaaa-bbbb-cccc-dddd-111111111116','Rock and Roll','Playlist untuk latihan gitar',8.0,'2024-04-15 00:00:00','123e4567-e89b-12d3-a456-426614174005',133.0);

INSERT INTO ROYALTI VALUES ('772674b1-db75-4354-a51e-78de4d7c9e13','ca6587f9-907c-416f-b422-ecd327d6a608',3256.0),
	('0cb866dd-c813-498a-91fd-4278fe8c93e3','588c1c03-b771-4d7d-9948-f9ec8ac39c04',6217.0),
	('1196655f-c498-4aa8-ae10-ee74793eb286','e58bf4b4-2277-4d8a-b43a-4009af7a29b1',5435.0),
	('4c21ba53-94e0-47b7-8276-dc315af335bb','dec44cc1-f24a-46be-adc0-24fe34f26d9e',2078.0),
	('faf742f5-89f1-48a8-ab97-dde3e3aad785','ef1e1d93-ab50-4a99-9f75-eaa4a02408ca',9960.0),
	('559e9f4e-b593-42ea-b972-e63d1fc9b8b9','926cc99b-201b-4ec2-8705-504ca2438664',9845.0),
	('848ff684-694e-4d6c-82e3-4f7e66cf73e7','b5fffa7d-a1ca-44a4-9127-16cd706677f3',4087.0),
	('475549e9-3788-4ace-88c2-33ad4ab20a51','e2dc44cc-01bd-441c-8b11-a8b6aeabb3db',9274.0),
	('05c9e593-752d-4d6e-9ff0-45a1eb7f8933','823c9948-1d10-45cf-a923-10be08f5511a',8251.0),
	('ec20d800-6bb8-4b44-a87e-56424c84c880','c856ed0e-d74e-4b1f-b610-91183a20c2e3',5973.0),
	('0ef94c5c-22a2-465a-bbff-609c5b28e12f','223c9cb5-3d73-44d6-9fbb-3078176f590f',1085.0),
	('940c2b47-f81e-47e5-9bfd-6d3a1a2e1798','77d83b03-c833-48d9-9fd7-713c648904db',5524.0),
	('99423623-c237-42c9-af64-eda3e19ec9d6','65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f',4625.0),
	('ed6205c5-7ac0-4f4b-8767-a654567f75d5','43234184-9da4-4211-a9ba-fe38b5c6e3e5',1501.0),
	('97275574-c016-4315-8ec8-e99a03e7bc25','4e072859-dd24-4b43-8817-270a5cd97ed7',9076.0),
	('0482276b-e3f6-4866-a3f9-c69268090491','40ec85b5-e3d4-464f-be7b-e5817f29657d',8649.0),
	('f7573215-946c-4cfd-a44c-5e794feaa189','056e0b9c-0f70-4489-a765-ba700c4ab3df',5589.0),
	('5d230609-d9e6-4f57-932e-b041ba0d620d','0eb36cad-4b62-4d52-b135-c1cc54cbd1fb',2475.0),
	('77f88810-71dd-4a93-aed5-6c0840dc3384','b529f128-98d7-47c4-846c-568ff1251058',4951.0),
	('b847fb4a-af70-4550-9262-8f655f3e8045','b006f49c-e12c-4078-a2e2-30213c6f73ab',4253.0),
	('3b89915d-4c4e-44f3-a69c-6b5915aec8ba','547ad9fb-9c7a-4b0a-889f-a897409ebf42',5617.0),
	('2bcb6a1e-b931-4e04-ada5-2dd6385cf248','249502b0-6eea-4469-b595-bdb33bc2eba0',128.0),
	('a5554896-2e18-47e2-ab5f-de87f9c3bee6','513f0176-d330-4278-8886-5c9195aabe93',8522.0),
	('35caf18e-c66f-44e3-a8b2-1f3974b86f43','fc5cf983-e28f-4614-b546-9345af86e2fe',8963.0),
	('98ddeffc-7018-4566-ab4c-d3988c461877','9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f',3770.0);



INSERT INTO AKUN_PLAY_USER_PLAYLIST VALUES ('john.doe@example.com','aaaaaaaa-bbbb-cccc-dddd-111111111111','john.doe@example.com','2024-04-11 18:20:00'),
	('jane.smith@outlook.com','aaaaaaaa-bbbb-cccc-dddd-111111111112','jane.smith@outlook.com','2024-04-12 10:30:00'),
	('michael.lee@yahoo.com','aaaaaaaa-bbbb-cccc-dddd-111111111113','michael.lee@yahoo.com','2024-04-13 12:15:00'),
	('sarah.jones@gmail.com','aaaaaaaa-bbbb-cccc-dddd-111111111114','sarah.jones@gmail.com','2024-04-14 14:20:00'),
	('david.miller@protonmail.com','aaaaaaaa-bbbb-cccc-dddd-111111111115','david.miller@protonmail.com','2024-04-15 16:22:00'),
	('ashley.hernandez@icloud.com','aaaaaaaa-bbbb-cccc-dddd-111111111116','ashley.hernandez@icloud.com','2024-04-16 18:00:00'),
	('daniel.williams@tutamail.com','aaaaaaaa-bbbb-cccc-dddd-111111111111','john.doe@example.com','2024-04-12 11:45:00'),
	('elizabeth.robinson@yandex.com','aaaaaaaa-bbbb-cccc-dddd-111111111112','jane.smith@outlook.com','2024-04-13 14:10:00'),
	('andrew.garcia@hushmail.com','aaaaaaaa-bbbb-cccc-dddd-111111111113','michael.lee@yahoo.com','2024-04-14 17:00:00'),
	('margaret.miller@tutanota.com','aaaaaaaa-bbbb-cccc-dddd-111111111114','sarah.jones@gmail.com','2024-04-15 13:30:00'),
	('christopher.thomas@posteo.net','aaaaaaaa-bbbb-cccc-dddd-111111111115','david.miller@protonmail.com','2024-04-16 10:40:00'),
	('samantha.hernandez@disroot.org','aaaaaaaa-bbbb-cccc-dddd-111111111116','ashley.hernandez@icloud.com','2024-04-13 16:05:00'),
	('joseph.davis@countermail.com','aaaaaaaa-bbbb-cccc-dddd-111111111111','john.doe@example.com','2024-04-14 18:45:00'),
	('katherine.johnson@mailbox.org','aaaaaaaa-bbbb-cccc-dddd-111111111112','jane.smith@outlook.com','2024-04-15 11:00:00'),
	('robert.williams@runbox.com','aaaaaaaa-bbbb-cccc-dddd-111111111113','michael.lee@yahoo.com','2024-04-16 15:15:00'),
	('victoria.robinson@cock.li','aaaaaaaa-bbbb-cccc-dddd-111111111114','sarah.jones@gmail.com','2024-04-17 12:12:00'),
	('david.garcia@aktivix.org','aaaaaaaa-bbbb-cccc-dddd-111111111115','david.miller@protonmail.com','2024-04-14 10:10:00'),
	('elena.fernandez@posteo.net','aaaaaaaa-bbbb-cccc-dddd-111111111116','ashley.hernandez@icloud.com','2024-04-15 13:13:00'),
	('benjamin.schmidt@tutanota.com','aaaaaaaa-bbbb-cccc-dddd-111111111111','john.doe@example.com','2024-04-16 20:00:00'),
	('isabella.wang@yandex.com','aaaaaaaa-bbbb-cccc-dddd-111111111112','jane.smith@outlook.com','2024-04-17 19:30:00');




INSERT INTO AKUN_PLAY_SONG VALUES ('john.doe@example.com','ca6587f9-907c-416f-b422-ecd327d6a608','2024-01-01 08:15:23'),
	('jane.smith@outlook.com','588c1c03-b771-4d7d-9948-f9ec8ac39c04','2024-01-02 14:30:45'),
	('michael.lee@yahoo.com','d53b9c05-136e-4007-9527-64fc1765eac9','2024-01-03 20:45:12'),
	('sarah.jones@gmail.com','5addeedf-da52-475d-b1cc-b987b6cecc2d','2024-01-04 03:10:55'),
	('david.miller@protonmail.com','ef1e1d93-ab50-4a99-9f75-eaa4a02408ca','2024-01-05 09:25:33'),
	('emily.garcia@hotmail.com','926cc99b-201b-4ec2-8705-504ca2438664','2024-01-06 15:40:21'),
	('william.davis@aol.com','c554e84a-dc98-47e5-b604-d3db58b01ff9','2024-01-07 21:55:47'),
	('ashley.hernandez@icloud.com','ca243463-e5bd-47f5-a156-e6cf734da889','2024-01-08 04:20:09'),
	('matthew.johnson@fastmail.com','0d45673a-0f42-4b4c-be64-f493d2b29680','2024-01-09 10:35:17'),
	('jennifer.lopez@riseup.net','c856ed0e-d74e-4b1f-b610-91183a20c2e3','2024-01-10 16:50:28'),
	('daniel.williams@tutamail.com','223c9cb5-3d73-44d6-9fbb-3078176f590f','2024-01-11 23:05:36'),
	('elizabeth.robinson@yandex.com','77d83b03-c833-48d9-9fd7-713c648904db','2024-01-12 05:30:44'),
	('andrew.garcia@hushmail.com','65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f','2024-01-13 11:45:55'),
	('margaret.miller@tutanota.com','43234184-9da4-4211-a9ba-fe38b5c6e3e5','2024-01-14 18:00:22'),
	('christopher.thomas@posteo.net','4e072859-dd24-4b43-8817-270a5cd97ed7','2024-01-15 00:15:33'),
	('samantha.hernandez@disroot.org','40ec85b5-e3d4-464f-be7b-e5817f29657d','2024-01-16 06:30:41'),
	('joseph.davis@countermail.com','056e0b9c-0f70-4489-a765-ba700c4ab3df','2024-01-17 12:45:59'),
	('katherine.johnson@mailbox.org','0eb36cad-4b62-4d52-b135-c1cc54cbd1fb','2024-01-18 19:00:15'),
	('robert.williams@runbox.com','b529f128-98d7-47c4-846c-568ff1251058','2024-01-19 01:15:27'),
	('victoria.robinson@cock.li','b006f49c-e12c-4078-a2e2-30213c6f73ab','2024-01-20 07:30:33'),
	('david.garcia@aktivix.org','0696f292-ff09-4143-b210-3a11a8d7b4a5','2024-01-21 13:45:42'),
	('elizabeth.miller@riseup.net','03e313c1-4bbf-4f37-9cf6-0791ed78fb42','2024-01-22 20:00:58'),
	('richard.thomas@tutanota.com','86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf','2024-01-23 02:16:11'),
	('sarah.hernandez@disroot.org','8de50413-f7a1-4eeb-a181-2588f9080b8f','2024-01-24 08:31:29'),
	('james.davis@posteo.net','9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f','2024-01-25 14:46:37'),
	('robert.williams@countermail.com','c6ca5238-0095-42a5-b065-099dc7737018','2024-01-26 21:01:48'),
	('victoria.robinson@runbox.com','2aea8119-67af-460b-9498-135a1075b04c','2024-01-27 03:17:55'),
	('alina.nguyen@protonmail.com','9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2','2024-01-28 09:33:04'),
	('omar.khan@riseup.net','d78a5e84-93e1-4a3c-9d3d-216381f810ac','2024-01-29 15:48:22'),
	('elena.fernandez@posteo.net','9acbcc65-b371-4297-895b-ee80fb13c5b1','2024-01-30 22:03:36'),
	('benjamin.schmidt@tutanota.com','7b8ba308-d499-417c-aa87-39b3e00f90a3','2024-01-31 04:18:45'),
	('isabella.wang@yandex.com','b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c','2024-02-01 10:33:53'),
	('ethan.lee@disroot.org','5dba73f8-ff13-4a0b-8ab7-98b251fd1087','2024-02-02 16:49:01'),
	('sophia.garcia@countermail.com','30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4','2024-02-03 23:04:19'),
	('lucas.martin@mailbox.org','6d0f0dde-e082-4800-99c4-58701db8881c','2024-02-04 05:19:27'),
	('charlotte.nguyen@cock.li','2546000b-e257-47b8-b7ba-da787e024c41','2024-02-05 11:34:35'),
	('adam.lee@aktivix.org','44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc','2024-02-06 17:49:44'),
	('chloe.fernandez@riseup.net','e58bf4b4-2277-4d8a-b43a-4009af7a29b1','2024-02-07 00:04:53'),
	('noah.schmidt@posteo.net','dec44cc1-f24a-46be-adc0-24fe34f26d9e','2024-02-08 06:20:01'),
	('olivia.wang@tutanota.com','b5fffa7d-a1ca-44a4-9127-16cd706677f3','2024-02-09 12:35:19'),
	('liam.lee@yandex.com','e2dc44cc-01bd-441c-8b11-a8b6aeabb3db','2024-02-10 18:50:26'),
	('mia.garcia@disroot.org','823c9948-1d10-45cf-a923-10be08f5511a','2024-02-11 01:05:37'),
	('william.martin@countermail.com','ea381cb5-9539-42fa-9015-fef196021ad8','2024-02-12 07:20:45'),
	('ava.nguyen@mailbox.org','5f23eaad-140a-4d87-a914-db1fe945779d','2024-02-13 13:35:53'),
	('jacob.lee@cock.li','53d50695-9c0c-41c8-aac3-89405899e8c4','2024-02-14 19:51:02'),
	('sophia.fernandez@aktivix.org','46c41473-738a-42b0-bb08-0bbe9ea3b114','2024-02-15 02:06:11'),
	('lucas.schmidt@riseup.net','547ad9fb-9c7a-4b0a-889f-a897409ebf42','2024-02-16 08:21:29'),
	('alexia.sasaki@tutanota.com','249502b0-6eea-4469-b595-bdb33bc2eba0','2024-02-17 14:36:38'),
	('omar.diaz@yandex.com','513f0176-d330-4278-8886-5c9195aabe93','2024-02-18 20:51:46'),
	('evelyn.taylor@posteo.net','fc5cf983-e28f-4614-b546-9345af86e2fe','2024-02-19 03:06:55'),
	('gabriel.nguyen@disroot.org','ca6587f9-907c-416f-b422-ecd327d6a608','2024-02-20 09:22:03'),
	('clara.martin@countermail.com','588c1c03-b771-4d7d-9948-f9ec8ac39c04','2024-02-21 15:37:11'),
	('john.doe@example.com','d53b9c05-136e-4007-9527-64fc1765eac9','2024-02-22 21:52:20'),
	('jane.smith@outlook.com','5addeedf-da52-475d-b1cc-b987b6cecc2d','2024-02-23 04:07:29'),
	('michael.lee@yahoo.com','ef1e1d93-ab50-4a99-9f75-eaa4a02408ca','2024-02-24 10:22:37'),
	('sarah.jones@gmail.com','926cc99b-201b-4ec2-8705-504ca2438664','2024-02-25 16:37:45'),
	('david.miller@protonmail.com','c554e84a-dc98-47e5-b604-d3db58b01ff9','2024-02-26 22:52:54'),
	('emily.garcia@hotmail.com','ca243463-e5bd-47f5-a156-e6cf734da889','2024-02-27 05:08:03'),
	('william.davis@aol.com','0d45673a-0f42-4b4c-be64-f493d2b29680','2024-02-28 11:23:11'),
	('ashley.hernandez@icloud.com','c856ed0e-d74e-4b1f-b610-91183a20c2e3','2024-02-29 17:38:19'),
	('matthew.johnson@fastmail.com','223c9cb5-3d73-44d6-9fbb-3078176f590f','2024-03-01 23:53:28'),
	('jennifer.lopez@riseup.net','77d83b03-c833-48d9-9fd7-713c648904db','2024-03-02 06:08:36'),
	('daniel.williams@tutamail.com','65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f','2024-03-03 12:23:45'),
	('elizabeth.robinson@yandex.com','43234184-9da4-4211-a9ba-fe38b5c6e3e5','2024-03-04 18:38:54'),
	('andrew.garcia@hushmail.com','4e072859-dd24-4b43-8817-270a5cd97ed7','2024-03-05 00:54:02'),
	('margaret.miller@tutanota.com','40ec85b5-e3d4-464f-be7b-e5817f29657d','2024-03-06 07:09:11'),
	('christopher.thomas@posteo.net','056e0b9c-0f70-4489-a765-ba700c4ab3df','2024-03-07 13:24:19'),
	('samantha.hernandez@disroot.org','0eb36cad-4b62-4d52-b135-c1cc54cbd1fb','2024-03-08 19:39:27'),
	('joseph.davis@countermail.com','b529f128-98d7-47c4-846c-568ff1251058','2024-03-09 01:54:36'),
	('katherine.johnson@mailbox.org','b006f49c-e12c-4078-a2e2-30213c6f73ab','2024-03-10 08:09:44'),
	('robert.williams@runbox.com','0696f292-ff09-4143-b210-3a11a8d7b4a5','2024-03-11 14:24:53'),
	('victoria.robinson@cock.li','03e313c1-4bbf-4f37-9cf6-0791ed78fb42','2024-03-12 20:40:02'),
	('david.garcia@aktivix.org','86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf','2024-03-13 02:55:11'),
	('elizabeth.miller@riseup.net','8de50413-f7a1-4eeb-a181-2588f9080b8f','2024-03-14 09:10:19'),
	('richard.thomas@tutanota.com','9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f','2024-03-15 15:25:28'),
	('sarah.hernandez@disroot.org','c6ca5238-0095-42a5-b065-099dc7737018','2024-03-16 21:40:36'),
	('james.davis@posteo.net','2aea8119-67af-460b-9498-135a1075b04c','2024-03-17 03:55:45'),
	('robert.williams@countermail.com','9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2','2024-03-18 10:10:53'),
	('victoria.robinson@runbox.com','d78a5e84-93e1-4a3c-9d3d-216381f810ac','2024-03-19 16:26:02'),
	('alina.nguyen@protonmail.com','9acbcc65-b371-4297-895b-ee80fb13c5b1','2024-03-20 22:41:11'),
	('omar.khan@riseup.net','7b8ba308-d499-417c-aa87-39b3e00f90a3','2024-03-21 04:56:19'),
	('elena.fernandez@posteo.net','b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c','2024-03-22 11:11:28'),
	('benjamin.schmidt@tutanota.com','5dba73f8-ff13-4a0b-8ab7-98b251fd1087','2024-03-23 17:26:36'),
	('isabella.wang@yandex.com','30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4','2024-03-24 23:41:45'),
	('ethan.lee@disroot.org','6d0f0dde-e082-4800-99c4-58701db8881c','2024-03-25 05:56:54'),
	('sophia.garcia@countermail.com','2546000b-e257-47b8-b7ba-da787e024c41','2024-03-26 12:12:02'),
	('lucas.martin@mailbox.org','44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc','2024-03-27 18:27:11'),
	('charlotte.nguyen@cock.li','e58bf4b4-2277-4d8a-b43a-4009af7a29b1','2024-03-28 00:42:19'),
	('adam.lee@aktivix.org','dec44cc1-f24a-46be-adc0-24fe34f26d9e','2024-03-29 06:57:28'),
	('chloe.fernandez@riseup.net','b5fffa7d-a1ca-44a4-9127-16cd706677f3','2024-03-30 13:12:36'),
	('noah.schmidt@posteo.net','e2dc44cc-01bd-441c-8b11-a8b6aeabb3db','2024-03-31 19:27:45'),
	('olivia.wang@tutanota.com','823c9948-1d10-45cf-a923-10be08f5511a','2024-04-01 01:42:53'),
	('liam.lee@yandex.com','ea381cb5-9539-42fa-9015-fef196021ad8','2024-04-02 07:58:02'),
	('mia.garcia@disroot.org','5f23eaad-140a-4d87-a914-db1fe945779d','2024-04-03 14:13:11'),
	('william.martin@countermail.com','53d50695-9c0c-41c8-aac3-89405899e8c4','2024-04-04 20:28:19'),
	('ava.nguyen@mailbox.org','46c41473-738a-42b0-bb08-0bbe9ea3b114','2024-04-05 02:43:28'),
	('jacob.lee@cock.li','547ad9fb-9c7a-4b0a-889f-a897409ebf42','2024-04-06 09:58:36'),
	('sophia.fernandez@aktivix.org','249502b0-6eea-4469-b595-bdb33bc2eba0','2024-04-07 16:13:45'),
	('lucas.schmidt@riseup.net','513f0176-d330-4278-8886-5c9195aabe93','2024-04-08 22:28:54'),
	('alexia.sasaki@tutanota.com','fc5cf983-e28f-4614-b546-9345af86e2fe','2024-04-09 04:44:02'),
	('omar.diaz@yandex.com','5f23eaad-140a-4d87-a914-db1fe945779d','2024-04-10 10:59:11'),
	('evelyn.taylor@posteo.net','53d50695-9c0c-41c8-aac3-89405899e8c4','2024-04-11 17:14:19'),
	('gabriel.nguyen@disroot.org','46c41473-738a-42b0-bb08-0bbe9ea3b114','2024-04-12 23:29:28'),
	('clara.martin@countermail.com','547ad9fb-9c7a-4b0a-889f-a897409ebf42','2024-04-13 05:44:36');



INSERT INTO PLAYLIST_SONG VALUES ('123e4567-e89b-12d3-a456-426614174000','ca6587f9-907c-416f-b422-ecd327d6a608'),
	('123e4567-e89b-12d3-a456-426614174001','588c1c03-b771-4d7d-9948-f9ec8ac39c04'),
	('123e4567-e89b-12d3-a456-426614174002','d53b9c05-136e-4007-9527-64fc1765eac9'),
	('123e4567-e89b-12d3-a456-426614174003','5addeedf-da52-475d-b1cc-b987b6cecc2d'),
	('123e4567-e89b-12d3-a456-426614174004','ef1e1d93-ab50-4a99-9f75-eaa4a02408ca'),
	('123e4567-e89b-12d3-a456-426614174005','926cc99b-201b-4ec2-8705-504ca2438664'),
	('123e4567-e89b-12d3-a456-426614174006','c554e84a-dc98-47e5-b604-d3db58b01ff9'),
	('123e4567-e89b-12d3-a456-426614174007','ca243463-e5bd-47f5-a156-e6cf734da889'),
	('123e4567-e89b-12d3-a456-426614174008','0d45673a-0f42-4b4c-be64-f493d2b29680'),
	('123e4567-e89b-12d3-a456-426614174009','c856ed0e-d74e-4b1f-b610-91183a20c2e3'),
	('123e4567-e89b-12d3-a456-426614174010','223c9cb5-3d73-44d6-9fbb-3078176f590f'),
	('123e4567-e89b-12d3-a456-426614174000','77d83b03-c833-48d9-9fd7-713c648904db'),
	('123e4567-e89b-12d3-a456-426614174001','65b4d2ad-0d71-4c0c-908d-9a2e4b997c6f'),
	('123e4567-e89b-12d3-a456-426614174002','43234184-9da4-4211-a9ba-fe38b5c6e3e5'),
	('123e4567-e89b-12d3-a456-426614174003','4e072859-dd24-4b43-8817-270a5cd97ed7'),
	('123e4567-e89b-12d3-a456-426614174004','40ec85b5-e3d4-464f-be7b-e5817f29657d'),
	('123e4567-e89b-12d3-a456-426614174005','056e0b9c-0f70-4489-a765-ba700c4ab3df'),
	('123e4567-e89b-12d3-a456-426614174006','0eb36cad-4b62-4d52-b135-c1cc54cbd1fb'),
	('123e4567-e89b-12d3-a456-426614174007','b529f128-98d7-47c4-846c-568ff1251058'),
	('123e4567-e89b-12d3-a456-426614174008','b006f49c-e12c-4078-a2e2-30213c6f73ab'),
	('123e4567-e89b-12d3-a456-426614174009','0696f292-ff09-4143-b210-3a11a8d7b4a5'),
	('123e4567-e89b-12d3-a456-426614174010','03e313c1-4bbf-4f37-9cf6-0791ed78fb42'),
	('123e4567-e89b-12d3-a456-426614174000','86c2c020-32ce-4cb6-8fd0-3dba9fcb3fcf'),
	('123e4567-e89b-12d3-a456-426614174001','8de50413-f7a1-4eeb-a181-2588f9080b8f'),
	('123e4567-e89b-12d3-a456-426614174002','9cdb1d8a-944b-4465-8c3a-8ec7ea427e1f'),
	('123e4567-e89b-12d3-a456-426614174003','c6ca5238-0095-42a5-b065-099dc7737018'),
	('123e4567-e89b-12d3-a456-426614174004','2aea8119-67af-460b-9498-135a1075b04c'),
	('123e4567-e89b-12d3-a456-426614174005','9bc30b6b-f0d6-4871-9bfb-2dd7e762b0f2'),
	('123e4567-e89b-12d3-a456-426614174006','d78a5e84-93e1-4a3c-9d3d-216381f810ac'),
	('123e4567-e89b-12d3-a456-426614174007','9acbcc65-b371-4297-895b-ee80fb13c5b1'),
	('123e4567-e89b-12d3-a456-426614174008','7b8ba308-d499-417c-aa87-39b3e00f90a3'),
	('123e4567-e89b-12d3-a456-426614174009','b0fe0d76-a1ba-4f03-9951-8f62f9bceb5c'),
	('123e4567-e89b-12d3-a456-426614174010','5dba73f8-ff13-4a0b-8ab7-98b251fd1087'),
	('123e4567-e89b-12d3-a456-426614174000','30dba82a-d6f4-4bbc-b6ce-dc0796e00cd4'),
	('123e4567-e89b-12d3-a456-426614174001','6d0f0dde-e082-4800-99c4-58701db8881c'),
	('123e4567-e89b-12d3-a456-426614174002','2546000b-e257-47b8-b7ba-da787e024c41'),
	('123e4567-e89b-12d3-a456-426614174003','44dd020d-e1f1-47b8-960f-b8d0e9e0f4bc'),
	('123e4567-e89b-12d3-a456-426614174004','e58bf4b4-2277-4d8a-b43a-4009af7a29b1'),
	('123e4567-e89b-12d3-a456-426614174005','dec44cc1-f24a-46be-adc0-24fe34f26d9e'),
	('123e4567-e89b-12d3-a456-426614174006','b5fffa7d-a1ca-44a4-9127-16cd706677f3'),
	('123e4567-e89b-12d3-a456-426614174007','e2dc44cc-01bd-441c-8b11-a8b6aeabb3db'),
	('123e4567-e89b-12d3-a456-426614174008','823c9948-1d10-45cf-a923-10be08f5511a'),
	('123e4567-e89b-12d3-a456-426614174009','ea381cb5-9539-42fa-9015-fef196021ad8'),
	('123e4567-e89b-12d3-a456-426614174010','5f23eaad-140a-4d87-a914-db1fe945779d'),
	('123e4567-e89b-12d3-a456-426614174000','53d50695-9c0c-41c8-aac3-89405899e8c4'),
	('123e4567-e89b-12d3-a456-426614174001','46c41473-738a-42b0-bb08-0bbe9ea3b114'),
	('123e4567-e89b-12d3-a456-426614174002','547ad9fb-9c7a-4b0a-889f-a897409ebf42'),
	('123e4567-e89b-12d3-a456-426614174003','249502b0-6eea-4469-b595-bdb33bc2eba0'),
	('123e4567-e89b-12d3-a456-426614174004','513f0176-d330-4278-8886-5c9195aabe93'),
	('123e4567-e89b-12d3-a456-426614174005','fc5cf983-e28f-4614-b546-9345af86e2fe'),
	('123e4567-e89b-12d3-a456-426614174006','46c41473-738a-42b0-bb08-0bbe9ea3b114'),
	('123e4567-e89b-12d3-a456-426614174007','547ad9fb-9c7a-4b0a-889f-a897409ebf42'),
	('123e4567-e89b-12d3-a456-426614174008','249502b0-6eea-4469-b595-bdb33bc2eba0'),
	('123e4567-e89b-12d3-a456-426614174009','513f0176-d330-4278-8886-5c9195aabe93'),
	('123e4567-e89b-12d3-a456-426614174010','fc5cf983-e28f-4614-b546-9345af86e2fe');
