drop table if exists nodes;
create table nodes (
  id integer primary key autoincrement,
  name text not null unique
);
