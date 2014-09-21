
drop table source;
create table source
(
id serial primary key not null,
active boolean,
name text,
url text,
type text,
created timestamp,
updated timestamp
);

drop table story;
create table story
(
id serial primary key not null,
source_id int,
path text,
created timestamp,
updated timestamp,
times_updated int,
source_url text,
source_name text,
fuzzy_summary text,
s_id text,
s_date timestamp,
s_title text,
s_summary text,
s_author text,
s_link text,
s_tags text,
s_media_content text
);

drop table topic;
create table topic
(
id serial primary key not null,
name text,
created timestamp,
updated timestamp
);

drop table topic_story;
create table topic_story
(
id serial primary key not null,
topic_id int,
story_id int,
score int,
created timestamp
);

drop table activity;
create table activity
(
id serial primary key not null,
story_id int,
created timestamp,
who text
);
