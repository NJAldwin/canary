begin transaction;
create table if not exists keys
(
        /* The API key */
        apikey text(36) collate nocase primary key,
        /* Whether the key is restricted to use from one IP */
        restricted integer(1),
        /* The IP from which requests will be made */
        ip text,
        /* An email associated with the key */
        email text collate nocase,
        /* The Unix timestamp of when the API key was created */
        created integer
);
commit;