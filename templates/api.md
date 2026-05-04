# <Resource name> API

Use this API to <primary purpose of the resource>.

- <Primary capability 1>
- <Primary capability 2>
- <Primary capability 3>

> Note: <Important prerequisite or behavior note.>

---

## <METHOD> /<endpoint>

Use this endpoint to <what the endpoint does>.

### What happens

- <System behavior 1>
- <System behavior 2>
- <System behavior 3>

---

### Path parameters

| Name           | Type   | Required | Description   |
| -------------- | ------ | -------- | ------------- |
| `<param_name>` | string | Yes      | <Description> |

*(Remove if not applicable)*

---

### Query parameters

| Name           | Type   | Required | Description   |
| -------------- | ------ | -------- | ------------- |
| `<param_name>` | string | No       | <Description> |

*(Remove if not applicable)*

---

### Request body

| Field          | Type   | Required | Description   |
| -------------- | ------ | -------- | ------------- |
| `<field_name>` | string | Yes      | <Description> |

*(Remove if not applicable)*

---

### Example request

```bash
curl -X <METHOD> "http://<host>/<endpoint>" \
  -H "x-api-key: <api-key>"
```

---

### Example response

```json
{
  "<field>": "<value>"
}
```

---

### Response fields

| Field          | Type   | Description   |
| -------------- | ------ | ------------- |
| `<field_name>` | string | <Description> |

---

### Error responses

#### 400 Bad Request

Returned when the request is malformed or contains invalid data.

```json
{
  "detail": "<error message>"
}
```

#### 404 Not Found

Returned when the requested resource does not exist.

```json
{
  "detail": "<resource not found message>"
}
```

#### 422 Unprocessable Entity

Returned when request validation fails.

Include only for endpoints with validated input.

```json
{
  "detail": [
    {
      "loc": ["body", "field"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

*(Remove errors that do not apply to this endpoint)*

---

## Additional details

- All endpoints require a valid `x-api-key` header.
- <Behavior note (processing, ordering, async, etc.)>
- <Constraints or assumptions>

---

## Related documentation

- [Workflows](workflows.md)
- [Errors](errors.md)
- [Related API page](related.md)
