ALTER TABLE subscribers
  ADD COLUMN status VARCHAR(20) DEFAULT 'active';

CREATE INDEX idx_subscribers_status ON subscribers(status);
