drop table disciple;
create table disciple(
    id integer primary key autoincrement,
    idfa text not null,
    uuid text not null,
    cookie text not null,
    userid text not null,
    master_id text not null,
    contrib integer default 0,
    valuable integer default 1,
    has_uncompleted integer default 0,
    start_time integer default 0,
    wait_seconds integer default 0,
    now_task text default '',
    freeze_status integer  default 0,
    balance text default 0,
    today_income text default 0,
    total_income text default 0,
    withdraw_realname text default ''
);

CREATE INDEX IX_USERID ON disciple(userid);
