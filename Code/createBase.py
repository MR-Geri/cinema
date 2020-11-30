def db_create(base):
    base.execute("""
                                       create table Cinemas
                                       (
                                           id    INTEGER not null
                                               primary key autoincrement
                                               unique,
                                           title STRING  not null
                                       );
                                       """)
    base.execute("""
                                       create table Halls
                                       (
                                           id         INTEGER not null
                                               constraint Halls_pk
                                                   primary key autoincrement,
                                           title      STRING  not null,
                                           cinema_id  INTEGER not null
                                               references Cinemas,
                                           rows       INTEGER not null,
                                           places_row INTEGER not null
                                       );
                                       """)
    base.execute("""create unique index Halls_id_uindex on Halls (id);""")
    base.execute("""
                                       create table Sessions
                                       (
                                           id       INTEGER not null
                                               primary key autoincrement
                                               unique,
                                           title    STRING  not null,
                                           hall_id  INTEGER not null
                                               references Halls,
                                           date     TEXT    not null,
                                           time     TEXT    not null,
                                           duration TEXT    not null,
                                           price    INTEGER default 0 not null
                                       );
                                       """)
    base.execute("""
                   create table Places
                   (
                       row        INTEGER not null,
                       place      INTEGER not null,
                       session_id INTEGER
                           references Sessions
                   );
                                       """)
