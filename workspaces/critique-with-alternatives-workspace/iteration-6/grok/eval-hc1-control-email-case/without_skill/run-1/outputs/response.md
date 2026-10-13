`createUser()` now lowercases the email before the duplicate check and before saving, and that change is committed on `main` as `760c2cb`.

The address is trimmed and passed through `toLowerCase()` once. That value is what the duplicate check compares and what gets stored, so `Bob@Example.invalid` and `bob@example.invalid` are the same account. Existing tests passed.