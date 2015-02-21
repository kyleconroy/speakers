# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

FORWARD = """
CREATE FUNCTION conference_fts_document(integer) RETURNS tsvector AS $$
DECLARE
    conference_document TEXT;
BEGIN
    SELECT concat_ws(' ', name, tagline, twitter_handle, twitter_hashtag)
        INTO conference_document FROM cfp_conference WHERE id=$1;
    RETURN to_tsvector('pg_catalog.simple', conference_document);
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION conference_fts_document_trigger() RETURNS TRIGGER AS $$
BEGIN
    NEW.fts_document=conference_fts_document(NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

ALTER TABLE cfp_conference ADD COLUMN fts_document tsvector;
UPDATE cfp_conference SET fts_document=conference_fts_document(id);

CREATE TRIGGER conference_fts_update_trigger BEFORE
    UPDATE ON cfp_conference FOR EACH ROW EXECUTE
    PROCEDURE conference_fts_document_trigger();
CREATE TRIGGER conference_fts_insert_trigger BEFORE
    INSERT ON cfp_conference FOR EACH ROW EXECUTE
    PROCEDURE conference_fts_document_trigger();
CREATE INDEX conference_fts_index ON cfp_conference USING gin(fts_document);
"""

BACKWARD = """
DROP INDEX conference_fts_index;
ALTER TABLE cfp_conference DROP COLUMN fts_document;
DROP TRIGGER conference_fts_update_trigger ON cfp_conference;
DROP TRIGGER conference_fts_insert_trigger ON cfp_conference;
DROP FUNCTION conference_fts_document (integer);
DROP FUNCTION conference_fts_document_trigger ();
"""


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0023_auto_20150219_0614'),
    ]

    operations = [
        migrations.operations.RunSQL(FORWARD, BACKWARD)
    ]
