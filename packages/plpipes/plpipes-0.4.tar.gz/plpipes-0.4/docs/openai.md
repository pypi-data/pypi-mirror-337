# OpenAI (ChatGPT)

PLPipes provides a very thin wrapper for the `openai` package.

Currently, it just automates the authentication side, reading the API
key from the configuration and setting it on the client package.

```python
import plpipes.cloud.openai as openai
completion = openai.Completion.create(...)
```

If used outside actions, if should be taken into account that
PLPipes config subsystem must be initialized before importing
`plpipes.cloud.openai`.

## Configuration

```yaml
cloud:
  openai:
    auth:
      api_key: YOUR-SECRET-KEY-GOES-HERE
```
