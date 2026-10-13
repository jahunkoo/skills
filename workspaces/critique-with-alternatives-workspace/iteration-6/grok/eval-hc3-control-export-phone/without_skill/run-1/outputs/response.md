The customer CSV now ends with a `phone` column, and the change is committed as `fce780d`.

`src/export.js` writes `id`, `name`, `email`, `city`, then `phone`. A missing phone is left blank, the same way other empty fields are handled. All three tests passed.