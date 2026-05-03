~~# <Resource> API

Use this API to <primary purpose of the resource>.

- <Primary capability 1>
- <Primary capability 2>
- <Primary capability 3>
- <Primary capability 4>

> <Important note about data availability, processing, or prerequisites>

---

## <METHOD> /<endpoint>

Use this endpoint to <what this endpoint does>.

### What happens

- <System behavior 1>
- <System behavior 2>
- <System behavior 3>
- <System behavior 4>

---

### Path parameters

| Name         | Type   | Required | Description   |
|--------------|--------|----------|---------------|
| <param_name> | <type> | Yes/No   | <description> |

*(Remove section if not applicable)*

---

### Query parameters

| Name         | Type   | Required | Description   |
|--------------|--------|----------|---------------|
| <param_name> | <type> | Yes/No   | <description> |

*(Remove section if not applicable)*

---

### Request body

| Field        | Type   | Required | Description   |
|--------------|--------|----------|---------------|
| <field_name> | <type> | Yes/No   | <description> |

*(Remove section if not applicable)*

---

### Example request

```bash
curl -X <METHOD> "http://<host>/<endpoint>" \
  -H "x-api-key: <api-key>" \
  <additional headers or flags>
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

| Field        | Type   | Description   |
|--------------|--------|---------------|
| <field_name> | <type> | <description> |

---

### Error responses

#### 400 Bad Request

```json
{
  "detail": "<error message>"
}
```

#### 404 Not Found

```json
{
  "detail": "<resource not found message>"
}
```

*(Add additional errors as needed)*

---

## <METHOD> /<endpoint-2>

Use this endpoint to <what this endpoint does>.

### What happens

- <System behavior 1>
- <System behavior 2>

---

### Example request

```bash
curl -X <METHOD> "http://<host>/<endpoint-2>" \
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

## Additional details

- All endpoints require a valid `x-api-key` header
- Behavior note about data or processing 
- Performance or ordering note 
- Any important constraints or assumptions  

---

## Related documentation

- [Workflows](workflows.md)
- [<Related API page>](related.md)
- [Errors](errors.md)

---

## Final rule set (lock this in)

- Use **sentence case headings**  
- Use **What happens** for behavior  
- Use **bash** for requests  
- Use **json** for responses  
- Use **text** for conceptual examples  
- Use **Resolution** (not Fix) everywhere~~ 
