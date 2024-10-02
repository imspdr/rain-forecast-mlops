CREATE TABLE rain_train
(
    id              BIGINT        NOT NULL AUTO_INCREMENT,
    name            VARCHAR(50)   NOT NULL,
    cpu_size        VARCHAR(50)   NOT NULL,
    memory_size     VARCHAR(50)   NOT NULL,
    start_day       VARCHAR(50)   NOT NULL,
    end_day         VARCHAR(50)   NOT NULL,
    created_at      DATETIME      NOT NULL,
    finished_at     DATETIME      NULL,
    status          VARCHAR(255)  NOT NULL,
    data_dist       LONGTEXT      NULL,
    model_name      VARCHAR(50)   NULL,
    model_info      LONGTEXT      NULL,
    model_pkl       LONGBLOB      NULL,
    PRIMARY KEY (id)
) CHARACTER SET utf8mb4;

CREATE TABLE rain_serving_model
(
    id                BIGINT       NOT NULL AUTO_INCREMENT,
    train_id          BIGINT       NOT NULL,
    hostname          VARCHAR(255) NOT NULL,
    url               VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
    FOREIGN KEY (train_id) REFERENCES `rain_train` (id) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
