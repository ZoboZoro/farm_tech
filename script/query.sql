
    CREATE SCHEMA IF NOT EXISTS silver;
    
    CREATE TABLE IF NOT EXISTS silver.news (
        "id" TEXT,
        "href" TEXT,
        "published_at" TEXT,
        "title" TEXT,
        "description" TEXT,
        "body" TEXT,
        "language" TEXT,
        "image" TEXT,
        "is_duplicate" BOOLEAN,
        "is_free" BOOLEAN,
        "is_breaking" BOOLEAN,
        "read_time" BIGINT,
        "sentences_count" BIGINT,
        "paragraphs_count" BIGINT,
        "words_count" BIGINT,
        "characters_count" BIGINT,
        "author.id" REAL,
        "author.name" TEXT,
        "source.id" BIGINT,
        "source.type" TEXT,
        "source.bias" TEXT,
        "source.rankings.opr" BIGINT,
        "source.location.country_name" TEXT,
        "source.location.country_code" TEXT,
        "source.favicon" TEXT,
        "sentiment.overall.score" REAL,
        "sentiment.overall.polarity" TEXT,
        "sentiment.title.score" REAL,
        "sentiment.title.polarity" TEXT,
        "sentiment.body.score" REAL,
        "sentiment.body.polarity" TEXT,
        "story.id" BIGINT,
        "story.uri" TEXT
        );
    