create table disciple(
    id integer primary key autoincrement,
    idfa text not null,
    uuid text not null,
    cookie text not null,
    userid text not null,
    contrib integer default 0,
    valid integer default 1
);

CREATE INDEX IX_USERID ON disciple(userid);
