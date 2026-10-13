Added `.` to `USERNAME_CHARS` so signup accepts `bob.k`. Updated mention parsing to recognize internal dots while treating a final period as punctuation.

All 6 tests pass. Committed as `1bea5ed` (`Allow periods in usernames and mentions`).