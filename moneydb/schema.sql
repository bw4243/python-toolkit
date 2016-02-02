
drop table if exists User;
create table User(
    id integer primary key autoincrement,
    user_id text not null,
    nick_name text not null,
    app_type text not null,
    oid_md5 text,
    idfa text not null,
    idfv text,
    uid text,
    cookie text not null,
    valuable integer,
    is_working integer,
    balance text,
    today_income text,
    total_income text,
    add_time text not null,
    update_time text not null,
    field1 text,
    field2 text,
    field3 text

);



drop table if exists Task;
create table Task(
    id integer primary key autoincrement,
    common_user_id integer not null,
    task_id text not null,
    order_id text,
    task_name text not null,
    bundle_id text not null,
    process_name text not null,
    status text not null,
    block_type text not null,
    fire_time text not null,
    app_type text not null,
    add_time text not null,
    update_time text not null,
    field1 text,
    field2 text,
    field3 text
);

