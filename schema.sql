drop table if exists nodes;
create table nodes (
  id integer primary key autoincrement,
  name text not null unique
);

drop table if exists reports;
create table reports (
  id integer primary key autoincrement,
  node_id integer not null
);
