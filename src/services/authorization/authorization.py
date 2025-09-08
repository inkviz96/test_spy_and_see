from enum import Enum, auto

from services.redis import RedisService, redis_service


class TokenType(Enum):
    ACCESS = auto()
    REFRESH = auto()
    RESET_PASSWORD = auto()
    CONFIRM_PASSWORD = auto()


class TokenWhitelistService:
    TOKEN_PREFIX = "JWT_"  # noqa: S105

    def __init__(self, redis: RedisService):
        """Initialize the token whitelist service.

        Args:
            redis (RedisService): The Redis service.
        """
        self.redis = redis

    async def add(
        self, token: str, username: str, expiration_time: int, token_type: TokenType
    ) -> None:
        """Add a token to the whitelist.

        Args:
            token (str): The token.
            username (str): The user name.
            expiration_time (int): The expiration time in seconds.
            token_type (TokenType): The token type.
        """
        await self.redis.set(
            f"{self.TOKEN_PREFIX}{token_type}_{username}",
            token,
            expire=expiration_time,
        )

    async def clear_user_tokens(self, username: str) -> None:
        """Clear all tokens for a user.

        Args:
            username (str): The user name.
        """
        access_token_key = f"{self.TOKEN_PREFIX}{TokenType.ACCESS}_{username}"
        refresh_token_key = f"{self.TOKEN_PREFIX}{TokenType.REFRESH}_{username}"
        await self.redis.delete(access_token_key)
        await self.redis.delete(refresh_token_key)

    async def check_token_on_the_whitelist(self, token: str, username: str) -> bool:
        """Check token on the whitelist.

        Args:
            token: Token.
            username: User name.

        Returns:
            bool: True if token is on the whitelist.
        """
        access_token = await self.redis.get(key=f"JWT_{TokenType.ACCESS}_{username}")
        refresh_token = await self.redis.get(key=f"JWT_{TokenType.REFRESH}_{username}")

        access_token_decoded = access_token.decode() if access_token else None
        refresh_token_decoded = refresh_token.decode() if refresh_token else None

        return token in {access_token_decoded, refresh_token_decoded}


token_whitelist_service = TokenWhitelistService(redis_service)
