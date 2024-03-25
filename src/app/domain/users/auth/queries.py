from contextvars import ContextVar


class CurrentUserTokenQuery:
    def __init__(self, token_ctx_var: ContextVar[str]) -> None:
        self.token_ctx_var = token_ctx_var

    async def __call__(self) -> str | None:
        return self.token_ctx_var(None)
